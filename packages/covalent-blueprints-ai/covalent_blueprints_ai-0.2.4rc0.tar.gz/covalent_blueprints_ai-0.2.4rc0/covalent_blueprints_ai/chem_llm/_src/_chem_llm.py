# Copyright 2024 Agnostiq Inc.
"""Deploy an LLM-HPC pipeline that infers molecules from user prompts
and computes their optical spectra using GPAW/ASE.
"""
import os
import sys
import time
from typing import List

import _utilities
import cloudpickle
import covalent as ct
import covalent_cloud as cc
import plotly.graph_objects as go
import requests
from _utilities import *

from covalent_blueprints_ai._versions import covalent_blueprints_pkg, covalent_cloud_pkg

cloudpickle.register_pickle_by_value(_utilities)
cloudpickle.register_pickle_by_value(sys.modules[__name__])

GPAW_ENV = "dft-gpaw@blueprints"

cc.create_env(
    name=GPAW_ENV,
    pip=[
        "ase",
        "scikit-learn",
        "plotly",
        covalent_cloud_pkg,
        covalent_blueprints_pkg,
    ],
    conda={
        "channels": ["conda-forge"],
        "dependencies": [
            "gpaw",
            "blas",
            "cupy",
            "openmpi",
            "openssh",
            "scalapack",
            "fftw",
            "qe",
        ],
    },
)


cc.create_env(
    name="nim-llama3.1-8b-instruct",
    pip=[
        covalent_cloud_pkg,
        covalent_blueprints_pkg,
    ],
    base_image="public.ecr.aws/covalent/ag-algos:l61250",
    wait=True,
)

CC_API_KEY = cc.get_api_key()
TIME_LIMIT = "3 hours"


hs_gpu = cc.HyperstackCloudExecutor(
    env="nim-llama3.1-8b-instruct", num_cpus=4, memory="64GB", time_limit=TIME_LIMIT
)

dft_light = cc.AWSCloudExecutor(
    memory="2GB",
    env=GPAW_ENV,
)

dft_heavy = cc.AWSCloudExecutor(
    num_cpus=18, memory="32GB", env=GPAW_ENV, time_limit="4 hours"
)

interface_ex = cc.AWSCloudExecutor(
    num_cpus=4, memory="12GB", env=GPAW_ENV, time_limit=TIME_LIMIT
)


CHEM_AGENT_SYSTEM_PROMPT = """You are a chemistry assistant. \
Use your chemistry knowledge to identify a short list of molecules \
that fit the user's description. Do NOT include proteins or other \
large bio-molecules. Focus on small, common molecules and ionic \
compounds.

Always respond ONLY with a comma-separated list of 2-3 molecules \
names. Here are some examples of how to structure your response.

User: "alcohols most readily collected during spirit distillation"
Assistant: "ethanol, methanol"

User: "The beach is always fun, but sunburn isn't. Sunscreen is \
great isn't it? Which chemicals are in it?"
Assistant: "oxybenzone, avobenzone, homosalate"
"""


@cc.service(executor=hs_gpu, name="Chem. NIM Llama3.1 8B")
def nim_llama3_8b_service(poll_freq_secs=4):
    """Hosts the Llama3.1 8B NIM as a Covalent Function Service."""
    # Start local server.
    python_path = ":".join(
        [
            "/var/lib/covalent/lib",
            "/opt/nim/llm",
            "/opt/nim/llm/.venv/lib/python3.10/site-packages",
        ]
    )
    os.system(
        "unset VLLM_ATTENTION_BACKEND && "
        f"PYTHONPATH={python_path} "
        "/bin/bash /opt/nvidia/nvidia_entrypoint.sh "
        "/opt/nim/start-server.sh &"
    )
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    # Poll server.
    while True:
        try:
            response = requests.get(
                "http://localhost:8000/v1/health/ready", headers=headers, timeout=600
            )
            response.raise_for_status()
            return {
                "url": "http://localhost:8000/v1/chat/completions",
                "headers": headers,
            }
        except Exception:  # pylint: disable=broad-except
            time.sleep(poll_freq_secs)


@nim_llama3_8b_service.endpoint("/generate")
def generate(url=None, headers=None, *, prompt=None, messages=None, kwargs=None):
    """Returns the raw response as JSON.

    kwargs:
        prompt: The user prompt.
        messages: A list of messages.
        kwargs: Additional keyword arguments.
    """
    if not (prompt or messages):
        return "Please provide a prompt or a list of messages."

    # Construct request.
    payload = {"model": "meta/llama-3.1-8b-instruct"}

    # Handle message or prompt.
    if messages:
        payload["messages"] = messages
    elif prompt:
        payload["messages"] = [{"role": "user", "content": prompt}]

    # Include any additional kwargs.
    for k, v in (kwargs or {}).items():
        payload[k] = v

    # Forward request to local NIM server.
    response = requests.post(url=url, headers=headers, json=payload, timeout=300)
    response.raise_for_status()
    return response.json()


@ct.electron(
    executor=dft_heavy, deps_bash="gpaw install-data ~/gpaw-setups-24.1.0 --register"
)
def dft(name: str) -> dict:
    """Use GPAW/ASE to compute the optical spectrum."""
    return SpectrumCalculator(name).compute()


@ct.electron(executor=dft_light)
def plot_spectra(s_dicts: List[dict]):
    """Create a plotly figure with the photo-absorption spectra."""
    fig = go.Figure()
    for s in s_dicts:
        fig.add_trace(
            go.Scatter(x=s["energy"], y=s["osz"], mode="lines", name=s["name"])
        )

    fig.update_layout(
        title="Photoabsorption Spectrum",
        xaxis_title="Energy (eV)",
        yaxis_title="Absorption (arb. units)",
    )
    return fig


@ct.lattice(executor=dft_light, workflow_executor=dft_light)
def compute_optical_spectra(compound_names: List[str]):
    """Parallel compute the optical spectra of a list of molecules."""
    dft_results = []
    for name in compound_names:
        dft_results.append(dft(name))
    return plot_spectra(dft_results)


@cc.service(executor=interface_ex, name="Chem. Interface")
def chem_interface_service(llm_backend):
    """Infers molecule names from user prompts"""
    cc.save_api_key(CC_API_KEY)
    llm = LLMAgent(
        system_prompt=CHEM_AGENT_SYSTEM_PROMPT,
        backend=llm_backend,
        process_content=lambda x: [x.strip() for x in x.strip(" .").split(", ")],
    )
    return {"llm": llm}


@chem_interface_service.endpoint("/spectra")
def get_spectra(
    llm: LLMAgent,
    *,
    prompt: str = "",
    redispatch_id: str = "",
):
    """Infer molecules and compute their optical spectra.

    kwargs:
        prompt: The user prompt.
        redispatch_id: The ID to redispatch the response.
    """
    if not prompt:
        return {"error": "Please provide a prompt."}

    response = llm.generate(prompt)
    compound_names = []
    for name in response["content"]:
        if (SpectrumCalculator(name).load().cid) is None:
            continue
        compound_names.append(name)

    if len(compound_names) == 0:
        raise ValueError(
            f"No valid molecules found in response content '{response['content']}'."
        )

    cc_dispatch = cc.redispatch if redispatch_id else cc.dispatch
    return {"id": cc_dispatch(compute_optical_spectra)(compound_names)}


@ct.lattice(
    executor=cc.AWSCloudExecutor(memory="2GB", env=GPAW_ENV, time_limit="4 hours"),
    workflow_executor=cc.AWSCloudExecutor(
        memory="2GB", env=GPAW_ENV, time_limit="4 hours"
    ),
)
def deploy_chem_llm():
    """Set up the LLM-HPC pipeline in Covalent Cloud"""
    llm_backend = nim_llama3_8b_service()
    user_client = chem_interface_service(llm_backend)
    return llm_backend, user_client


dispatch_id = cc.dispatch(deploy_chem_llm)()

# TODO: test inside workflow
# TODO: require NGC_API_KEY

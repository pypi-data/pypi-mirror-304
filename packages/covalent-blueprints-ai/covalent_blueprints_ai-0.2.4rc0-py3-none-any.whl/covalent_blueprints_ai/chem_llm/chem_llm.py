# Copyright 2024 Agnostiq Inc.
"""Blueprint for an LLM-HPC pipeline that infers molecules from user
prompts and launches GPAW/ASE jobs to compute optical spectra for each
molecule."""

from covalent_blueprints import blueprint, get_blueprint
from covalent_blueprints.blueprints.templates import ServiceWorkflowBlueprint

from covalent_blueprints_ai._prefix import PREFIX


@blueprint("LLM-HPC Pipeline for Optical Spectra of Chemicals")
def chem_llm():
    """A blueprint that deploys an LLM-HPC pipeline to infer
    molecules from user prompts and compute their optical spectra.

    The deployed interface service includes one endpoint:
    - `/spectra`: Infer molecules and dispatch spectral calculations.

    This endpoint accepts the following keyword-only parameters:
    - `prompt`: The user prompt.
    - `redispatch_id`: Optional ID to redispatch another HPC workflow.

    Returns:
        Covalent blueprint that deploys an LLM-HPC pipeline for
        computing optical spectra of chemicals.

    Example:

        ```
        from covalent_blueprints_ai import chem_llm

        chem_llm_bp = chem_llm()
        llm_client, user_client = chem_llm_bp.run()

        # Generate optical spectra based on a prompt
        prompt = "Compounds in cinnamon that give it its flavor."
        spectra_results = user_client.spectra(prompt=prompt)

        # Tear down the deployment.
        llm_client.teardown()
        user_client.teardown()
        ```
    """
    bp = get_blueprint(f"{PREFIX}/chem_llm", _cls=ServiceWorkflowBlueprint)
    bp.executors.set_executor_key(
        electron_key="dft",
        service_key="nim_llama3_8b_service",
    )
    bp.set_default_inputs()

    return bp

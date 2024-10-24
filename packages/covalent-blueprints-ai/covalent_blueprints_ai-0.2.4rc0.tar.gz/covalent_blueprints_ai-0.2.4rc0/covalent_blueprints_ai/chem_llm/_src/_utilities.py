# Copyright 2024 Agnostiq Inc.
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import requests
from ase import Atoms
from ase.data import chemical_symbols
from covalent_cloud.function_serve.deployment import Deployment

PUBCHEM_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"


class SpectrumCalculator:
    """Use GPAW/ASE together with PubChem data to compute the optical
    spectrum of a molecule."""

    GET_CID_URL = f"{PUBCHEM_URL}/compound/name/{{name}}/cids/TXT"
    GET_DATA_URL = f"{PUBCHEM_URL}/compound/cid/{{cid}}/JSON"

    def __init__(self, name: str):
        """Initialize the SpectrumCalculator with a molecule name.

        Args:
            name: The name of the molecule to compute the spectrum for.
        """
        self.name = name
        self.cid = None
        self.molecule_data = None
        self.spectrum: Optional[Dict[str, List[float]]] = None

    @property
    def molecule(self) -> Atoms:
        """Return the molecule as an ASE Atoms object."""
        if self.molecule_data is None:
            self.load()
        return Atoms(**self.molecule_data)

    def _download_molecule(self) -> Optional[dict]:
        try:
            data = self._fetch_molecule_data()
        except Exception:  # pylint: disable=broad-except
            return None

        if not data:
            return None

        return self._extract_coordinates(data)

    def _fetch_molecule_data(self) -> dict:
        get_data_url = self.GET_DATA_URL.format(cid=self.cid)
        get_data_url += "/?record_type=3d"
        response = requests.get(get_data_url, timeout=60)
        response.raise_for_status()
        return response.json()

    def _extract_coordinates(self, data: dict) -> dict:
        symbols = []
        xyz = []

        for compound in data.get("PC_Compounds", []):
            element_list = compound.get("atoms", {}).get("element", [])
            coordinates = self._get_coordinates_from_compound(compound)
            for aid, x, y, z in coordinates:
                symbol = chemical_symbols[element_list[aid - 1]]
                symbols.append(symbol)
                xyz.append((x, y, z))

        return {"symbols": symbols, "positions": xyz}

    def _get_coordinates_from_compound(self, compound: dict) -> list:
        coordinates = []
        atoms_aid = compound.get("atoms", {}).get("aid", [])

        for coord in compound.get("coords", []):
            for conformer in coord.get("conformers", []):
                x_coords = conformer.get("x", [])
                y_coords = conformer.get("y", [])
                z_coords = conformer.get("z", [])
                if not z_coords:
                    z_coords = [0] * len(x_coords)

                coordinates.extend(zip(atoms_aid, x_coords, y_coords, z_coords))

        return coordinates

    def _download_cid(self) -> Optional[int]:
        try:
            get_cid_url = self.GET_CID_URL.format(name=self.name)
            response = requests.get(get_cid_url, timeout=60)
            response.raise_for_status()
            cid = response.text.strip()
            return int(cid)
        except Exception:  # pylint: disable=broad-except
            return None

    def _read_spectrum(self, path: Path) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            lines = [line for line in lines if not line.startswith("#")]

        keys = ["energy", "osz", "x", "y", "z"]
        data = {"name": self.name, **{key: [] for key in keys}}
        for line in lines:
            vals = [float(x) for x in line.split()]
            for i, key in enumerate(keys):
                data[key].append(vals[i])

        return data

    def load(self) -> "SpectrumCalculator":
        """Load data from PubChem and store it in the
        SpectrumCalculator object."""
        self.cid = self._download_cid()
        self.molecule_data = self._download_molecule()
        return self

    def compute(
        self,
        e_min: float = 0.0,
        e_max: float = 20.0,
        center: Optional[float] = 5.0,
        **gpaw_kwargs,
    ) -> Optional[Dict[str, List[float]]]:
        """Compute the optical spectrum of the molecule.

        Args:
            e_min: Minimum energy (eV). Defaults to 1.0.
            e_max: Maximum energy (eV). Defaults to 100.0.
            center: Optional size of surrounding vacuum when centering
                the molecule. Defaults to 5.0 (Ang.).
            **kwargs: Additional keyword arguments for the GPAW
                calculator. Defaults to
                {"mode": "fd", "xc": "PBE", "h": 0.25}.

        Returns:
            The spectrum dictionary.
        """
        from gpaw import GPAW
        from gpaw.lrtddft import LrTDDFT, photoabsorption_spectrum

        output = self.name + ".dat"
        output_path = Path(output).expanduser().absolute()
        molecule = deepcopy(self.molecule)
        if center:
            molecule.center(vacuum=center)

        kwargs = {"mode": "fd", "xc": "PBE", "h": 0.25, **gpaw_kwargs}
        calc = GPAW(**kwargs)
        molecule.set_calculator(calc)
        molecule.get_potential_energy()
        lr = LrTDDFT(calc, xc="LDA")
        lr.write(str(output_path.with_suffix(".gz")))

        photoabsorption_spectrum(lr, output, e_min=e_min, e_max=e_max)
        self.spectrum = self._read_spectrum(str(output_path))
        return self.spectrum


class LLMAgent:
    """Define an LLM Agent with custom prompting and optional response
    format enforcement."""

    def __init__(
        self,
        system_prompt: str,
        backend: Deployment,
        user_prompt_template: str = "{}",
        prepend_messages: Optional[List[Dict[str, str]]] = None,
        process_content: Optional[Callable[[Dict[str, str]], Dict[str, str]]] = None,
    ):
        self.backend = backend
        self.system_prompt = system_prompt
        self.user_prompt_template = user_prompt_template
        self.prepend_messages = prepend_messages or []
        self.process_content = process_content

    def generate(self, prompt: str, **kwargs) -> Any:
        """Generate a response to a user prompt."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.prepend_messages,
            {"role": "user", "content": self.user_prompt_template.format(prompt)},
        ]
        response_message = self.backend.generate(messages=messages, kwargs=kwargs)[
            "choices"
        ][0]["message"]
        if self.process_content is not None:
            response_message["content"] = self.process_content(
                response_message.get("content", None)
            )

        return response_message

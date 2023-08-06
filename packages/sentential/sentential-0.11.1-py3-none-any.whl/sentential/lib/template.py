from shutil import copy
from os import makedirs
from pathlib import PosixPath
from os.path import dirname, abspath, exists
from jinja2 import Environment, FileSystemLoader, Template
from sentential.lib.shapes import SNTL_ENTRY_VERSION, derive_paths
from sentential.lib.ontology import Ontology
from sentential.lib.shapes import Envs
from typing import cast

PACKAGE_PATH = PosixPath(dirname(abspath(__file__))).parent


class Init:
    def __init__(self, repository_name: str, runtime: str) -> None:
        self.repository_name = repository_name
        self.runtime = runtime
        self.entry_version = SNTL_ENTRY_VERSION
        self.path = derive_paths()
        self.jinja = Environment(loader=FileSystemLoader(f"{PACKAGE_PATH}/templates"))

    def scaffold(self) -> None:
        if not exists(self.path.src):
            makedirs(self.path.src)

        self._write(self.jinja.get_template("Dockerfile"), self.path.dockerfile)

        copy(f"{PACKAGE_PATH}/templates/policy.json", self.path.policy)
        copy(f"{PACKAGE_PATH}/templates/shapes.py", self.path.shapes)

    def _write(self, template: Template, write_to: PosixPath) -> PosixPath:
        if not exists(write_to):
            with open(write_to, "w+") as f:
                f.writelines(
                    template.render(
                        repository_name=self.repository_name,
                        runtime=self.runtime,
                        entry_version=self.entry_version,
                        paths=self.path,
                    )
                )

        return write_to


class Policy:
    def __init__(self, ontology: Ontology) -> None:
        self.ontology = ontology
        self.jinja = Environment(loader=FileSystemLoader("."))

    def render(self) -> str:
        template = self.jinja.get_template("policy.json")
        return template.render(
            context=self.ontology.context, env=cast(Envs, self.ontology.envs.parameters)
        )

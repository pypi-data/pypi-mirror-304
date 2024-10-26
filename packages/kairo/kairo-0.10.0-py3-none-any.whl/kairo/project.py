"""
This file contains the project manager class.
"""

from functools import cached_property
from os import path, mkdir, listdir
from shutil import rmtree

from kairo.constants import DEFAULT_PROJECT_DIR


class Manager:
    """
    The project manager class.
    """

    def __init__(self):
        self._project_dir = path.join(path.dirname(path.abspath(__file__)), DEFAULT_PROJECT_DIR)

    @cached_property
    def project_dir(self) -> str:
        """
        Get the project directory.

        :return: The project directory.
        """
        return self._project_dir

    def add(self, name: str) -> None:
        """
        Add a new project to the project directory.

        :param name: The name of the project.

        :raises ValueError: If the project name is empty.

        :return: None
        """
        if not name:
            raise ValueError("Project name cannot be empty.")

        new_project_dir = path.join(self.project_dir, name)
        if path.exists(new_project_dir):
            return

        mkdir(new_project_dir)

    def remove(self, name: str) -> None:
        """
        Remove a project from the project directory.

        :param name: The name of the project.

        :raises ValueError: If the project name is empty.

        :return: None
        """
        if not name:
            raise ValueError("Project name cannot be empty.")

        new_project_dir = path.join(self.project_dir, name)
        if path.exists(new_project_dir):
            rmtree(new_project_dir)

    def list(self) -> list[str]:
        """
        List all projects in the project directory.

        :return: A list of project names.
        """
        return [
            d for d in listdir(self.project_dir) if path.isdir(path.join(self.project_dir, d))
        ]

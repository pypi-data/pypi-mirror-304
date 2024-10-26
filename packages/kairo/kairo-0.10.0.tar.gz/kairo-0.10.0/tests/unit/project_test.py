import tempfile
from os import path

import pytest
from kairo.project import Manager


@pytest.fixture()
def with_project_manager(mocker):
    with tempfile.TemporaryDirectory() as temp_dir:
        mocker.patch.object(Manager, "project_dir", mocker.PropertyMock(return_value=temp_dir))
        yield Manager()


class TestProjectManager:
    def test_create_project(self, with_project_manager):
        # when
        with_project_manager.add("test_project")

        # then
        assert path.exists(path.join(with_project_manager.project_dir, "test_project"))

    def test_delete_project(self, with_project_manager):
        # when
        with_project_manager.add("test_project")
        with_project_manager.remove("test_project")

        # then
        assert not path.exists(path.join(with_project_manager.project_dir, "test_project"))

    def test_list_projects(self, with_project_manager):
        # when
        with_project_manager.add("test_project")
        with_project_manager.add("another_project")

        # then
        assert all(
            project in with_project_manager.list()
            for project in ["test_project", "another_project"]
        )

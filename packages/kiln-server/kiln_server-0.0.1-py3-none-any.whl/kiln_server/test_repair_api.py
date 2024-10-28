import json
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from libs.core.kiln_ai.datamodel import (
    DataSource,
    DataSourceType,
    Project,
    Task,
    TaskOutput,
    TaskRun,
)
from libs.server.kiln_server.repair_api import (
    RepairRunPost,
    RepairTaskApiInput,
    connect_repair_api,
)


@pytest.fixture
def app():
    app = FastAPI()
    connect_repair_api(app)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def data_source():
    return DataSource(
        type=DataSourceType.synthetic,
        properties={
            "model_name": "gpt_4o",
            "model_provider": "openai",
            "adapter_name": "langchain_adapter",
            "prompt_builder_name": "simple_prompt_builder",
        },
    )


@pytest.fixture
def improvement_task(tmp_path) -> Task:
    project_path = tmp_path / "test_project" / "project.kiln"
    project_path.parent.mkdir()

    project = Project(name="Test Project", path=str(project_path))
    project.save_to_file()

    task = Task(name="Test Task", instruction="Test Instruction", parent=project)
    task.save_to_file()
    return task


@pytest.fixture
def improvement_task_run(data_source, improvement_task):
    task_run = TaskRun(
        input="Test Input",
        input_source=data_source,
        parent=improvement_task,
        output=TaskOutput(output="Test Output", source=data_source),
    )
    task_run.save_to_file()

    return task_run


@pytest.fixture
def mock_repair_task_run(improvement_task, data_source):
    return TaskRun(
        output=TaskOutput(
            output="Test Output",
            source=data_source,
        ),
        input="The input to the improvement task",
        input_source=data_source,
    )


@pytest.fixture
def mock_langchain_adapter(mock_repair_task_run):
    with patch("libs.server.kiln_server.repair_api.LangChainPromptAdapter") as mock:
        mock_adapter = AsyncMock()
        mock_adapter.invoke = AsyncMock()
        mock.return_value = mock_adapter

        mock_adapter.invoke.return_value = mock_repair_task_run

        yield mock_adapter


@pytest.fixture
def mock_run_and_task(improvement_task, improvement_task_run):
    with patch("libs.server.kiln_server.repair_api.task_and_run_from_id") as mock:
        mock.return_value = (improvement_task, improvement_task_run)
        yield mock


def test_repair_run_success(
    mock_run_and_task,
    mock_langchain_adapter,
    client,
    improvement_task,
    mock_repair_task_run,
):
    # Arrange
    input_data = RepairTaskApiInput(evaluator_feedback="Fix this issue")

    # Act
    response = client.post(
        "/api/projects/proj-ID/tasks/task-ID/runs/run-ID/run_repair",
        json=input_data.model_dump(),
    )

    # Assert
    assert response.status_code == 200
    res = response.json()
    repaired_output = res["output"]
    assert TaskOutput.model_validate(repaired_output) == mock_repair_task_run.output
    mock_langchain_adapter.invoke.assert_awaited_once()


def test_save_repair_success(
    mock_run_and_task,
    mock_langchain_adapter,
    client,
    improvement_task,
    mock_repair_task_run,
):
    # Arrange
    input_data = RepairRunPost(
        repair_run=mock_repair_task_run.model_dump(),
        evaluator_feedback="Fix this issue",
    )

    # Act
    response = client.post(
        "/api/projects/proj-ID/tasks/task-ID/runs/run-ID/repair",
        json=json.loads(input_data.model_dump_json()),
    )

    # Assert
    res = response.json()
    assert response.status_code == 200
    repaired_output = res["repaired_output"]
    assert TaskOutput.model_validate(repaired_output) == mock_repair_task_run.output
    assert res["repair_instructions"] == "Fix this issue"
    assert res["input"] == "Test Input"

    # Verify that the run was updated in the file system
    updated_run = improvement_task.runs()[0]
    assert updated_run.repair_instructions == "Fix this issue"
    assert updated_run.repaired_output == mock_repair_task_run.output


def test_repair_run_missing_model_info(
    mock_run_and_task,
    mock_langchain_adapter,
    client,
    improvement_task,
    mock_repair_task_run,
):
    # Arrange
    input_data = RepairTaskApiInput(evaluator_feedback="Fix this issue")
    mock_run_and_task.return_value[1].output.source.properties["model_name"] = None
    mock_run_and_task.return_value[1].output.source.properties["model_provider"] = None

    # Act
    response = client.post(
        "/api/projects/proj-ID/tasks/task-ID/runs/run-ID/run_repair",
        json=input_data.model_dump(),
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Model name and provider must be specified."

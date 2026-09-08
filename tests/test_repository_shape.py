import ast
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
AZURE_YAML = ROOT / "azure.yaml"


def _agent_service() -> tuple[str, dict]:
    document = yaml.safe_load(AZURE_YAML.read_text(encoding="utf-8"))
    services = document.get("services", {})
    hosted = [
        (name, service)
        for name, service in services.items()
        if service.get("host") == "azure.ai.agent"
    ]
    assert len(hosted) == 1
    return hosted[0]


def test_hosted_agent_contract() -> None:
    _, service = _agent_service()
    assert service["project"] == "src/agent-framework-agent-basic-responses"
    assert service["codeConfiguration"] == {
        "runtime": "python_3_13",
        "entryPoint": "main.py",
    }
    assert service["protocols"] == [{"protocol": "responses", "version": "2.0.0"}]

    project = ROOT / service["project"]
    assert project.is_dir()
    assert (project / service["codeConfiguration"]["entryPoint"]).is_file()


def test_main_uses_expected_foundry_types_without_importing_it() -> None:
    _, service = _agent_service()
    source_path = (
        ROOT
        / service["project"]
        / service["codeConfiguration"]["entryPoint"]
    )
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(source_path))
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    assert {
        "Agent",
        "FoundryChatClient",
        "ResponsesHostServer",
        "DefaultAzureCredential",
    } <= imported

    lowered = source.lower()
    assert "ghp_" not in lowered
    assert "github_pat_" not in lowered
    assert "https://ai.azure.com/api/projects/" not in lowered


def test_sensitive_and_generated_files_are_ignored() -> None:
    patterns = {
        line.strip()
        for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    assert {
        ".env",
        ".azure/",
        ".foundry/results/",
        "*.pem",
        "*.key",
        "webhook*.secret",
    } <= patterns

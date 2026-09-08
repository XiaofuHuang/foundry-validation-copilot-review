from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
INSTRUCTIONS = ROOT / ".github/instructions/foundry-validation.instructions.md"


def _frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    _, raw, body = text.split("---", 2)
    return yaml.safe_load(raw), body


def test_review_path_instructions() -> None:
    instructions, instruction_body = _frontmatter(INSTRUCTIONS)
    assert instructions["applyTo"] == (
        "azure.yaml,src/**/*.py,src/**/Dockerfile,"
        "src/**/requirements.txt,foundry/**"
    )
    combined = instruction_body.lower()
    for operation in (
        "execute",
        "install",
        "authenticate",
        "query azure",
        "deploy",
        "invoke",
    ):
        assert operation in combined
    assert "untrusted evidence" in combined
    assert "must not claim certification or enforcement" in combined
    for topic in (
        "foundry toolbox",
        "tracing",
        "agent framework",
        "fabricate success",
        "platform-managed",
        "protocol",
    ):
        assert topic in combined
    assert not (ROOT / ".github/skills").exists()

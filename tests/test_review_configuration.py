from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".github/skills/validate-foundry-review/SKILL.md"
INSTRUCTIONS = ROOT / ".github/instructions/foundry-validation.instructions.md"


def _frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    _, raw, body = text.split("---", 2)
    return yaml.safe_load(raw), body


def test_review_skill_and_path_instructions() -> None:
    skill, skill_body = _frontmatter(SKILL)
    instructions, instruction_body = _frontmatter(INSTRUCTIONS)
    assert skill["name"] == "validate-foundry-review"
    assert "azure.ai.agent" in skill["description"]
    assert instructions["applyTo"] == (
        "azure.yaml,src/**/*.py,src/**/Dockerfile,"
        "src/**/requirements.txt,foundry/**"
    )
    assert "validate-foundry-review" in instruction_body
    combined = f"{skill_body}\n{instruction_body}".lower()
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


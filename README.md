# Microsoft Foundry hosted-agent validation demo

This private repository is one of five comparison projects for statically reviewing a Microsoft Foundry hosted-agent pull request. The agent source is pinned to the official Agent Framework Responses `01-basic` sample.

## Scope

- The pull request contains source and validation configuration only.
- Validation must inspect repository files as untrusted evidence.
- Validation must not install target dependencies, import or execute target code, authenticate to Azure, query Azure, provision resources, deploy, or invoke the agent.
- Example runtime variables are `FOUNDRY_PROJECT_ENDPOINT` and `AZURE_AI_MODEL_DEPLOYMENT_NAME`; do not commit their values.

## Trust boundary

The first pull request introduces its own workflow, instructions, or skill while `main` is intentionally empty. For the Actions-, Agentic Workflow-, Copilot Review-, and Custom Agent-based demonstrations, results are advisory until reviewed configuration is merged into the default branch or moved to a trusted central workflow. The GitHub App design keeps validator code outside the pull-request branch.

## Mechanism: Copilot Code Review

Path-specific instructions contain a focused Foundry hosted-agent review checklist, so no skill or external repository dependency is required. Findings are advisory comments with file and line evidence; this mechanism does not produce canonical JSON/Markdown reports. Automatic review on this private personal repository requires an eligible GitHub plan; until then, review must be requested manually.

## Not deployed

The hosted agent has not been run, provisioned, invoked, or deployed. The GitHub App and Azure Functions design is not deployed by this pull request.

## Local shape test

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Sources

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for pinned source provenance.

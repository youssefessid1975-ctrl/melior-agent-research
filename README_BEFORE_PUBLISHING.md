# Publish Melior to GitHub

This package presents Melior as a **research engineering portfolio project**: a reviewer-facing narrative, historical implementation results, and a new runnable companion experiment. It does not contain your full original private source tree.

## Quick publishing steps

1. Read the top-level `README.md` and check the wording accurately reflects your role.
2. Run the demonstration and tests:

```bash
python -m unittest discover -s tests -v
python -m experiments.public_demo
```

3. Create an empty public GitHub repository named `melior-agent-research`.
4. Copy the **contents** of this folder into it; then run:

```bash
git init -b main
git add .
git diff --cached --stat
git commit -m "Publish Melior research engineering portfolio"
git remote add origin https://github.com/YOUR_USERNAME/melior-agent-research.git
git push -u origin main
```

5. Add the repo link to the **Melior** entry on your ETH CV. Pin the repo on your GitHub profile.
6. For an even stronger reviewable technical record, release selected sanitized modules and original checkpoint evidence following [`docs/real-code-release-plan.md`](docs/real-code-release-plan.md).

## Private-file check before every push

Never include API keys, `.env` files, raw private provider traces, hidden benchmark solutions, private credentials, sensitive customer or cofounder material, or code you lack rights to redistribute. The historical metrics should remain attached to their actual dated checkpoint and experimental scope; public companion-demo numbers are separate.

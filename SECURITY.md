# Security / disclosure boundaries

This public repo is intentionally minimal. Do **not** upload private AI prompts, provider requests/responses, model keys, agent trajectories, local machine paths, access tokens, third-party data, private benchmark oracles, or unreviewed logs.

Do not copy the full historical `.git` directory from the private repository: secret content may remain in old commits even when later deleted. Make a fresh repository with a clean history and individually reviewed files.

The sample simulator makes **no network calls** and does not run model-generated shell commands. It is not a hardened production sandbox.

Before publishing real source, review authorization boundaries, package licenses, attribution, private cofounder work and all retained evidence. Check ignored files as well as staged diffs.

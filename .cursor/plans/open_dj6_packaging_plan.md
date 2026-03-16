# Packaging GLadMe into `open-dj6`

To give your friend a ready-to-use version of his **GLadMe Framework**, we can package the Claude Code setup directly into the MinuteWork `open-dj6` open-source template. 

This gives him a working Django/React application that already has the agentic continuous learning loop pre-configured and ready to run.

## Why This Approach? (The Architectural Choice)
Instead of trying to replicate the complex features of Cursor or Anthropic's Claude Code (like file parsing, context management, semantic search, and git operations), this approach treats `open-dj6` as a structural "template" or "substrate". 

By using Claude Code simply as an underlying *engine* that acts on the `open-dj6` template, we avoid rebuilding the wheel. Gautam Lab can focus on defining the `Goal`, building the logic, and writing the test `Metric`, while offloading the heavy lifting of Coder/Reviewer agent interactions to a specialized, state-of-the-art CLI tool that already solves those problems natively.

## Option A: Project-Local Installation (The Sandbox)
This packages the skill directly into the `open-dj6` directory. It is perfect for giving him a locked-down, guaranteed-to-work sandbox.
1. Create the `.claude/skills` directory in the root of `open-dj6`.
2. Copy the `autoresearch` skill files directly into `open-dj6/.claude/skills/autoresearch/`.
3. Commit this to the git repository.

*Now, anytime someone opens the `open-dj6` repo and runs `claude`, the `/autoresearch` command is natively available for that specific project.*

## Option B: Global Installation (The Lab-Wide Setup)
If he wants to use the GLadMe loop across *all* of his lab's diverse projects (e.g., the deer re-identification system or the smart irrigation system) instead of just the Django template, he should install the skill globally:

```bash
cp -r autoresearch/skills/autoresearch ~/.claude/skills/autoresearch
```

*Now, he can open his terminal in ANY project folder on his machine, type `claude`, and use the `/autoresearch` continuous learning loop.*

## Establishing a GLadMe "Verify" Metric
The Autoresearch loop requires a **mechanical verification metric**. If he uses the project-local `open-dj6` sandbox, we can pre-configure a few commands that act as the "Monitoring Agent" for his experiments out of the box.

We can highlight these in his documentation:
- **Backend Quality Metric:** `pytest` (e.g., trying to write tests or fix logic in Django).
- **Frontend Quality Metric:** `npm run tsc` (e.g., eliminating TypeScript errors in React) or `npm run build` (checking bundle size/success).

## Step 3: Enforcing Contracts to Prevent AI Drift
One of the biggest risks of autonomous AI loops is "code drift"—where the AI writes functional code that violates your specific architectural patterns, security rules, or design systems. 

To solve this, Gautam Lab can use **Context Injections** within the loop. 

In `open-dj6`, we have a deep `.cursor/commands/context.md` file that teaches the AI how to audit the architecture (e.g., `show_engine_flow`, `show_db_flow`, `show_network_flow`). 

Your friend can pass these context files directly into the `/autoresearch` prompt to serve as **strict guardrails** for the Coder/Reviewer agents.

Example of a highly constrained prompt invoking the `.cursor/commands/context.md` protocols:
```text
/autoresearch
Goal: Refactor the ChatSessionService to use the unified WebhookProvider. You MUST follow the exact architectural rules defined here: @.cursor/commands/context.md and regenerate backend docs if you add a new service.
Scope: web/services/chat.py, common/services/webhooks.py
Metric: Pass rate (higher is better)
Verify: pytest tests/test_chat_session.py
```
This forces the AI to read your architectural laws *before* entering Phase 1 of the action loop, guaranteeing that every single iteration it tries complies with Gautam Lab protocol.

## Update the `README.md`
We will add a dedicated "Agentic Development (GLadMe)" section to the `open-dj6` README. It will instruct him on how to test the loop immediately with these architectural guardrails in place.

Example addition to the README:
```markdown
## GLadMe Agentic Loop

This repository comes pre-configured with the **GLadMe Autoresearch Skill** for Claude Code.

1. Ensure Claude Code is installed (`npm i -g @anthropic-ai/claude-code`).
2. Start the continuous learning loop by running `claude` and invoking the skill:

```text
/autoresearch
Goal: Increase python test coverage while adhering to our architecture protocols detailed in @.cursor/commands/context.md
Scope: web/**/*.py, tests/**/*.py
Metric: Pass rate (higher is better)
Verify: pytest
```
Claude will iteratively modify code, run `pytest`, keep passing code in compliance with strict Django rules, and auto-revert failed/non-compliant code.
```

## Step 4: Zip and Deliver
Once these three things are added (the `.claude/skills/autoresearch` folder, the test scripts, and the README update), the `open-dj6` repository *is* the GLadMe framework. You can push it to a branch or send him the zipped folder, and he can start doing agentic development on day one.

> Entry point for the `/dev-flow` slash command — loads the instructions and the workflow, then starts execution.

Load the following rules files:

- `.claude/rules/general/instructions.md`
- `.claude/rules/general/development-workflow.md`
- `.claude/.env`

If any file can't be loaded, stop execution and report it.

Specific rules for this command:

- Always use git worktree inside the `.claude/worktrees` directory to isolate the agent's development environment.
- Never alter the main branch directly (`{{ GIT_MAIN_BRANCH }}`).
- Do not perform automatic merge/rebase at the end of a workflow. Wait for explicit human approval.

Strictly follow these rules. Then begin executing the workflow starting from **Step 1 — PLANNING**.

You can get the value for `{{ * }}` placeholders in the markdown files, for example, like `{{ GIT_MAIN_BRANCH }}` or `{{ DEV_FLOW_MAX_ITERATIONS }}`, etc, in the `.claude/.env` file.

Behavior:

- Be concise in outputs.
- Do not generate unnecessary explanations.
- Focus on completing the task.
- Log each step being executed.

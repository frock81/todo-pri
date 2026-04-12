# Development Workflow

> Canonical and complete development workflow specification — agents, steps, iterations, and success/failure criteria.

## Execution Protocol

### 1. PLANNING

Agent: `planner`

Responsibilities:

- Analyze requirements
- Create a clear technical specification

Output:

- `dev-flow/specs.md`

---

### 2. APPROVAL CHECKPOINT

Pause execution so the full technical specification can be reviewed and approved.

Granting authorization to proceed is **not your responsibility** — it must be given by a human reviewer.

Once approved, you will receive authorization to begin executing the main subflow iterations.

---

### 3. TEST DESIGN (before coding)

Agent: `*_test_designer`

Responsibilities:

- Create a test plan based on `dev-flow/specs.md`

Output:

- `dev-flow/test_plan.md`

---

### 4. IMPLEMENTATION

Agents:

- `*_api_coder`
- `*_cli_coder`
- `*_service_coder`
- `*_lib_coder`
- `*_utils_coder`

Responsibilities:

- Implement code based on `dev-flow/test_plan.md`
- Write/update code under the `/src` directory

Rules:

- Follow the coding standards defined in `.claude/rules/coding-standards.md`

---

### 5. REVIEW

Agent: `*_reviewer` (fastapi, frontend, shell_script)

Responsibilities:

- Improve readability
- Ensure separation of concerns

Constraints:

- Must not alter behavior

Output:

- `dev-flow/review_notes.md`

---

### 6. TESTING

Agent: `*_test_engineer` (fastapi, frontend, shell_script)

Responsibilities:

- Write tests
- Cover edge cases
- Generate/update tests under the `/tests` directory

---

### 7. MERGE/REBASE CHECKPOINT

Pause execution for a final review before merging or rebasing into the main branch (`{{ GIT_MAIN_BRANCH }}`).

Granting authorization to merge/rebase is **not your responsibility** — it must be given by a human reviewer.

Once approved, you will be instructed to perform the final merge/rebase. Follow the commit message conventions defined in `.claude/rules/techs/git-commit-messages.md`. Do not include workflow tracking files (`dev-flow/*`) in the commit.

After the merge/rebase is complete, remove the git worktree that was created. The workflow is then finished.

---

## Iteration Control

- Maximum iterations per execution: **{{ DEV_FLOW_MAX_ITERATIONS }}**
- Track the current iteration count in `dev-flow/iteration.txt` inside the worktree
- Initial value: `1`
- Increment after each full workflow cycle (steps 3–6)

### Validation (after each iteration)

- Run the full test suite
- If **all tests pass** → stop (success)
- If **tests fail** → increment counter and proceed to next iteration

### Failure Handling

If `iteration == {{ DEV_FLOW_MAX_ITERATIONS }}` and tests still fail:

- Stop execution
- Generate `dev-flow/failure_report.md` inside the worktree

The failure report must include:

- Failing tests
- Suspected root causes
- Files involved
- Suggested fixes

---

## Execution Rules

- Do not skip steps
- Each agent must respect its defined scope

---

## Success Criteria

All tests must pass (`pytest exit code == 0`).

---

## Shared Memory

Files used as shared context across agents:

| File                       | Purpose                       |
| -------------------------- | ----------------------------- |
| `dev-flow/specs.md`        | Technical specification       |
| `dev-flow/test_plan.md`    | Test plan                     |
| `dev-flow/review_notes.md` | Review feedback               |
| `dev-flow/memory.md`       | Worktree name and branch name |
| `dev-flow/iteration.txt`   | Current iteration counter     |

Rules:

- Always read the relevant files before executing a step
- Update only when there is new content to record
- These files must **not** be committed

---

## Output Contracts

Each agent must strictly follow its defined output format.

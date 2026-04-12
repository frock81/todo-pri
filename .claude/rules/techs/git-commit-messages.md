# Git Commit Messages

## General Instructions

- Write commit messages in English (US).
- Focus more on the "why" and "how" than on the "what", but include the "what" as well.

## Format

Follow the **Conventional Commits** standard: use a **50-character summary line** in the imperative mood (e.g., "add", not "adds" or "added"), separated by a blank line from an **optional body wrapped at 72 characters**. **Use types** such as feat:, fix:, or docs: for clarity, and use ! to indicate breaking changes.

**Standard commit message structure**:

- **Header**: <type>(<optional scope>): <description> (50 characters max)
- **Body**: (Optional) Explain what changed and why, not how. Wrap at 72 characters.
- **Footer**: (Optional) Reference issue IDs (e.g., Closes #123) or BREAKING CHANGE.

## Common Commit Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation-only changes
- **style**: Formatting, missing semicolons, etc. (no code changes)
- **refactor**: Code restructuring without adding features or fixing bugs
- **perf**: Performance improvement
- **chore**: Changes to the build process or auxiliary tools

## Example

```text
feat(auth): validate JWT token

Implement JWT validation to protect API endpoints and
improve session management, replacing legacy session
storage.

Closes #15
```

## Best Practices

- **Imperative mood**: Use "add" instead of "adds" or "added".
- **No period**: Do not end the subject line with a period.
- **Capitalization**: Capitalize only the first word of the subject line.
- **Blank line**: Always separate the subject from the body with a blank line.

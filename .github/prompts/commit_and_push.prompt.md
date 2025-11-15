---
description: Commit and push changes with conventional commit messages. Use docs=true to include documentation updates.
argument-hint: "[docs=true to update docs]"
agent: agent
---

# Commit and Push Changes

Analyze the current git changes and create a conventional commit following the project's commit standards.

## Instructions

1. **Check for staged/unstaged changes**: Review what files have been modified
2. **Analyze the changes**: Understand what was changed and why
3. **Review commit standards**: Check `commitlint.config.js` for valid types and scopes
4. **Update documentation** (only if `${input:docs}` is set to `true`):
   - Search for relevant documentation files using `grep_search` or `semantic_search`
   - Determine which docs need updates based on changes:
     - RPi implementation changes → Update `docs/rpi-setup.md`
     - Android app changes → Update `docs/android-setup.md`
     - iOS app changes → Update `docs/ios-setup.md`
     - Architectural changes → Update `docs/architecture.md`
     - Major project changes → Update main `README.md`
     - New workflows or tools → Update relevant platform guide
   - Update all affected documentation files with the changes
   - Include documentation updates in the same commit as code changes
5. **Determine commit type**: Must match valid types in `commitlint.config.js`
6. **Select appropriate scope** (optional but recommended): Must match valid scopes in `commitlint.config.js` if provided
7. **Write commit message** in this format:
   ```
   <type>[optional scope]: <description>

   [optional body explaining the change]

   [optional footer(s)]
   ```
8. **Stage all changes** (including documentation updates if applicable)
9. **Create the commit** with the properly formatted message
10. **Push to remote** repository

## Commit Standards

**IMPORTANT**: Always check `commitlint.config.js` for the authoritative list of valid types and scopes.

**IMPORTANT**: Ensure that the line length is never larger than `'header-max-length' from `commitlint.config.js`

### Valid Commit Types (from commitlint.config.js)

- `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `build`

### Valid Scopes (from commitlint.config.js - optional)

- Platform-specific: `rpi`, `android`, `ios`
- Component-specific: `docs`, `config`, `deps`, `ci`

### Examples

- `feat(rpi): add WiFi Aware service publisher implementation`
- `feat(android): implement WiFi Aware discovery session`
- `feat(ios): add WiFi Aware subscriber with data path`
- `fix(android): resolve permission request timing issue`
- `docs(architecture): add message protocol specifications`
- `docs: update quick start guide` (scope optional)
- `chore(deps): update gradle dependencies`
- `ci: add automated build workflow` (no scope needed)
- `build(android): configure proguard rules for release`

## Requirements

- Description should be lowercase, imperative mood ("add" not "added" or "adds")
- Keep entire header (type + scope + description) under 100 characters (per commitlint.config.js)
- If changes span multiple areas, consider separate commits
- Use body to explain "why" not "what" (code shows what)
- Reference issues/PRs in footer if applicable

## Example Workflow

After analyzing the changes, execute:

```bash
git add -A
git commit -m "<type>(scope): description"
git push origin <branch-name>
```

## Usage Examples

```bash
# Standard commit without documentation updates
/commit-and-push

# Commit with documentation analysis and updates
/commit-and-push docs=true
```

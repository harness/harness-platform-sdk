## Task: Determine Next Version

**Repository Context:** This is a Python module repository (`harness-platform-sdk`) published to PyPI. Source code is located in `src/harness_platform_sdk/`. Versioning follows [Semantic Versioning](https://semver.org/) with tags in format `v{MAJOR}.{MINOR}.{PATCH}`.

Inputs: most recent tag (from `git describe --tags --abbrev=0`), diff range `<most-recent-tag>..HEAD`

### Steps

1. **Partition changed files into substantive and exempt.** From the diff range, collect all changed files and partition them using the exempt path set defined in "Rule: Infrastructure File Exemption" below.

2. **If substantive set is empty,** classify as **Patch** (no code changes; infrastructure/docs updates only) and skip to step 5.

3. **If substantive set is non-empty, analyze module changes.** Examine only `src/harness_platform_sdk/` changes:
    - **Inspect for breaking changes:** Removed public classes, removed/renamed public functions, incompatible signature changes
    - **Inspect for new features:** New public classes, new public functions, new submodules
    - **Inspect for bugfixes/refactors:** Bugfixes, internal refactors, optimizations, documentation strings

4. **Classify the bump using these rules, in order**:
    - **Major** — Any breaking change to public API:
      - Removed or renamed public class/function from `src/harness_platform_sdk/` top-level or public submodules
      - Incompatible changes to function signatures, return types, or exceptions for public APIs
      - Changes that would require users to modify their code when upgrading
    - **Minor** — New features or non-breaking additions:
      - New public classes, functions, or public APIs in `src/harness_platform_sdk/`
      - New public submodules (e.g., new `*_api` module)
      - Additions that extend functionality without removing or changing existing public APIs
    - **Patch** — Bugfixes, refactors, and internal changes:
      - Bugfixes in existing code
      - Internal refactors, optimizations, or code cleanup
      - Documentation string updates
      - Test additions or modifications
      - Infrastructure, tooling, or deployment changes
      - Changes only to exempt paths (README, docs, CI/CD, scripts, etc.)

5. **Compute the next version** by bumping the appropriate segment of the most recent tag (semver: `MAJOR.MINOR.PATCH`), resetting lower segments to 0:
    - Major bump: `v1.0.0` → `v2.0.0`
    - Minor bump: `v1.0.0` → `v1.1.0`
    - Patch bump: `v1.0.0` → `v1.0.1`

6. **On Major classification**, halt and request confirmation rather than proceeding automatically. Output: the classification reasoning, the specific breaking changes identified, and an explicit prompt for the user/approver to confirm the Major bump before the pipeline continues.

7. **Emit the result** (current tag, classification, next version) as pipeline output variables for downstream steps (changelog, tagging) to consume.

### Rule: Infrastructure File Exemption

**Define an exempt path set** (repo-root-relative, matched by prefix or exact name). These files do not affect version bumps—changes to them are always considered Patch-level:

**Documentation & Configuration:**
- README*, CHANGELOG.md, LICENSE, CONTRIBUTING.md, .editorconfig, .gitignore

**Development Tools & CI/CD:**
- mise.toml, Makefile, pyproject.toml (only [tool.*] sections, not [project]version)
- .ai/, .harness/, .devcontainer/, .github/
- scripts/ (development and tooling scripts, not SDK source code)
- templates/ (code generation templates, not SDK source)

**Test Infrastructure:**
- tests/ (all test files, test fixtures, and test infrastructure)

**Documentation Generation:**
- docs/ (generated documentation)
- DOCKERHUB_OVERVIEW.md, CONTRIBUTING_NEW_CLASSES.md (supplementary docs)

**Infrastructure & Build:**
- build/, dist/ (build artifacts)
- Dockerfile*, *.local.toml, os_packages.txt

**Apply before classification, not after:**

1. From the full changed-file list, partition into two sets: `exempt` (matches the list above) and `substantive` (everything else).
   - Note: `pyproject.toml` is exempt for changes to `[tool.*]` sections (e.g., build config, formatting rules), but changes to `[project]` section (e.g., `version`, `dependencies`, `classifiers`) are **substantive** because they reflect SDK metadata.

2. Run the Major/Minor/Patch classification using **only the `substantive` set**. Exempt files are invisible to the classification logic.

3. **If `substantive` is empty** (i.e., every changed file matched the exempt list), classify the release as **Patch**, regardless of how many exempt files changed or how widely they're spread (e.g., touching `.harness/`, `README.md`, `scripts/`, and `.editorconfig` together is still Patch).

4. **If `substantive` is non-empty**, classify normally based on `substantive` alone. Ignore exempt files entirely when computing the bump (they neither upgrade nor downgrade the result).

5. **Example substantive changes:**
   - Changes to `src/harness_platform_sdk/` (module source code)
   - Changes to `src/harness_platform_sdk/__init__.py` (public API, `__version__`)
   - Changes to `pyproject.toml` `[project]` section (metadata, dependencies)

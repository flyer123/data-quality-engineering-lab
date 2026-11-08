# Data Quality & Observability Engineering Lab

A compact, production-oriented data quality and observability project built around the Olist dataset. The lab demonstrates practical data-quality engineering, Python testing, data reliability, incident investigation, and—later—quality checks integrated into a data pipeline.

**Planned duration:** 12 weeks  
**Target effort:** approximately 4–6 hours per week  
**Current position:** Week 3 — validation runner implementation and quality checks completed; documentation review and commit remain.

---

## Project objectives

- Build reusable data-quality validation rules and an execution runner.
- Apply the framework to real Olist datasets and document dataset-specific expectations.
- Develop data-quality metrics and observability capabilities.
- Investigate data-quality incidents and write concise postmortems.
- Integrate quality checks into a pipeline in the final milestone.

Data quality is treated as an observability and reliability layer around a data pipeline, not merely as a final ETL step.

## Technology stack

- Python 3.13
- Pandas
- PostgreSQL
- pytest
- mypy
- Ruff
- Docker Compose (introduced in a later milestone)

The initial implementation is local. PostgreSQL persistence, Docker integration, and monitoring are deliberately postponed until the relevant milestones.

## Repository structure

```text
data-quality-engineering-lab/
├── README.md
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── docker-compose.yml
├── data/
│   ├── raw/
│   ├── curated/
│   └── broken/
├── sql/
│   ├── schema.sql
│   └── views.sql
├── src/
│   ├── ingestion/
│   ├── validation/
│   ├── metrics/
│   ├── monitoring/
│   └── incidents/
├── tests/
│   └── validation/
└── docs/
    ├── architecture.md
    ├── dataset_inventory.md
    ├── quality_dimensions.md
    ├── roadmap.md
    └── postmortems/
```

The tree represents the intended project layout; folders and components for later milestones may not yet contain implementation.

---

## Progress and 12-week plan

Use the checkboxes to track completion. A checked item means the work is implemented or completed; documentation and commit tasks are tracked separately where applicable.

### M0 — Foundation (Week 1)

- [x] Establish the repository and initial project structure.
- [x] Configure the Python 3.13 virtual environment and project package.
- [x] Configure the initial development and quality-tooling environment.
- [x] Establish the Olist-based project scope and roadmap.

### M1 — Validation engine (Weeks 2–4)

#### Week 2 — Generic validation rules

- [x] Define `ValidationResult` with rule, dataset, column, pass/fail, failed-row count, and message fields.
- [x] Define the abstract `ValidationRule` interface.
- [x] Implement `NotNullRule`.
- [x] Implement `RangeRule` with inclusive boundaries and separate NULL handling.
- [x] Implement `AcceptedValuesRule` with NULL values ignored and empty configuration rejected.
- [x] Implement `RegexRule` with NULL values ignored and full-string pattern matching.
- [x] Add unit tests for the four rule types (21 tests reported passing).

#### Week 3 — Validation runner and quality gate

- [x] Implement `ValidationRunner` as a concrete orchestration class.
- [x] Accept an ordered collection of configured `ValidationRule` instances.
- [x] Execute every configured rule and return ordered `ValidationResult` objects.
- [x] Reject an empty rule collection with `ValueError`.
- [x] Ensure a failed validation result does not stop later rules from running.
- [x] Ensure each execution returns a fresh results list.
- [x] Test runner reuse with separate DataFrames.
- [x] Test that validation does not mutate the input DataFrame (`test_dataframe_integrity`).
- [x] Run the full pytest suite successfully (reported by the user).
- [x] Run mypy successfully (reported by the user).
- [x] Run Ruff successfully (reported by the user).
- [x] Update `docs/architecture.md` to describe the runner and its relationship to `ValidationRule` and `ValidationResult`.
- [x] Review the intended changes with `git status` and `git diff`.
- [x] Commit the Week 3 changes.

**Week 3 status:** implementation and quality checks are complete. Close the milestone after the architecture documentation, final diff review, and commit are complete.

#### Week 4 — Apply validation to Olist data

- [ ] Inspect and document the schemas and assumptions for the selected Olist tables.
- [ ] Identify dataset-specific quality expectations.
- [ ] Select relevant completeness, validity, range, accepted-value, and referential-integrity checks.
- [ ] Apply the existing generic validation framework to real datasets.
- [ ] Review and document the validation outcomes.

### M2 — Observability (Weeks 5–7)

- [ ] Define the quality metrics needed to describe dataset health.
- [ ] Implement the planned metrics layer.
- [ ] Develop the planned monitoring and observability functionality.
- [ ] Review how validation outcomes and quality metrics can support reliability decisions.

### M3 — Data-quality incidents (Weeks 8–10)

- [ ] Prepare representative data-quality failure scenarios.
- [ ] Investigate failures using validation results and quality evidence.
- [ ] Document causes, impact, resolution, and prevention in postmortems.
- [ ] Review the incident workflow and identify reliability improvements.

### M4 — Production integration and capstone (Weeks 11–12)

- [ ] Integrate quality checks into a data-pipeline workflow.
- [ ] Introduce the planned PostgreSQL persistence and Docker Compose components where appropriate.
- [ ] Demonstrate the validation, observability, and incident capabilities in an end-to-end capstone.
- [ ] Document the final architecture, operating assumptions, and project outcomes.

The later-milestone checklists are intentionally high-level. Break them into concrete tasks when each milestone begins; do not introduce infrastructure before it is needed.

---

## Current validation design

### Rule responsibilities

Each rule is configured with its target column and rule-specific parameters, then implements:

```text
validate(data: pd.DataFrame, dataset: str) -> ValidationResult
```

The individual rules validate supplied data. They do not load CSV files, connect to databases, persist results, print reports, calculate historical metrics, or send alerts.

### Runner responsibilities and contract

`ValidationRunner` owns an ordered collection of configured `ValidationRule` objects. Its `run_validation(data, dataset)` method executes each rule and returns a `list[ValidationResult]`.

Current design decisions:

- Depend on the `ValidationRule` interface, not concrete rule classes.
- Pass the DataFrame into each execution; do not retain it as runner state.
- Create a new local results list for each execution.
- Preserve configured rule order.
- Continue after a rule returns `passed=False`.
- Allow unexpected rule-execution exceptions to propagate.
- Do not mutate the input DataFrame.
- Keep persistence, logging, metrics, monitoring, parallel execution, and exception recovery outside the current runner scope.

### Current validation package

```text
src/validation/
├── __init__.py
├── base.py
├── result.py
├── validation_runner.py
└── rules/
    ├── __init__.py
    ├── not_null.py
    ├── range.py
    ├── accepted_values.py
    └── regex.py
```

### Current validation tests

```text
tests/validation/
├── test_accepted.py
├── test_not_null.py
├── test_range.py
├── test_regex.py
└── test_runner.py
```

---

## Development and quality checks

Run commands from the repository root, using the project's active Python 3.13 virtual environment:

```bash
python -m pytest -v
python -m mypy src
python -m ruff check .
```

Optional formatting check, if Ruff is configured as the project formatter:

```bash
python -m ruff format --check .
```

Do not weaken tests or disable checks merely to obtain a passing result. Investigate and fix the underlying issue.

## Week 3 — final review and commit

After updating `docs/architecture.md` and placing this README in the repository root, review the changes:

```bash
git status --short
git diff --check
git diff
```

Stage only the files that belong to this milestone. Adjust the paths if your actual changed-file list differs:

```bash
git add README.md docs/architecture.md \
  src/validation/validation_runner.py \
  tests/validation/test_runner.py
```

Inspect exactly what is staged, then commit:

```bash
git diff --cached --check
git diff --cached
git commit -m "Complete validation runner and tests"
git status --short
```

The final `git status --short` should be empty if all intended changes have been committed and there are no unrelated working-tree changes. Do not stage unrelated files just to make the working tree clean.

---

## Learning and implementation approach

- Implement the code and tests yourself; use the project requirements and contracts as guidance.
- Work incrementally: implement, test, review, then proceed.
- Prefer focused code reviews and explanations of design trade-offs over replacement implementations.
- Avoid unnecessary abstractions and infrastructure.
- Keep generic validation mechanics stable unless applying them to real data reveals a concrete deficiency.

## Reading reference

The project is partly grounded in *Data Quality Fundamentals: A Practitioner’s Guide to Building Trustworthy Data Pipelines* by Barr Moses, Lior Gavish, and Molly Vorwerck (O’Reilly, 2022). The planned reading target is approximately 25–35 pages per week. Verify chapter references before relying on specific chapter numbers.
# Referee 2 — Pre-Flight Protocol

Before writing any replication script, complete this pre-flight checklist for each target language. The goal is to catch environment and data-loading problems *before* investing effort in full replication code.

---

## Step 1: Plan

Read the author's code end-to-end and answer:

1. **What packages/libraries are needed?** List every package the replication will require (e.g., `fixest` in R, `linearmodels` in Python).
2. **What data formats are used?** (`.csv`, `.parquet`, `.rds`, `.dta`, etc.) — will Python be able to read them?
3. **What econometric features are needed?** (clustered SEs, high-dimensional FEs, IV, event studies, etc.) — which package in the target language provides them?
4. **Are there any known cross-language pitfalls?** (e.g., default NA handling differs between R and Python — R keeps NAs in many operations, Python/pandas drops them)

Write this plan as a brief checklist in `code/replication/preflight_notes.md` before touching any code.

---

## Step 2: Environment Setup

### Python (mandatory — always use a venv)

```bash
cd <project_root>
python3 -m venv .venv
source .venv/bin/activate
pip install <packages from Step 1>
```

- If the project already has a `.venv/`, activate it and check installed packages
- If `pip install` fails for any package, diagnose and resolve *now* — do not proceed

### R

```r
# Check that required packages are installed
required <- c("fixest", "data.table", "haven", ...)
missing <- required[!sapply(required, requireNamespace, quietly = TRUE)]
if (length(missing) > 0) install.packages(missing)
```

---

## Step 3: Minimal Working Example (MWE)

For each replication language, write a short script (~20 lines) that:

1. Loads the main analysis dataset
2. Prints dimensions (rows x columns) — must match the author's data
3. Prints summary stats for the outcome variable and main treatment variable — spot-check against the author's
4. Runs one trivial OLS regression (outcome ~ treatment, no FEs, no clustering)
5. Prints the coefficient and standard error

**Name:** `code/replication/referee2_preflight_mwe.py` (and `.R`)

**Run it.** If it fails, fix the problem before proceeding. Common failures:

| Failure | Likely cause |
|---------|-------------|
| `ModuleNotFoundError` | venv not activated or package not installed |
| Wrong row count | Data loading issue (encoding, delimiter, missing value parsing) |
| Cannot read `.dta` | Need `pyreadstat` (Python) or `haven` (R) |
| Cannot read `.rds` | Only R can read `.rds` — need to export to `.csv`/`.dta` first |
| Different summary stats | Different NA handling — investigate before proceeding |

**Only proceed to full replication scripts once all MWEs pass.**

---

## Step 4: Write Replication Scripts

Now write the full replication scripts as described in Audit 2 of the main skill. You have confidence that:

- The environment works
- Packages are installed
- Data loads correctly
- Basic operations produce sensible output

This avoids the failure mode of writing 200 lines of replication code that crashes on line 3 because of a missing package or venv issue.

---

## Cleanup

- Keep `preflight_notes.md` and the MWE scripts — they document that the environment was validated
- The MWE scripts serve as a minimal reproducibility check that others can run quickly

# Empirical Correctness Checklist

Shared rubric for auditing empirical research code. This is the **single source of
truth** for the three correctness domains below; it is consumed by the
`referee2` skill (whole-project audit) and the `code-audit` skill (single-file diagnostic). It holds only the *rubric* — no severity formats, output templates, or
skill-specific procedure. Each consuming skill wraps these checks in its own framing.

---

## 1. Data integrity

- **Duplicates** — is there a check for duplicate rows on the panel/unit identifier
  (and on merge keys)?
- **Missing values** — are NAs handled *explicitly* (not silently dropped)? Is the
  chosen treatment (drop / impute / keep) documented and justified?
- **Panel structure** — is the panel balanced or unbalanced, and is this acknowledged?
- **Merges / joins** — is each merge validated?
  - Join type (left / inner / full) intentional and correct for the goal?
  - Cardinality (one-to-one vs many-to-one) documented?
  - Post-merge row-count check — did the merge inflate or drop observations unexpectedly?
  - Are unmatched observations inspected rather than silently discarded?
- **Variable construction** — do constructed variables (dummies, logs, interactions,
  lags) match their intended definitions? Is indexing / iteration correct (no
  off-by-one, no iteration over the wrong dimension)?
- **Filters / sample restrictions** — do `filter()` / `[condition]` statements actually
  implement the stated sample restrictions?
- **Selection** — are there sample-selection steps that could introduce bias?

---

## 2. Econometrics

- **Identification** — is the source of variation clearly stated and plausible, and is
  the identification strategy actually implemented in the code as described?
- **Estimating equation** — does the code estimate the specification the paper /
  documentation claims? Are the right functions used for the model (e.g. fixed-effects
  handling: `feols`/`felm` vs a plain `lm()`)?
- **Standard errors**
  - Clustered at the appropriate level? (Panel: at minimum the unit level.)
  - Enough clusters (>50 rule of thumb)? With few clusters, is a correction used
    (wild-cluster bootstrap)?
  - iid SEs on grouped / panel data → flag as likely incorrect.
  - Is heteroskedasticity addressed (robust SEs) where relevant?
- **Fixed effects** — consistent with the stated design; not collinear with treatment;
  absorbing what the design claims.
- **Controls** — any *bad controls* (variables themselves affected by treatment,
  post-treatment outcomes used as controls — Angrist & Pischke)?
- **Sample definition** — who is in the sample and why? Are restrictions justified and
  documented?
- **Difference-in-Differences** — is the parallel-trends assumption testable with this
  data, and is it tested (event-study plot / pre-treatment coefficients)? For staggered
  adoption, is a heterogeneity-robust estimator used (Sun & Abraham; Callaway &
  Sant'Anna; de Chaisemartin & D'Haultfœuille)? Vanilla TWFE on staggered timing → flag.
- **Instrumental variables** — is the first stage reported? Is the first-stage
  F-statistic checked (rule of thumb F > 10, or weak-IV-robust inference used)? Is the
  exclusion restriction discussed?
- **RCT / RD** — are balance tests shown? (RD: McCrary density test; bandwidth
  sensitivity.)
- **Winsorisation / trimming** — is it applied? At what level? Is it justified?
- **Magnitude plausibility** — is the effect size reasonable given priors (not
  mechanically zero, not implausibly large)?

---

## 3. Reproducibility & replication package

- **Seeds** — is a random seed set wherever a stochastic procedure is used?
- **Paths** — are all file paths relative to the project root? (Absolute paths like
  `/Users/...` or `C:\Users\...` are automatic failures.)
- **Dependencies** — are package/library versions recorded (`renv.lock`,
  `sessionInfo()`, `requirements.txt`, or equivalent)?
- **Execution order** — is there a clear order (numbered scripts, a master script, or a
  README) that runs the pipeline end-to-end from raw data to final output?
- **Folder structure** — clear separation of raw data, cleaned data, code, and output?
- **Naming** — are variables, datasets, and scripts named informatively
  (`treatment_intensity` not `x1`; `county_panel_2000_2020` not `data2`;
  `01_clean` / `02_estimate` for order)?
- **Intermediate outputs** — are they saved so individual scripts can be re-run without
  rebuilding everything?
- **Determinism** — does re-running the code produce identical outputs?

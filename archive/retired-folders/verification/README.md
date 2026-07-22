# Verification: the new bottleneck

> "Production used to be the bottleneck of research, now verification is." — Scott Cunningham

- Code, analyses, even drafts are now almost costless to produce. The agent is confident even when it's wrong, and rarely says "I'm not sure." So the work shifts from *producing* to *checking*.
- Agents can help here too — but verification only counts if it tests the real thing and survives:
  - **Save it as code.** A check worth running is worth keeping — a named, re-runnable script in the repo, not a number reported in chat with nothing behind it.
  - **Check against a known truth.** Monte Carlo simulation is the cleanest: simulate from parameters you chose, then confirm the estimator recovers them.
  - **Test ground truth, not your reconstruction.** Call the real function / the actual data, not a hand-rebuilt version of the rule you *think* it follows.

## Example

- [`example-recovery-check.R`](example-recovery-check.R) — a runnable recovery check: pick a true slope, simulate 2000 datasets, confirm the estimator is unbiased and its 95% CI is well calibrated. Swap in your own estimator and re-run; the truth doesn't move, so any drift is a red flag.

```
Rscript example-recovery-check.R
```

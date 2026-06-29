# example-recovery-check.R
#
# A worked example of the idea in the "Verification" part of the talk: when an agent
# writes or adapts an estimator, don't just trust it — check that it recovers a known
# truth. Here the "truth" is a slope we choose; we simulate data from it many times,
# run the estimator, and confirm (a) it's unbiased and (b) its 95% confidence interval
# covers the truth ~95% of the time. If you adapt an estimator, swap `estimate_slope()`
# for yours and re-run: the truth doesn't move, so any drift in the numbers below is a
# red flag.
#
# Base R only. Run with:  Rscript example-recovery-check.R

set.seed(20260629)        # reproducible — the whole point of a saved check

# --- ground truth (what the estimator must recover) ---
true_intercept <- 1.5
true_slope     <- 0.8
sigma          <- 2.0     # noise sd
n              <- 200     # observations per simulated dataset
n_sim          <- 2000    # number of simulated datasets

# --- the estimator under test ---
# Stand-in for "the function I adapted from a package". Replace its body with your own
# estimator; the check around it stays the same.
estimate_slope <- function(x, y) {
  fit <- lm(y ~ x)
  ci  <- confint(fit, "x", level = 0.95)
  list(
    slope    = unname(coef(fit)["x"]),
    ci_lower = ci[1],
    ci_upper = ci[2]
  )
}

# --- Monte Carlo loop ---
slopes  <- numeric(n_sim)
covered <- logical(n_sim)

for (i in seq_len(n_sim)) {
  x <- rnorm(n)
  y <- true_intercept + true_slope * x + rnorm(n, sd = sigma)
  est <- estimate_slope(x, y)
  slopes[i]  <- est$slope
  covered[i] <- (est$ci_lower <= true_slope) && (true_slope <= est$ci_upper)
}

# --- summarize ---
mean_slope <- mean(slopes)
bias       <- mean_slope - true_slope
coverage   <- mean(covered)

cat(sprintf("true slope          : %.4f\n", true_slope))
cat(sprintf("mean estimated slope: %.4f\n", mean_slope))
cat(sprintf("bias                : %.4f\n", bias))
cat(sprintf("95%% CI coverage     : %.3f  (target ~0.95)\n", coverage))

# --- pass/fail (tolerances scaled to the Monte Carlo error) ---
bias_ok     <- abs(bias) < 0.02
coverage_ok <- abs(coverage - 0.95) < 0.02

if (bias_ok && coverage_ok) {
  cat("\nPASS: estimator recovers the true slope and the CI is well calibrated.\n")
  quit(status = 0)
} else {
  cat("\nFAIL: recovery check failed — inspect the estimator.\n")
  if (!bias_ok)     cat("  - bias is larger than tolerance\n")
  if (!coverage_ok) cat("  - CI coverage is off the nominal 95%\n")
  quit(status = 1)
}

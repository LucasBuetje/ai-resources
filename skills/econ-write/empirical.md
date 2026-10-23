# EMPIRICAL WORK RULES

The previous section covered how to format tables and figures; this section covers what they should show and why -- the substance of an empirical paper is its identification and how its results are presented.

## Identification (Cochrane)
The three most important things: Identification, Identification, Identification.
1. Describe what economic mechanism caused dispersion in your right-hand variables
2. Describe what constitutes the error term (what else causes variation in Y?)
3. Explain why the error term is uncorrelated with X in economic terms
4. Explain the economics of why your instruments are valid
5. Describe the source of variation driving your estimates for every number you present

*For strategy-specific narrative structure (RCT, DiD/staggered, IV, RDD, Synthetic Control/DiD, Bunching, Shift-Share, Event Study, ML, Structural), see [identification-strategies.md](identification-strategies.md).*

## Results Presentation
- Start with the main result. No warmup exercises
- Follow with graphs and tables giving intuition
- Show how the main result is a robust feature of compelling stylized facts
- Follow with limited robustness checks (put most in web appendix)
- Give stylized facts in the data, not just estimates and p-values
- Explain economic significance, not just statistical significance -- with a large enough sample even a trivial effect becomes statistically significant, so a small p-value alone says little; the reader needs the magnitude relative to a benchmark to judge whether the effect matters
- Translate coefficients into meaningful units: dollars, percentage points, standard deviations, or equivalent policy benchmarks
- Compare your effect size to: (a) the mean of the dependent variable, (b) the effect of a well-known intervention, or (c) a policy-relevant threshold. Example: "The effect equals 40% of the black-white test score gap"
- For elasticities, state whether they are at the mean, at the median, or arc elasticities
- Back-of-envelope calculations are encouraged: "At the sample mean, this implies X additional dollars per household per year"
- Present results from most parsimonious to least parsimonious specification so the reader can see how the estimate moves as controls are added. Coefficient stability is suggestive -- not conclusive -- evidence against omitted-variable bias, and only when the added controls move the R-squared meaningfully (a coefficient can be stable yet biased if the controls explain little); report the R-squared changes, and ideally an Oster (2019) bound, rather than relying on stability alone

## Presenting Null Results
- A null result IS a result. Frame it as informative, not as failure
- Distinguish between "no effect" (precisely estimated zero) and "imprecisely estimated" (wide confidence intervals that include both zero and meaningful effects) -- failing to reject zero is not the same as establishing zero; only a tight interval that excludes economically meaningful effects is informative about absence
- Report confidence intervals alongside or instead of p-values -- "we can rule out effects larger than X"
- Discuss statistical power: was the study powered to detect economically meaningful effects?
- If pre-registered, emphasize that the null was not the result of specification searching
- Relate to prior literature: does the null contradict or refine previous findings?

## Common Empirical Mistakes
- R-squared interpretation depends on context: in cross-sectional micro regressions (wages, health), 0.1-0.3 is typical; an R-squared near 1 in a cross-section often signals a mechanical relationship -- you included "right shoes" to predict "left shoes" (Cochrane). In time-series or macro, high R-squared may be appropriate. Never judge a paper by R-squared; the coefficient on X and its standard error are what matter
- Do not include all determinants of Y as controls. A "bad control" is itself an outcome of the treatment, so conditioning on it does not cleanly remove a mechanism -- it compares non-comparable groups and induces selection bias. Education's effect works partly through industry, so controlling for industry does not isolate the "non-industry" return; it biases the estimate (Angrist and Pischke, Mostly Harmless Econometrics, Sec. 3.2.3)
- Do not confuse instruments with controls
- Do not claim causality without clearly explaining your identification strategy
- Do not ignore reverse causality
- Always address: (i) reverse causality, (ii) unobserved heterogeneity, (iii) measurement error

## Standard Errors and Inference
- Cluster standard errors at the level of treatment assignment (not the most granular unit), and state the clustering level explicitly -- when treatment is assigned and shocks are correlated within a cluster, observations are not independent, so treating them as independent understates standard errors and overstates significance
- With few clusters (rule of thumb: fewer than ~40, worse when cluster sizes are unbalanced), cluster-robust standard errors over-reject -- the cluster-robust variance estimator is consistent only as the number of clusters grows, so with few clusters it is biased down and standard critical values reject true nulls too often; use the wild cluster bootstrap (Cameron, Gelbach, and Miller 2008) or randomization inference instead
- For randomized or design-based settings, randomization (permutation) inference is often more credible than relying on asymptotic standard errors

## Heterogeneity Analysis
- Present heterogeneity results AFTER the main result, not before
- Pre-specify subgroups based on theory, not data mining
- Report the number of subgroups tested (multiple testing problem)
- Interpret magnitudes: "The effect is 3x larger for women" is more informative than "The interaction term is significant"
- Use visual presentation (forest plots or coefficient plots) when showing many subgroups

## Mechanisms
- Mechanisms sections should test specific channels, not speculate
- Structure as: (1) theory predicts mechanism M, (2) if M operates, we should observe X, (3) we test for X
- Distinguish between mediation analysis and suggestive evidence
- Be honest about what your data can and cannot identify mechanistically
- Do NOT list every possible mechanism without testing any of them

---

# MODERN EMPIRICAL PRACTICES

The rules above are timeless; the practices below are the credibility-revolution conventions that referees and data editors increasingly expect. Treat them as defaults, not optional extras.

## Pre-Registration and Pre-Analysis Plans
- If your study is pre-registered, state this in the introduction (it is a credibility asset)
- Clearly distinguish pre-specified analyses from exploratory analyses
- Report any deviations from the pre-analysis plan explicitly, with the reason for each
- Reference the pre-analysis plan (e.g., AEA RCT Registry number)

## Multiple Testing
- When testing multiple outcomes or subgroups, acknowledge the multiple testing problem
- Pre-specify outcome families and consider summary indices to reduce the number of tests
- Report family-wise error rate corrections (Bonferroni, Holm) or false discovery rate (Benjamini-Hochberg); for pre-specified outcome families, report Anderson (2008) sharpened FDR q-values
- At minimum, flag which results survive multiple testing correction

## Specification Robustness
- Do NOT present only the specification that "works"
- Consider a specification curve or multiverse analysis for key results
- Report the distribution of estimates across reasonable specifications

## Transparency and Reproducibility
- State data availability clearly: public, restricted access, or proprietary
- Provide or reference replication code
- Describe any data cleaning decisions that materially affect results
- If using restricted data, describe the application process so others can replicate

## Citation Integrity
- Verify every citation: confirm that the author names, year, journal, and key finding are accurate. AI tools frequently hallucinate or misattribute citations
- When citing a result from another paper, check that you are citing the correct specification (e.g., the preferred estimate, not a robustness check)
- Distinguish between working paper versions and published versions -- findings sometimes change between versions
- Do NOT cite papers you have not read. If you know a paper only through secondary citations, cite the secondary source: "as discussed in [secondary source]"
- For well-known results (e.g., Mincer returns, gravity equation), cite the original source, not a textbook or survey

## Replication Packages (AEA Data Editor Standards)
- Every empirical paper submitted to AEA journals (and increasingly other journals) must include a replication package
- Include a README following the Social Science Data Editors template: Data Availability & Provenance Statements, Dataset List, Computational Requirements (software versions, hardware, expected runtime), Description of Programs, Instructions for Replicators
- Cite every dataset in the manuscript's References section with standard in-text citations -- including datasets you created
- Directory structure: `data/raw/`, `data/analysis/`, `code/`, `results/`. Never commingle code and data files
- Code must reproduce all results without manual intervention. The only exception: a single config file where replicators set directory paths
- For restricted-access data: provide a Data Availability Statement explaining application procedures, expected wait times, and any monetary costs
- Include a `LICENSE.txt` (AEA recommends CC-BY 4.0 for data and documents, and the modified BSD license for code)
- Map every table and figure to a specific program file: "Table 3 is produced by `code/table3_main_results.do`"
- These standards apply to AEA, Econometrica (ES Data Editor), Economic Journal, and increasingly to field journals

## AI Use Disclosure
- AEA policy: AI may not be listed as an author. If AI was used in drafting or editing the manuscript, disclose this during submission
- Econometric Society: requires a responsibility statement that all co-authors accept responsibility for all content
- What to disclose: drafting assistance, code generation, literature search assistance, data analysis suggestions
- What typically does not require disclosure: spell-check, grammar tools, LaTeX formatting
- Regardless of journal policy: you are responsible for verifying ALL AI-generated content, including citations, numerical claims, and statistical interpretations
- Practical rule: if AI drafted a paragraph, read it as if a careless RA wrote it -- verify every fact, every citation, every number

---


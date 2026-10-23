# TABLES AND FIGURES

*For LaTeX formatting of tables, figures, and bibliographies, see [latex-tips.md](latex-tips.md).*

## Regression Tables
- Every table must have a self-contained caption explaining the regression, variables, and what is shown
- No number should appear in a table that is not discussed in the text
- Use plain English variable names ("Years of education", "Female"), NOT code names
- Use consistent decimal places (2-3) throughout all tables
- Report standard errors for every important number. Specify clustering level ("Standard errors clustered at the state level")
- Report at the bottom of each table: N, R-squared, which fixed effects are included, and the list of controls
- Significance stars: * 10%, ** 5%, *** 1% (note: some journals discourage stars; check target journal style)
- A reader should be able to write down the exact regression from the table alone

## Descriptive Statistics Tables
*(For where this table belongs and balance-test placement, see [writing-data.md](writing-data.md).)*
- Report N, mean, SD, min, max for all key variables
- Separate panels for treatment vs. control groups (if applicable)
- Balance tests: report difference in means with p-values in a separate column or table
- Define every variable in the table notes
- Round to 2-3 meaningful decimal places

## Figures
- A good figure conveys a pattern more clearly than a table with many rows
- Give figures self-contained captions with verbal definitions of symbols
- Label axes clearly with sensible units
- Avoid dotted lines that disappear when reproduced
- Do not use dashes for volatile series

## When to Use Figures vs. Tables
- Use **figures** for: trends over time, distributions, non-linear relationships, RD/event-study plots, and any result where the visual pattern is the point
- Use **tables** for: regression coefficients with standard errors, precise numerical comparisons across specifications, summary statistics
- A figure showing 20 regression coefficients (coefficient plot) is usually better than a table with 20 rows
- Rule of thumb: if you say "as Table 3 shows, there is an inverted-U relationship," replace the table with a figure
- Every key result should appear in EITHER a figure or a table, not both (save space)
- Place the most important figure/table near the beginning of the results section

## Data Visualization (Schwabish, JEP)
- Show the data, not the analyst's cleverness
- Reduce non-data ink (Tufte principle)
- Use direct labels instead of legends when possible
- Highlight the comparison that matters
- Use consistent color schemes across related figures

---


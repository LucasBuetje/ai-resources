# Example: Defensive Merge with Assertions
# Economic context: Merging GDP panel with inflation data

# Assert: Verify keys exist and are unique to prevent merge explosion
stopifnot(length(unique(df_gdp$iso_year)) == nrow(df_gdp))
stopifnot(length(unique(df_inflation$iso_year)) == nrow(df_inflation))

# Join: Explicit by-argument to avoid silent natural joins
df_merged <- df_gdp %>%
  inner_join(df_inflation, by = c("iso_code", "year"))

# Assert: Validate no data loss
stopifnot(nrow(df_merged) == nrow(df_gdp))

# Transformation: Log-linearize
df_merged$log_gdp <- log(df_merged$gdp)

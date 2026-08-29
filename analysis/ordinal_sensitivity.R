args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) stop("Usage: Rscript ordinal_sensitivity.R input.csv output.json")
required <- c("ordinal", "jsonlite")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) stop(paste("Install:", paste(missing, collapse = ", ")))
data <- read.csv(args[[1]])
fit <- ordinal::clmm(as.factor(rating) ~ condition + (1 | participant_code) + (1 | scenario_id), data = data)
summary <- list(n = nrow(data), coefficients = coef(summary(fit)), warning = "Optional ordinal sensitivity analysis; interpret alongside diagnostics and effect sizes.")
jsonlite::write_json(summary, args[[2]], pretty = TRUE, auto_unbox = TRUE)


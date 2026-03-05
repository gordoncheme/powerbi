cat(
  "\nTableau TWBX Parser\n",
  "-------------------\n",
  "Purpose:\n",
  "Extract metadata from a Tableau .twbx file and write CSV outputs.\n\n"
)

library(twbparser)
library(readr)
library(dplyr)

# ---- Helper -------------------------------------------------------------

strip_quotes <- function(x) {
  x <- trimws(x)
  gsub('^"(.*)"$|^\047(.*)\047$', '\\1\\2', x)
}

# ---- User inputs --------------------------------------------------------

path <- readline(
  prompt = "Enter path to the .twbx file (with or without quotes): "
)

path <- strip_quotes(path)

if (path == "") {
  stop("No TWBX path provided. Aborting.")
}

if (!file.exists(path)) {
  stop(paste("File not found:", path))
}

out_dir <- readline(
  prompt = "Enter output directory name [default: twbparser_out]: "
)

out_dir <- strip_quotes(out_dir)

if (out_dir == "") {
  out_dir <- "twbparser_out"
}

# ---- Setup --------------------------------------------------------------

dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

cat("\nUsing TWBX file:\n ", normalizePath(path), "\n")
cat("Writing output to:\n ", normalizePath(out_dir), "\n\n")

# ---- Parse --------------------------------------------------------------

parser <- TwbParser$new(path)

write_csv(parser$get_datasources(),
          file.path(out_dir, "datasources.csv"))

write_csv(parser$get_fields(),
          file.path(out_dir, "fields.csv"))

write_csv(
  parser$get_calculated_fields(pretty = TRUE, wrap = 120),
  file.path(out_dir, "calculated_fields.csv")
)

write_csv(parser$get_joins(),
          file.path(out_dir, "joins_legacy.csv"))

write_csv(parser$get_relationships(),
          file.path(out_dir, "relationships_modern.csv"))

write_csv(parser$pages,
          file.path(out_dir, "pages.csv"))

write_csv(parser$pages_summary,
          file.path(out_dir, "pages_summary.csv"))

write_csv(
  twb_custom_sql(parser$xml_doc),
  file.path(out_dir, "custom_sql.csv")
)

cat("\nDone.\n")
cat("Files written to:", normalizePath(out_dir), "\n")

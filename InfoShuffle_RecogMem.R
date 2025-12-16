# Create mapping
option1_seq <- 1:10
option2_seq <- letters[1:10]

map_A <- data.frame(
  actual = paste0("sequence_", option1_seq),
  lure   = paste0("sequence_", option2_seq),
  stringsAsFactors = FALSE
)

map_B <- data.frame(
  actual = paste0("sequence_", option2_seq),
  lure   = paste0("sequence_", option1_seq),
  stringsAsFactors = FALSE
)

mapping_table <- rbind(map_A, map_B)

# Path to save CSVs
save_path <- "/Users/laurigurguryan/Desktop/InfoShuffleProject"

# Sequences
seq_numbers <- 1:10
seq_letters <- letters[1:10]

# Base categories with 5 options each
base_categories <- list(
  cat1 = paste0("cat1-", 1:5),
  cat2 = paste0("cat2-", 1:5),
  cat3 = paste0("cat3-", 1:5),
  cat4 = paste0("cat4-", 1:5),
  cat5 = paste0("cat5-", 1:5)
)

# Function to get sequence ID from filename
get_sequence_id <- function(filename, mapping_actuals) {
  matched <- mapping_actuals[sapply(mapping_actuals, function(x) grepl(x, filename))]
  if(length(matched) == 0) return(NA)
  return(matched[1])
}

# Function to combine left/right images, preserve original positions, and generate unique lures
combine_images_with_lure <- function(seq_name, mapping_table, base_categories) {
  test_file <- file.path(save_path, paste0(seq_name, "_test.csv"))
  
  if(!file.exists(test_file)) {
    message("File not found: ", test_file)
    return(NULL)
  }
  
  test_df <- read.csv(test_file, stringsAsFactors = FALSE)
  
  # Stack left and right images
  studied_image <- c(test_df$left_image, test_df$right_image)
  original_position <- c(test_df$left_original_position, test_df$right_original_position)
  
  combined_df <- data.frame(
    studied_image = studied_image,
    original_position = original_position,
    stringsAsFactors = FALSE
  )
  
  # Extract cat part
  cat_part <- regmatches(combined_df$studied_image, regexpr("cat[0-9]+-", combined_df$studied_image))
  cat_part_clean <- sub("-$", "", cat_part)
  combined_df$cat <- cat_part_clean
  
  # Generate unique lure numbers per cat
  combined_df <- do.call(rbind, lapply(split(combined_df, combined_df$cat), function(subdf) {
    cat_name <- unique(subdf$cat)
    if(is.na(cat_name) || !(cat_name %in% names(base_categories))) {
      subdf$lure <- NA
    } else {
      n <- nrow(subdf)
      numbers <- rep(base_categories[[cat_name]], length.out = n)
      numbers <- sample(numbers) # shuffle without replacement
      lure_base <- paste0(mapping_table$lure[match(sapply(subdf$studied_image, get_sequence_id, mapping_table$actual), mapping_table$actual)], "_stimuli/")
      subdf$lure <- paste0(lure_base, numbers)
    }
    subdf
  }))
  
  # Drop temporary column
  combined_df$cat <- NULL
  
  # Save CSV
  out_file <- file.path(save_path, paste0(seq_name, "_test_recog.csv"))
  write.csv(combined_df, out_file, row.names = FALSE, quote = FALSE)
  
  message("Saved: ", out_file)
}

# Apply to all sequences
all_sequences <- c(paste0("sequence_", seq_numbers), paste0("sequence_", seq_letters))

for(seq_name in all_sequences) {
  combine_images_with_lure(seq_name, mapping_table, base_categories)
}

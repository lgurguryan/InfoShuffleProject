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

# Path 
save_path <- "/Users/laurigurguryan/Desktop/InfoShuffleProject"

# Info 
seq_numbers <- 1:10
seq_letters <- letters[1:10]
all_sequences <- c(
  paste0("sequence_", seq_numbers),
  paste0("sequence_", seq_letters)
)

base_categories <- list(
  cat1 = paste0("cat1-", 1:5),
  cat2 = paste0("cat2-", 1:5),
  cat3 = paste0("cat3-", 1:5),
  cat4 = paste0("cat4-", 1:5),
  cat5 = paste0("cat5-", 1:5)
)

# Subjects
#subjects <- c("01", "02")
subjects <- sprintf("%02d", 1:10)

# Get sequence ID
get_sequence_id <- function(filename, mapping_actuals) {
  matched <- mapping_actuals[sapply(mapping_actuals, function(x) grepl(x, filename))]
  if (length(matched) == 0) return(NA)
  matched[1]
}

# Create function 
combine_images_with_lure <- function(
    seq_name,
    mapping_table,
    base_categories,
    subject_folder,
    seed = NULL
) {
  
  test_file <- file.path(save_path, paste0(seq_name, "_test.csv"))
  
  if (!file.exists(test_file)) {
    message("File not found: ", test_file)
    return(NULL)
  }
  
  if (!is.null(seed)) set.seed(seed)
  
  test_df <- read.csv(test_file, stringsAsFactors = FALSE)
  
  # Stack left/right images
  studied_image <- c(test_df$left_image, test_df$right_image)
  original_position <- c(
    test_df$left_original_position,
    test_df$right_original_position
  )
  
  combined_df <- data.frame(
    studied_image = studied_image,
    original_position = original_position,
    stringsAsFactors = FALSE
  )
  
  # Extract category
  cat_part <- regmatches(
    combined_df$studied_image,
    regexpr("cat[0-9]+-", combined_df$studied_image)
  )
  combined_df$cat <- sub("-$", "", cat_part)
  
  # Generate lures
  combined_df <- do.call(rbind, lapply(
    split(combined_df, combined_df$cat),
    function(subdf) {
      
      cat_name <- unique(subdf$cat)
      
      if (is.na(cat_name) || !(cat_name %in% names(base_categories))) {
        subdf$lure <- NA
      } else {
        n <- nrow(subdf)
        numbers <- rep(base_categories[[cat_name]], length.out = n)
        numbers <- sample(numbers)
        
        lure_base <- paste0(
          mapping_table$lure[
            match(
              sapply(subdf$studied_image, get_sequence_id, mapping_table$actual),
              mapping_table$actual
            )
          ],
          "_stimuli/"
        )
        
        subdf$lure <- paste0(lure_base, numbers)
      }
      
      subdf
    }
  ))
  
  combined_df$cat <- NULL
  
  # 50-50 left/right 
  n_trials <- nrow(combined_df)
  
  studied_on_left <- rep(c(TRUE, FALSE), length.out = n_trials)
  studied_on_left <- sample(studied_on_left)
  
  combined_df$left_image  <- NA_character_
  combined_df$right_image <- NA_character_
  
  combined_df$left_image[studied_on_left]  <- combined_df$studied_image[studied_on_left]
  combined_df$right_image[studied_on_left] <- combined_df$lure[studied_on_left]
  
  combined_df$left_image[!studied_on_left]  <- combined_df$lure[!studied_on_left]
  combined_df$right_image[!studied_on_left] <- combined_df$studied_image[!studied_on_left]
  
  combined_df$correct_answer <- ifelse(studied_on_left, "left", "right")
  
  # Shuffle row order for fully randomized trial sequence
  combined_df <- combined_df[sample(nrow(combined_df)), ]
  
  # Save
  subject_path <- file.path(save_path, subject_folder)
  if (!dir.exists(subject_path)) dir.create(subject_path)
  
  out_file <- file.path(subject_path, paste0(seq_name, "_test_recog.csv"))
  write.csv(combined_df, out_file, row.names = FALSE, quote = FALSE)
  
  message("Saved: ", out_file)
}

# Run function 
base_seed <- 1000 # set seed 

for(subject in subjects) {
  for(seq_name in all_sequences) {
    seed <- base_seed + as.integer(subject) * 100000 + match(seq_name, all_sequences)
    
    combine_images_with_lure(
      seq_name,
      mapping_table,
      base_categories,
      subject_folder = subject,
      seed = seed
    )
  }
}


# Create the new blocks csvs
# Loop over subjects and block versions
block_versions <- c("V1", "V2")

for(subject in subjects) {
  
  # Path to the subject folder where the CSVs are saved
  subject_folder_path <- file.path(save_path, subject)
  
  for(version in block_versions) {
    # Read original blocks CSV
    blocks_file <- file.path(save_path, paste0("blocks_", version, ".csv"))
    blocks_df <- read.csv(blocks_file, stringsAsFactors = FALSE)
    
    # Update test_file column: prepend the specified path + subject
    blocks_df$test_file <- paste0(
      "/Users/aussie-dzmac/Documents/InfoShuffleProject/RecogMemSubFolders/", 
      subject, "/",
      sub("_test", "_test_recog", blocks_df$test_file)
    )
    
    # Save updated CSV in the subject folder
    out_file <- file.path(subject_folder_path, paste0("blocks_", version, "_recog.csv"))
    write.csv(blocks_df, out_file, row.names = FALSE, quote = FALSE)
    message("Saved updated CSV for subject ", subject, ": ", out_file)
  }
}

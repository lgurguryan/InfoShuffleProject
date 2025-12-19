# Libraries 
library(pwr)

# Info 
n_subjects <- 10 
base_path <- "/Users/laurigurguryan/Desktop/InfoShuffleProject/SubjectFiles_RecogMemFullRando"
base_seed <- 13  
n_sequences <- 10
n_categories <- 5
n_exemplars <- 5

# Function to generate 1 sequence 
# (each category contributes one exemplar, 
# the order of categories is shuffled each time, 
# and the same category does not appear twice in a row)
generate_sequence <- function(categories_list) {
  blocks <- list()
  prev_last_cat <- NULL #keeps track of last cat used so no repeats back to back
  remaining <- categories_list
  
  for (i in 1:n_exemplars) {
    available_cats <- names(remaining)
    
    repeat {
      block_cats <- sample(available_cats)
      if (is.null(prev_last_cat) || block_cats[1] != prev_last_cat) break
    }
    
    block <- sapply(block_cats, function(cat) {
      exemplar <- remaining[[cat]][1]
      remaining[[cat]] <<- remaining[[cat]][-1]
      return(exemplar)
    }, USE.NAMES = FALSE)
    
    blocks[[i]] <- block
    prev_last_cat <- sub("-.*", "", tail(block, 1))
  }
  
  return(unlist(blocks))
}

# Function to create mutiple unique sequences 
generate_multiple_sequences <- function(base_categories, n_seq) {
  unique_seqs <- list()
  seen <- character(0)
  
  while (length(unique_seqs) < n_seq) {
    # Shuffle categories and exemplars
    categories <- lapply(base_categories, function(x) sample(x))
    seq <- generate_sequence(categories)
    seq_str <- paste(seq, collapse = "-")
    
    if (!(seq_str %in% seen)) {
      seen <- c(seen, seq_str)
      unique_seqs[[length(unique_seqs) + 1]] <- seq
    }
  }
  
  return(unique_seqs)
}

# Function to create test pairs 
create_test_pairs <- function(seq, prefix) {
  test_positions <- list(
    c(5,6), c(10,11), c(15,16), c(20,21),
    c(2,3), c(7,8), c(12,13), c(18,19), c(23,24)
  )
  
  across_boundary <- list(c(5,6), c(10,11), c(15,16), c(20,21))
  within_boundary <- list(c(2,3), c(7,8), c(12,13), c(18,19), c(23,24))
  
  test_data <- lapply(test_positions, function(pos) {
    img1 <- paste0(prefix, seq[pos[1]], ".jpg")
    img2 <- paste0(prefix, seq[pos[2]], ".jpg")
    
    pair_imgs <- c(img1, img2)
    pair_pos <- c(pos[1], pos[2])
    
    shuffled_indices <- sample(2)
    left_img <- pair_imgs[shuffled_indices[1]]
    right_img <- pair_imgs[shuffled_indices[2]]
    left_pos <- pair_pos[shuffled_indices[1]]
    right_pos <- pair_pos[shuffled_indices[2]]
    
    correct_answer <- ifelse(left_pos == pos[1], "left", "right")
    
    pairType <- if (any(sapply(across_boundary, function(x) identical(x,pos)))) {
      "across-boundary"
    } else if (any(sapply(within_boundary, function(x) identical(x,pos)))) {
      "within-boundary"
    } else {
      NA
    }
    
    data.frame(
      left_image = left_img,
      right_image = right_img,
      left_original_position = left_pos,
      right_original_position = right_pos,
      correct_answer = correct_answer,
      pairType = pairType,
      stringsAsFactors = FALSE
    )
  })
  
  test_df <- do.call(rbind, test_data)
  test_df <- test_df[sample(nrow(test_df)), ]  # shuffle rows
  return(test_df)
}

# Loop for all subjects 
for (subj in 1:n_subjects) {
  set.seed(base_seed + subj)
  subject_id <- sprintf("%02d", subj)
  subject_path <- file.path(base_path, subject_id)
  dir.create(subject_path, showWarnings = FALSE, recursive = TRUE)
  
  cat("Generating files for", subject_id, "\n")
  
  # Create base categories
  base_categories <- list()
  for (i in 1:n_categories) {
    cat_name <- paste0("cat", i)
    base_categories[[cat_name]] <- paste0(cat_name, "-", 1:n_exemplars)
  }
  
  # Shuffle exemplars within categories
  base_categories <- lapply(base_categories, sample)
  
  # Generate multiple shuffled sequences
  sequences <- generate_multiple_sequences(base_categories, n_sequences)
  
  encoding_questions <- c(
    "Do you know the word for this item in any other languages?",
    "Is this item man-made?",
    "Do you find this item to be pleasant?",
    "Would this item fit in a shoe box?",
    "Does this item contain any metal?"
  )
  
  # SHUFFLED sequences (1-10)
  for (i in 1:n_sequences) {
    seq <- sequences[[i]]
    categories <- sub("-.*", "", seq)
    
    shuffled_questions <- sample(encoding_questions)
    question_map <- setNames(shuffled_questions, paste0("cat", 1:5))
    encoding_col <- question_map[categories]
    
    prefix <- paste0("sequence_", i, "_stimuli/")
    seq_jpg <- paste0(prefix, seq, ".jpg")
    
    df <- data.frame(
      image_filename = seq_jpg,
      encoding_question = encoding_col,
      stringsAsFactors = FALSE
    )
    
    write.csv(df,
              file = file.path(subject_path, paste0("sequence_", i, ".csv")),
              row.names = FALSE, quote = FALSE
    )
    
    map_df <- data.frame(
      category = names(question_map),
      encoding_question = unname(question_map),
      stringsAsFactors = FALSE
    )
    
    write.csv(map_df,
              file = file.path(subject_path, paste0("sequence_", i, "_question_map.csv")),
              row.names = FALSE, quote = FALSE
    )
    
    # Create test CSV for shuffled sequences
    test_df <- create_test_pairs(seq, prefix)
    test_df$pairType <- "across-boundary"  # all should be across-boundary for shuffled 
    
    write.csv(test_df,
              file = file.path(subject_path, paste0("sequence_", i, "_test.csv")),
              row.names = FALSE, quote = FALSE
    )
  }
  
  # BLOCKED sequences (a-j)
  seq_names <- letters[1:10]
  
  for (i in 1:n_sequences) {
    df <- read.csv(file.path(subject_path, paste0("sequence_", i, ".csv")),
                   stringsAsFactors = FALSE)
    
    # Extract category and exemplar
    df$category <- sub("-.*", "", basename(df$image_filename))
    df$exemplar <- as.numeric(sub(".*-(\\d+)\\.jpg$", "\\1", df$image_filename))
    
    # Randomize category order and exemplars within categories
    category_order <- sample(unique(df$category))
    df_random <- do.call(rbind, lapply(category_order, function(cat) {
      cat_rows <- df[df$category == cat, ]
      cat_rows[sample(nrow(cat_rows)), ]
    }))
    
    # Image filenames for blocked sequence
    df_random$image_filename <- gsub(
      paste0("sequence_", i, "_stimuli/"),
      paste0("sequence_", seq_names[i], "_stimuli/"),
      df_random$image_filename
    )
    
    # Save blocked sequence CSV
    write.csv(df_random[, c("image_filename", "encoding_question")],
              file = file.path(subject_path, paste0("sequence_", seq_names[i], ".csv")),
              row.names = FALSE, quote = FALSE
    )
    
    # Save mapping CSV
    mapping <- tapply(df_random$encoding_question, df_random$category, `[`, 1)
    write.csv(
      data.frame(category = names(mapping),
                 encoding_question = unname(mapping)),
      file = file.path(subject_path,
                       paste0("sequence_", seq_names[i], "_question_map.csv")),
      row.names = FALSE, quote = FALSE
    )
    
    # Create test CSV for blocked sequence
    stim_names <- sub(".*/", "", sub(".jpg$", "", df_random$image_filename))
    blocked_prefix <- paste0("sequence_", seq_names[i], "_stimuli/")
    
    test_df_blocked <- create_test_pairs(seq = stim_names, prefix = blocked_prefix)
    write.csv(test_df_blocked,
              file = file.path(subject_path, paste0("sequence_", seq_names[i], "_test.csv")),
              row.names = FALSE, quote = FALSE
    )
  }
  
  # Create block csvs
  blocks_V1 <- data.frame(
    block = 1:10,
    csv_filename = c(paste0("sequence_", 1:5, ".csv"),
                     paste0("sequence_", letters[6:10], ".csv")),
    test_file = c(paste0("sequence_", 1:5, "_test.csv"),
                  paste0("sequence_", letters[6:10], "_test.csv")),
    stringsAsFactors = FALSE
  )
  
  write.csv(blocks_V1,
            file = file.path(subject_path, "blocks_V1.csv"),
            row.names = FALSE, quote = FALSE
  )
  
  blocks_V2 <- data.frame(
    block = 1:10,
    csv_filename = c(paste0("sequence_", 6:10, ".csv"),
                     paste0("sequence_", letters[1:5], ".csv")),
    test_file = c(paste0("sequence_", 6:10, "_test.csv"),
                  paste0("sequence_", letters[1:5], "_test.csv")),
    stringsAsFactors = FALSE
  )
  
  write.csv(blocks_V2,
            file = file.path(subject_path, "blocks_V2.csv"),
            row.names = FALSE, quote = FALSE
  )
  
  # Update blocks csv to include the path on aussie for each subject
  
  full_path_prefix <- paste0("/Users/aussie-dzmac/Documents/InfoShuffleProject/SubjectFiles_RecogMemFullRando/", subject_id, "/")
  
  # Blocks_V1
  blocks_V1$csv_filename <- paste0(full_path_prefix, blocks_V1$csv_filename)
  blocks_V1$test_file   <- paste0(full_path_prefix, blocks_V1$test_file)
  
  write.csv(blocks_V1,
            file = file.path(subject_path, "blocks_V1.csv"),
            row.names = FALSE, quote = FALSE
  )
  
  # Blocks_V2
  blocks_V2$csv_filename <- paste0(full_path_prefix, blocks_V2$csv_filename)
  blocks_V2$test_file   <- paste0(full_path_prefix, blocks_V2$test_file)
  
  write.csv(blocks_V2,
            file = file.path(subject_path, "blocks_V2.csv"),
            row.names = FALSE, quote = FALSE
  )
  
}  
###########################
### RECOGNITION MEMORY PART 
##########################

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
save_path <- "/Users/laurigurguryan/Desktop/InfoShuffleProject/SubjectFiles_RecogMemFullRando"

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
  
  test_file <- file.path(save_path, subject_folder, paste0(seq_name, "_test.csv"))
  
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
base_seed <- 999 # set seed 

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
new_path_prefix <- "/Users/aussie-dzmac/Documents/InfoShuffleProject/SubjectFiles_TemMemFullRando"

for(subject in subjects) {
  
  subject_folder_path <- file.path(save_path, subject)
  
  for(version in block_versions) {
    # Read original blocks CSV
    blocks_file <- file.path(save_path, subject, paste0("blocks_", version, ".csv"))
    blocks_df <- read.csv(blocks_file, stringsAsFactors = FALSE)
    
    # Replace the path for test_file
    blocks_df$test_file <- file.path(
      new_path_prefix, 
      subject, 
      basename(sub("_test", "_test_recog", blocks_df$test_file))
    )
    
    # Replace path for csv_filename 
    blocks_df$csv_filename <- file.path(
      new_path_prefix, 
      subject, 
      basename(blocks_df$csv_filename)
    )
    
    # Save updated CSV
    out_file <- file.path(subject_folder_path, paste0("blocks_", version, "_recog.csv"))
    write.csv(blocks_df, out_file, row.names = FALSE, quote = FALSE)
    
    message("Saved updated CSV for subject ", subject, ": ", out_file)
  }
}
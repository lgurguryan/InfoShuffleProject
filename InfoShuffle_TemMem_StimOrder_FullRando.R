# Libraries 
library(pwr)

# Info 
n_subjects <- 100 
base_path <- "/Users/laurigurguryan/Desktop/InfoShuffleProject/SubjectFiles_TemMemFullRando"
base_seed <- 42  
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
  
  full_path_prefix <- paste0("/Users/halledz/Documents/InfoShuffleProject/TemMem_W2026/SubjectFiles_TemMemFullRando/", subject_id, "/")
  
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



# Power analysis 
pwr.t.test(d = 0.2, power = 0.80, sig.level = 0.05,
           type = "paired", alternative = "two.sided")

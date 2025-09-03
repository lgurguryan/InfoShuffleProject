## SHUFFLED ##

# Get the same results each time i run the script 
set.seed(42)

# Create base categories
base_categories <- list(
  cat1 = paste0("cat1-", 1:5),
  cat2 = paste0("cat2-", 1:5),
  cat3 = paste0("cat3-", 1:5),
  cat4 = paste0("cat4-", 1:5),
  cat5 = paste0("cat5-", 1:5)
)

# Shuffle exemplars within each category
base_categories <- lapply(base_categories, sample)

# Function to generate a sequence
generate_sequence <- function(categories) {
  blocks <- list()
  prev_last_cat <- NULL
  remaining <- categories
  
  for (i in 1:5) {
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

# Generate multiple unique sequences
generate_multiple_sequences <- function(n) {
  unique_seqs <- list()
  seen <- character(0)
  
  while (length(unique_seqs) < n) {
    categories <- lapply(base_categories, sample)
    
    seq <- generate_sequence(categories)
    seq_str <- paste(seq, collapse = "-")
    
    if (!(seq_str %in% seen)) {
      seen <- c(seen, seq_str)
      unique_seqs[[length(unique_seqs) + 1]] <- seq
    }
  }
  
  return(unique_seqs)
}

# Get 10 versions of unique sequence 
sequences <- generate_multiple_sequences(10)

# Print  
for (i in 1:5) {
  cat(sprintf("Sequence %d:\n", i))
  print(matrix(sequences[[i]], nrow = 5, byrow = TRUE))
  cat("\n")
}

# Create CSV with encoding questions + mapping
save_path <- "/Users/laurigurguryan/Desktop/InfoShuffleProject"

# Define encoding questions
encoding_questions <- c("Do you know the word for this item in any other languages?", 
                        "Is this item man-made?", 
                        "Do you find this item to be pleasant?",
                        "Would this item fit in a shoe box?",
                        "Does this item contain any metal?")

for (i in 1:10) {
  seq <- sequences[[i]]
  
  # Extract categories from stimulus names 
  categories <- sub("-.*", "", seq)
  
  # Randomly assign encoding questions to categories
  shuffled_questions <- sample(encoding_questions)
  question_map <- setNames(shuffled_questions, paste0("cat", 1:5))
  
  # Map each stimulus to its category's question
  encoding_col <- question_map[categories]
  
  # Add folder prefix for image filenames
  prefix <- paste0("sequence_", i, "_stimuli/")
  seq_jpg <- paste0(prefix, seq, ".jpg")
  
  # Create dataframe with encoding questions
  df <- data.frame(
    image_filename = seq_jpg,
    encoding_question = encoding_col,
    stringsAsFactors = FALSE
  )
  
  # Save main sequence CSV
  file_path <- file.path(save_path, paste0("sequence_", i, ".csv"))
  write.csv(df, file = file_path, row.names = FALSE, quote = FALSE)
  
  # Save mapping CSV 
  map_df <- data.frame(
    category = names(question_map),
    encoding_question = unname(question_map),
    stringsAsFactors = FALSE
  )
  map_file_path <- file.path(save_path, paste0("sequence_", i, "_question_map.csv"))
  write.csv(map_df, file = map_file_path, row.names = FALSE, quote = FALSE)
}

# Test pairs 
save_path <- "/Users/laurigurguryan/Desktop/InfoShuffleProject"

test_positions <- list(c(5, 6), c(10, 11), c(15, 16), c(20, 21), 
                       c(2, 3), c(7, 8), c(12, 13), c(18, 19), c(23, 24))

# Define pair types
across_boundary <- list(c(5, 6), c(10, 11), c(15, 16), c(20, 21))
within_boundary <- list(c(2, 3), c(7, 8), c(12, 13), c(18, 19), c(23, 24))

set.seed(42)

for (i in 1:10) {
  seq <- sequences[[i]]
  prefix <- paste0("sequence_", i, "_stimuli/")
  
  test_data <- lapply(test_positions, function(pos) {
    # Images with their original positions
    img1 <- paste0(prefix, seq[pos[1]], ".jpg")
    img2 <- paste0(prefix, seq[pos[2]], ".jpg")
    
    # Create pairs and their original positions
    pair_imgs <- c(img1, img2)
    pair_pos  <- c(pos[1], pos[2])
    
    # Randomize left/right order
    shuffled_indices <- sample(2)
    left_img <- pair_imgs[shuffled_indices[1]]
    right_img <- pair_imgs[shuffled_indices[2]]
    left_pos <- pair_pos[shuffled_indices[1]]
    right_pos <- pair_pos[shuffled_indices[2]]
    
    # Determine correct answer
    correct_answer <- ifelse(left_pos == pos[1], "left", "right")
    
    # Determine pair type
    pairType <- if (any(sapply(across_boundary, function(x) identical(x, pos)))) {
      "across-boundary"
    } else if (any(sapply(within_boundary, function(x) identical(x, pos)))) {
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
  
  # Randomize row order
  test_df <- test_df[sample(nrow(test_df)), ]
  
  # Save 
  test_file_path <- file.path(save_path, paste0("sequence_", i, "_test.csv"))
  write.csv(test_df, file = test_file_path, row.names = FALSE, quote = FALSE)
}

## BLOCKED ##

# Use above and create the alternative sequences that are lettered 
# Sequence names a-j
seq_names <- letters[1:10]  

for (i in 1:10) {
  # Load the original randomized sequence
  orig_csv <- file.path(save_path, paste0("sequence_", i, ".csv"))
  df <- read.csv(orig_csv, stringsAsFactors = FALSE)
  
  # Extract category and exemplar number from filename
  df$category <- sub("-.*", "", sub(".*/", "", df$image_filename))  # cat1, cat2, etc.
  df$exemplar <- as.numeric(sub(".*-(\\d+)\\.jpg$", "\\1", df$image_filename))
  
  # Sort by category and exemplar
  df_sorted <- df[order(df$category, df$exemplar), ]
  
  # Replace the sequence number in the filename with the new letter (1=a, 2=b...)
  df_sorted$image_filename <- gsub(
    pattern = paste0("sequence_", i, "_stimuli/"),
    replacement = paste0("sequence_", seq_names[i], "_stimuli/"),
    x = df_sorted$image_filename
  )
  
  # Save the sorted sequence CSV
  new_csv <- file.path(save_path, paste0("sequence_", seq_names[i], ".csv"))
  write.csv(df_sorted[, c("image_filename", "encoding_question")], file = new_csv,
            row.names = FALSE, quote = FALSE)
  
  # Mapping category & encoding question
  mapping <- tapply(df_sorted$encoding_question, df_sorted$category, function(x) x[1])
  map_df <- data.frame(
    category = names(mapping),
    encoding_question = unname(mapping),
    stringsAsFactors = FALSE
  )
  
  # Save the mapping CSV
  map_file <- file.path(save_path, paste0("sequence_", seq_names[i], "_question_map.csv"))
  write.csv(map_df, file = map_file, row.names = FALSE, quote = FALSE)
}

# Test pairs
seq_names <- letters[1:10]  # a, b, c, ..., j

for (i in 1:10) {
  # Load the original randomized test CSV
  orig_test_csv <- file.path(save_path, paste0("sequence_", i, "_test.csv"))
  test_df <- read.csv(orig_test_csv, stringsAsFactors = FALSE)
  
  # Replace sequence number in left/right image filenames
  test_df$left_image <- gsub(
    pattern = paste0("sequence_", i, "_stimuli/"),
    replacement = paste0("sequence_", seq_names[i], "_stimuli/"),
    x = test_df$left_image
  )
  
  test_df$right_image <- gsub(
    pattern = paste0("sequence_", i, "_stimuli/"),
    replacement = paste0("sequence_", seq_names[i], "_stimuli/"),
    x = test_df$right_image
  )
  
  # Set all pairType to "across-boundary"
  test_df$pairType <- "across-boundary"
  
  # Save as new test CSV for sequences a-j
  new_test_csv <- file.path(save_path, paste0("sequence_", seq_names[i], "_test.csv"))
  write.csv(test_df, file = new_test_csv, row.names = FALSE, quote = FALSE)
}

## CREATE BLOCKS V1/V2 ##

# Define save path
save_path <- "/Users/laurigurguryan/Desktop/InfoShuffleProject"

# Sequence names
seq_letters <- letters[1:10]  

# v1
# csv filenames: 1-5 and f-j
v1_csv_files <- c(
  paste0("sequence_", 1:5, ".csv"),
  paste0("sequence_", seq_letters[6:10], ".csv")
)
# corresponding test files
v1_test_files <- gsub(".csv", "_test.csv", v1_csv_files)

# Create blocks_V1 dataframe
blocks_V1 <- data.frame(
  block = 1:10,
  csv_filename = v1_csv_files,
  test_file = v1_test_files,
  stringsAsFactors = FALSE
)

# Save CSV
write.csv(blocks_V1, file = file.path(save_path, "blocks_V1.csv"),
          row.names = FALSE, quote = FALSE)


# V2
# csv filenames: 6-10 and a-e
v2_csv_files <- c(
  paste0("sequence_", 6:10, ".csv"),
  paste0("sequence_", seq_letters[1:5], ".csv")
)
# corresponding test files
v2_test_files <- gsub(".csv", "_test.csv", v2_csv_files)

# Create blocks_V2 dataframe
blocks_V2 <- data.frame(
  block = 1:10,
  csv_filename = v2_csv_files,
  test_file = v2_test_files,
  stringsAsFactors = FALSE
)

# Save CSV
write.csv(blocks_V2, file = file.path(save_path, "blocks_V2.csv"),
          row.names = FALSE, quote = FALSE)

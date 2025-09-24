# Libraries 
library(dplyr)
library(ggplot2)

# Path
folder_path <- "/Users/laurigurguryan/Desktop/InfoShuffleProject/test"

# List all CSV files
csv_files <- list.files(path = folder_path, pattern = "\\.csv$", full.names = TRUE)

# Columns to keep (and in what ordered)
columns_to_keep <- c("participant", "block", "csv_filename", "test_file", "thisN", "image_filename", 
                     "StudyTrialResp.keys",	"StudyTrialResp.rt", "estimated_minutes", 
                     "estimated_seconds", "left_image", "right_image", 
                     "left_original_position", "right_original_position", "correct_answer", 
                     "pairType", "TestLoop.TestResp.keys", "TestLoop.TestResp.corr", 	"TestLoop.TestResp.rt", 
                     "DistractorLoop.thisRepN", "expName"
                     )

# Read CSVs, select columns, and combine
all_data <- do.call(rbind, lapply(csv_files, function(file) {
  df <- read.csv(file)
  
  df <- df[, intersect(columns_to_keep, names(df))]
  return(df)
}))

# Reorder columns exactly as in columns_to_keep
all_data <- all_data[, columns_to_keep]

# Remove NA rows (instructions)
#all_data <- all_data %>%
  #filter(!is.na(block) & block != "")

# Add condition (blocked vs shuffled)
all_data <- all_data %>%
  mutate(
    condition = case_when(
      grepl("sequence_\\d+", csv_filename) ~ "shuffled",  # check if number
      grepl("sequence_[A-Za-z]+", csv_filename) ~ "blocked", # check if letter
      TRUE ~ NA_character_  
    )
  )

# Add versoin of experiment 
all_data <- all_data %>%
  mutate(expVersion = sub("^[^_]+_", "", expName))


# Number of participants
num_unique_participants <- n_distinct(all_data$participant)
cat("Number of participants:", num_unique_participants, "\n")

####################
## TIME ESTIMATES ##
####################
# Drop rows with NA or blanks for 'estimated_minutes' & 'estimated_seconds'
# (gets rid of study/distractor/test rows)
time_estimates <- all_data[, c("participant", "condition", "estimated_minutes", "estimated_seconds")]

time_estimates <- time_estimates[
  !is.na(time_estimates$participant) & time_estimates$participant != "" &
    !is.na(time_estimates$estimated_minutes) & time_estimates$estimated_minutes != "" &
    !is.na(time_estimates$estimated_seconds) & time_estimates$estimated_seconds != "", ]

# Calculate mean and SD per condition
time_estimates <- time_estimates %>%
  mutate(
    estimated_minutes = as.numeric(estimated_minutes),
    estimated_seconds = as.numeric(estimated_seconds)
  )

time_avg_sd_per_condition <- time_estimates %>%
  group_by(condition) %>%
  summarise(
    mean_minutes = mean(estimated_minutes, na.rm = TRUE),
    sd_minutes = sd(estimated_minutes, na.rm = TRUE),
    mean_seconds = mean(estimated_seconds, na.rm = TRUE),
    sd_seconds = sd(estimated_seconds, na.rm = TRUE),
    .groups = "drop"
  )

print(time_avg_sd_per_condition)

# Calcualte TotalDuration (in seconds)
time_estimates <- time_estimates %>%
  mutate(
    estimated_minutes = as.numeric(estimated_minutes),
    estimated_seconds = as.numeric(estimated_seconds),
    TotalDuration = estimated_minutes * 60 + estimated_seconds
  )

# Calculate mean and SD 
time_avg_sd_per_condition <- time_estimates %>%
  group_by(condition) %>%
  summarise(
    mean_total = mean(TotalDuration, na.rm = TRUE),
    sd_total = sd(TotalDuration, na.rm = TRUE),
    .groups = "drop")

print(time_avg_sd_per_condition)

# Plot 
ggplot(time_estimates, aes(x = condition, y = TotalDuration)) +
  geom_jitter(aes(color = condition), width = 0.2, size = 3, alpha = 0.7) +  
  stat_summary(fun = mean, geom = "point", shape = 18, size = 5, color = "black") +  
  stat_summary(fun.data = mean_sdl, fun.args = list(mult = 1), geom = "errorbar", width = 0.2, color = "black") +  
  geom_hline(yintercept = 150, color = "red", linetype = "dashed", size = 1) +
  annotate("text", x = 1.5, y = 150, label = "actual time", 
           vjust = -1, color = "black", fontface = "bold") +
   labs(title = "Total duration by Condition",
    x = "Condition",
    y = "Total duration (seconds)"
  ) +
  theme_minimal() +
  theme(legend.position = "none")

ggplot(time_estimates, aes(x = condition, y = TotalDuration, fill = condition)) +
  geom_violin(trim = FALSE, alpha = 0.4, color = "black") +  
  geom_jitter(aes(color = condition), width = 0.2, size = 3, alpha = 0.7) +  
  stat_summary(fun = mean, geom = "point", shape = 18, size = 5, color = "black"  
  ) +
  stat_summary(fun.data = mean_sdl, fun.args = list(mult = 1), geom = "errorbar", width = 0.2, color = "black"  # SD/error bars
  ) +
  geom_hline(yintercept = 150, color = "red", linetype = "dashed", size = 1) +
  annotate("text", x = 1.5, y = 150, label = "actual time", 
             vjust = -1, color = "black", fontface = "bold") +
  labs(title = "Total duration by Condition",
    x = "Condition",
    y = "Total duration (seconds)"
  ) +
  theme_minimal() +
  theme(legend.position = "none")

####################
#### TEST PHASE ####
####################

# Filter to only keep test phase rows 
# (based on if has pairType; only test trials do)
test_df <- all_data %>%
  filter(!is.na(pairType) & pairType != "")

test_df <- test_df %>%
  mutate(TestLoop.TestResp.corr = as.numeric(TestLoop.TestResp.corr))

# Calculate mean and SD per participant
subject_stats <- test_df %>%
  group_by(participant, condition, pairType) %>%
  summarise(
    mean_corr = mean(TestLoop.TestResp.corr, na.rm = TRUE),
    sd_corr = sd(TestLoop.TestResp.corr, na.rm = TRUE),
    .groups = "drop"
  )

print(subject_stats)

#Plot 
ggplot(subject_stats, aes(x = pairType, y = mean_corr, fill = condition)) +
  geom_violin(trim = FALSE, alpha = 0.4, color = "black") +  
  geom_jitter(aes(color = condition), width = 0.2, size = 2, alpha = 0.7) +  
  stat_summary(
    fun = mean, geom = "point", shape = 18, size = 4, color = "black"  
  ) +
  stat_summary(fun.data = mean_sdl, fun.args = list(mult = 1), geom = "errorbar",
               width = 0.2, color = "black"  
  ) +
  facet_wrap(~condition) +
  labs(title = " Mean correct by PairType and Condition",
      x = "Pair Type",
      y = "Mean correct"
  ) +
  theme_minimal() +
  theme(legend.position = "none")

# Reaction times 
test_df <- test_df %>%
  mutate(TestLoop.TestResp.rt = as.numeric(TestLoop.TestResp.rt))

# Calculate mean and SD per participant
rt_subject_stats <- test_df %>%
  group_by(participant, condition, pairType) %>%
  summarise(
    mean_rt = mean(TestLoop.TestResp.rt, na.rm = TRUE),
    sd_rt = sd(TestLoop.TestResp.rt, na.rm = TRUE),
    .groups = "drop"
  )

print(rt_subject_stats)

# plot 
ggplot(rt_subject_stats, aes(x = pairType, y = mean_rt, fill = condition)) +
  geom_violin(trim = FALSE, alpha = 0.4, color = "black") +   
  geom_jitter(aes(color = condition), width = 0.2, size = 2, alpha = 0.7) +  
  stat_summary(fun = mean, geom = "point",shape = 18, size = 4, color = "black"  
  ) +
  stat_summary(fun.data = mean_sdl, fun.args = list(mult = 1), geom = "errorbar", width = 0.2, color = "black"  
  ) +
  facet_wrap(~condition) +
  labs(
    title = "Mean RT by PairType and Condition",
    x = "Pair Type",
    y = "Mean RT (ms)"
  ) +
  theme_minimal() +
  theme(legend.position = "none")
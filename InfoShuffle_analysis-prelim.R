####################
## Load libraries ##
####################

# dplyr: tools for manipulating and summarizing data
library(dplyr)

# ggplot2: used to create visualizations
library(ggplot2)

# effsize: used to compute effect sizes such as Cohen's d
library(effsize)

# lme4: used to run mixed-effects models
library(lme4)      

# lmerTest: adds statistical tests (p-values) to mixed models
library(lmerTest)  

# tidyr: tools for reshaping data 
library(tidyr)

##############
## Set path ##
##############

# This tells R where the participant data files are stored.
# Each participant completed the experiment and produced a CSV file.
# We want to combine all of these files into one dataset.

# You will have to change this to match the folder on your desktop with the files
folder_path <- "/Users/laurigurguryan/Desktop/InfoShuffleProject/temmem"

########################
## List all CSV files ##
########################

# list.files() searches the folder and returns the names of all CSV files.
# full.names = TRUE ensures we get the full file path so R can open them.

csv_files <- list.files(path = folder_path, pattern = "\\.csv$", full.names = TRUE)

#####################
## Columns to keep ##
#####################

# Experiment output files often contain MANY columns.
# We only keep the columns relevant to our analysis.
columns_to_keep <- c("participant", "block", "csv_filename", "test_file", "thisN", "image_filename", 
                     "StudyTrialResp.keys",	"StudyTrialResp.rt", "estimated_minutes", 
                     "estimated_seconds", "left_image", "right_image", 
                     "left_original_position", "right_original_position", "correct_answer", 
                     "pairType", "TestLoop.TestResp.keys", "TestLoop.TestResp.corr", 	"TestLoop.TestResp.rt", 
                     "DistractorLoop.thisRepN", "expName"
                     )
############################################
## Read CSVs, select columns, and combine ##
############################################

# lapply() loops through each CSV file and reads it into R.
# read.csv() loads each participant's data.
# intersect() ensures we only keep columns that actually exist in the file.
# do.call(rbind, ...) stacks all participant dataframes into ONE dataframe.

all_data <- do.call(rbind, lapply(csv_files, function(file) {
  df <- read.csv(file)
  
  df <- df[, intersect(columns_to_keep, names(df))]
  return(df)
}))

###################################################
## Reorder columns exactly as in columns_to_keep ##
###################################################
all_data <- all_data[, columns_to_keep]

##########################
## Add condition label ##
#########################

# Our experiment has two conditions: blocked vs shuffled
# The condition is encoded in the filename.
# We detect it using pattern matching.

all_data <- all_data %>%
  mutate(
    condition = case_when(
      grepl("sequence_\\d+", csv_filename) ~ "shuffled",  # check if number, label as shuffled
      grepl("sequence_[A-Za-z]+", csv_filename) ~ "blocked", # check if letter, label as blocked
      TRUE ~ NA_character_  
    )
  )

###############################
## Add version of experiment ##
###############################

# This extracts the version number from the experiment name.
all_data <- all_data %>%
  mutate(expVersion = sub("^[^_]+_", "", expName))

###########################################
## Remove NAs (if participant ID is NA) ##
##########################################
all_data <- all_data %>%
  filter(!is.na(participant))

########################
## Count participants ##
########################

# n_distinct() counts the number of unique participants.

# Number of participants
num_unique_participants <- n_distinct(all_data$participant)
cat("Number of participants:", num_unique_participants, "\n")

# This prints the participant IDs
unique_ids <- unique(all_data$participant)
cat("Unique participant IDs:", paste(unique_ids, collapse = ", "), "\n")

##############
## Exclude ##
#############
exclude_ids <- c(3, 123, 131, 136, 145, 157, 161, 174, 175, 182)

all_data <- all_data[!(all_data$participant %in% exclude_ids), ]

# Number of participants after excluding
num_unique_participants_clean<- n_distinct(all_data$participant)
cat("Number of participants after exclusion:", num_unique_participants_clean, "\n")

unique_ids <- unique(all_data$participant)
cat("Unique participant IDs after exclusion:", paste(unique_ids, collapse = ", "), "\n")


####################
## TIME ESTIMATES ##
####################

# In this part of the experiment participants estimated how long the encoding task took.
# First we remove rows that do not contain time estimates 
# (these rows correspond to other parts of the experiment.)

# Drop rows with NA or blanks for 'estimated_minutes' & 'estimated_seconds'
# (gets rid of study/distractor/test rows)
time_estimates <- all_data %>%
  select(participant, condition, estimated_minutes, estimated_seconds) %>%
  filter(
    !is.na(participant),
    !is.na(estimated_minutes), estimated_minutes != "",
    !is.na(estimated_seconds), estimated_seconds != ""
  ) %>%
  # Convert time estimates to numeric values
  mutate(
    estimated_minutes = as.numeric(estimated_minutes),
    estimated_seconds = as.numeric(estimated_seconds),
    # Convert minutes and seconds to total seconds
    TotalDuration = estimated_minutes * 60 + estimated_seconds
  )

#####################
## Avg per subject ##
#####################
# Here we calculate each participant's average estimated duration.

time_subject <- time_estimates %>%
  group_by(participant, condition) %>%
  summarise(
    mean_total = mean(TotalDuration, na.rm = TRUE),
    .groups = "drop"
  )

# Summary stats per condition 
time_condition_summary <- time_subject %>%
  group_by(condition) %>%
  summarise(
    mean_total = mean(mean_total, na.rm = TRUE),
    sd_total = sd(mean_total, na.rm = TRUE),
    n = n(),
    se_total = sd_total / sqrt(n),
    .groups = "drop"
  )

print(time_condition_summary)

# Plot
ggplot(time_subject, aes(x = condition, y = mean_total)) +
  geom_jitter(aes(color = condition), width = 0.15, size = 3, alpha = 0.7) +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 5, color = "black") +
  stat_summary(fun.data = mean_sdl, fun.args = list(mult = 1),
               geom = "errorbar", width = 0.2, color = "black") +
  geom_hline(yintercept = 150, color = "red", linetype = "dashed", size = 1) +
  annotate("text", x = 1.5, y = 150, label = "Actual time", vjust = -1, fontface = "bold") +
  labs(
    title = "Estimated Duration by Condition",
    x = "Condition",
    y = "Estimated Duration (seconds)"
  ) +
  theme_minimal() +
  theme(legend.position = "none")

# Violin plot 
ggplot(time_subject, aes(x = condition, y = mean_total, fill = condition)) +
  geom_violin(trim = FALSE, alpha = 0.4, color = "black") +
  geom_jitter(aes(color = condition), width = 0.15, size = 3, alpha = 0.7) +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 5, color = "black") +
  stat_summary(fun.data = mean_sdl, fun.args = list(mult = 1),
               geom = "errorbar", width = 0.2, color = "black") +
  geom_hline(yintercept = 150, color = "red", linetype = "dashed", size = 1) +
  annotate("text", x = 1.5, y = 150, label = "Actual time", vjust = -1, fontface = "bold") +
  labs(
    title = "Estimated Duration by Condition",
    x = "Condition",
    y = "Estimated Duration (seconds)"
  ) +
  scale_fill_manual(values = c("lightblue", "pink")) +
  scale_color_manual(values = c("deepskyblue1", "orchid")) +
  theme_minimal() +
  theme(legend.position = "none")

# Stats (paired t-test)
# Reshape to make wide 
time_wide <- time_subject %>%
  pivot_wider(
    id_cols = participant,
    names_from = condition,
    values_from = mean_total
  )

head(time_wide)
#########################################
## Statistical testing (paired t-test) ##
#########################################

# We use a paired t-test because the same participants experienced both conditions.

# Reshape to make wide format
time_wide <- time_subject %>%
  pivot_wider(
    id_cols = participant,
    names_from = condition,
    values_from = mean_total
  )

head(time_wide)

# Paired t-test
t_test_result <- t.test(time_wide$shuffled, time_wide$blocked, paired = TRUE)
print(t_test_result)

# Effect size
# Cohen's d measures the magnitude of the effect.

# Interpreting  Cohen's d:
# 0.2  = small effect
# 0.5  = medium effect
# 0.8+ = large effect

cohen_d_result <- cohen.d(time_wide$shuffled, time_wide$blocked, paired = TRUE)
print(cohen_d_result)

####################
#### TEST PHASE ####
####################

# Filter to only keep test phase rows 
# (based on if has pairType; only test trials do)
test_df <- all_data %>%
  filter(!is.na(pairType) & pairType != "")

# Convert accuracy variable to numeric 
test_df <- test_df %>%
  mutate(TestLoop.TestResp.corr = as.numeric(TestLoop.TestResp.corr))

###############
## Accuracy ##
##############

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
  scale_fill_manual(values = c("springgreen", "yellow")) +
  scale_color_manual(values = c("seagreen", "orange")) +
  theme_minimal() +
  theme(legend.position = "none")

######################################################################
# Statistical test (glmm - generalized linear mixed effects model) ##
######################################################################
# Accuracy is binary (correct vs incorrect),

# This model predicts whether a response is correct or incorrect.
# Because the outcome has only two possibilities (correct vs incorrect),
# we use logistic regression instead of regular linear regression.

# The model estimates how predictors (like condition or pair type)
# change the likelihood of a correct response.

# Participant is included as a random effect to account for differences between people.

accuracy_lmm <- glmer(
  TestLoop.TestResp.corr ~ condition + pairType + (1 | participant),
  data = test_df,
  family = binomial,
  control = glmerControl(optimizer = "bobyqa")
)

summary(accuracy_lmm)

# This converts coefficients to odds ratios which are easier to interpret.
# Interpretations: 
# OR = 1  → the predictor does not change accuracy
# OR > 1  → the predictor makes correct responses more likely
# OR < 1  → the predictor makes correct responses less likely

# If OR < 1, we can calculate the decrease in odds using: 1 - OR
exp(fixef(accuracy_lmm))  

###
# Creat df with info about the test pairs 
pairs_df <- data.frame(
  pair_id = 1:9,
  pos1 = c(2, 5, 7, 10, 12, 15, 18, 20, 23),
  pos2 = c(3, 6, 8, 11, 13, 16, 19, 21, 24)
)

print(pairs_df)

# Function to get pair_id 
get_pair_id <- function(left_pos, right_pos, pairs_df) {
  # Check which row in pairs_df matches the positions (order doesn't matter)
  match_row <- pairs_df[
    (pairs_df$pos1 == left_pos & pairs_df$pos2 == right_pos) |
      (pairs_df$pos1 == right_pos & pairs_df$pos2 == left_pos), 
  ]
  
  if(nrow(match_row) == 0) return(NA) 
  return(match_row$pair_id)
}

# Apply function to test_df
test_df$pair_id <- apply(test_df[, c("left_original_position", "right_original_position")], 1, 
                         function(x) get_pair_id(x[1], x[2], pairs_df))

# Summary table as a function of pair_id (overall position)

pair_summary <- test_df %>%
  group_by(pairType, condition, pair_id) %>%
  summarise(
    mean_corr = mean(TestLoop.TestResp.corr, na.rm = TRUE),
    sd_corr = sd(TestLoop.TestResp.corr, na.rm = TRUE),
    n = n(),
    se_corr = sd_corr / sqrt(n),
    .groups = "drop"
  )


dodge <- position_dodge(width = 0.8)

ggplot(pair_summary, aes(x = pairType, y = mean_corr, fill = condition)) +
  geom_bar(stat = "identity", width = 0.7, position = dodge) +   
  geom_errorbar(aes(ymin = mean_corr - se_corr, ymax = mean_corr + se_corr),
                width = 0.2, position = dodge) +
  facet_wrap(~pair_id, scales = "free_x") +
  labs(
    x = "Pair type",
    y = "Mean correct response",
    title = "Mean correct response as a function of position"
  ) +
  theme_minimal() +
  theme(legend.position = "top")

# Across-boundary only
ggplot(
  pair_summary %>% filter(pairType == "across-boundary"),
  aes(x = pairType, y = mean_corr, fill = condition)
) +
  geom_bar(stat = "identity", width = 0.7, position = dodge) +
  geom_errorbar(aes(ymin = mean_corr - se_corr, ymax = mean_corr + se_corr),
                width = 0.2, position = dodge) +
  facet_wrap(~pair_id, scales = "free_x") +
  labs(
    x = "Pair type",
    y = "Mean correct response",
    title = "Mean correct response (Across-boundary pairs)"
  ) +
  theme_minimal() +
  theme(legend.position = "top")

# Within-boundary only
ggplot(
  pair_summary %>% filter(pairType == "within-boundary"),
  aes(x = pairType, y = mean_corr, fill = condition)
) +
  geom_bar(stat = "identity", width = 0.7, position = dodge) +
  geom_errorbar(aes(ymin = mean_corr - se_corr, ymax = mean_corr + se_corr),
                width = 0.2, position = dodge) +
  facet_wrap(~pair_id, scales = "free_x") +
  labs(
    x = "Pair type",
    y = "Mean correct response",
    title = "Mean correct response (Within-boundary pairs)"
  ) +
  theme_minimal() +
  theme(legend.position = "top")

# Test pairs where cond difference 
ggplot(
  pair_summary %>% filter(pair_id %in% c(2, 4, 6, 8)),
  aes(x = condition, y = mean_corr, fill = condition)
) +
  geom_bar(stat = "identity", width = 0.7, position = dodge) +
  geom_errorbar(aes(ymin = mean_corr - se_corr, ymax = mean_corr + se_corr),
                width = 0.2, position = dodge) +
  facet_wrap(~pair_id) +
  labs(
    x = "Condition",
    y = "Mean correct response",
    title = "Mean correct response for test pairs 2, 4, 6, 8"
  ) +
  theme_minimal() +
  theme(legend.position = "top")


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
                     "StudyTrialResp.keys", "StudyTrialResp.rt", "estimated_minutes",
                     "estimated_seconds", "left_image", "right_image",
                     "left_original_position", "right_original_position", "correct_answer",
                     "pairType", "TestLoop.TestResp.keys", "TestLoop.TestResp.corr", "TestLoop.TestResp.rt",
                     "DistractorLoop.thisRepN", "expName")

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
# The condition is encoded in the csv filename.
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
exclude_ids <- c(3, 123, 131, 136, 145, 157, 161, 174, 175, 182, 730635, 36696)

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
    TotalDuration = estimated_minutes * 60 + estimated_seconds)

#####################
## Avg per subject ##
#####################
# Here we calculate each participant's average estimated duration.
# Each participant has multiple trials, so we collapse them into one value per person.
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
    n = n(),
    .groups = "drop"
  )

time_condition_summary$sd_total <- tapply(
  time_subject$mean_total,
  time_subject$condition,
  sd
)

# Standard error is computed manually from SD and n.
time_condition_summary$se_total <- time_condition_summary$sd_total /
  sqrt(time_condition_summary$n)

#Print
print(time_condition_summary)


# Plot ##

# This is a bar plot
# Step 1: Start creating the ggplot
# We tell ggplot which dataset to use and which variables to map to axes.

# what you have in line 202 is incorrect...line 203 is the corrected versio
#ggplot (subject_stats, aes(x = pairType, y = mean_corr, fill = condition)) +
  ggplot(time_subject, aes(x = condition, y = mean_total, fill = condition)) +
  
  # Step 2: Bars (means per condition)
  # fill = condition makes each bar match its group color
  stat_summary(
    fun = mean,
    geom = "bar",
    alpha = 0.7   # alpha controls transparency (lower = more transparent)
  ) +
  
  # Step 3: Error bars (SE around the mean)
  # linewidth makes the error bars thicker and more visible
  stat_summary(
    fun.data = mean_se,
    geom = "errorbar",
    width = 0.2,
    linewidth = 1.2) +
  
  # Step 4: Connect points for each participant
  # group = participant tells ggplot which points belong together
  geom_line(
    aes(group = participant),
    color = "darkgray",
    alpha = 0.3) +
  
  # Step 5: Individual participant data points
  geom_jitter(
    width = 0.1,
    alpha = 0.3,
    size = 2,
    aes(color = condition)) +
  
  # Step 6: Manually set bar colors
  # scale_fill_manual overrides default ggplot colors
  # IMPORTANT: names must match condition values exactly
    
 # This is also incorrect (looks like you copy pasted incrrectly again...time estimates dont have pair type in analysis)
 # scale_fill_manual(values = c(
  #  "within" = "#FF7256",
  #  "across" = "#FF8C00")) +
 # scale_color_manual(values = c(
 #   "within" = "darkgreen",  
  #  "across" = "darkblue" )) +
    scale_fill_manual(values = c(
      "blocked" = "#FF7256",
      "shuffled" = "#FF8C00")) +
    scale_color_manual(values = c(
      "blocked" = "darkgreen",  
      "shuffled" = "darkblue" )) +
  # Step 7: Labels
  #labs(
  #  title = "",
  #  x = "Pair Type",
  #  y = "Mean") +
  # lines 246 to 249 are also incorrect. looks like you copy/pasted incorrectly. Correct below:
  labs(
    title = "",
    x = "Condition",
    y = "Time (in seconds)") +
  
  # Step 8: Clean theme
  # I've added options to change the font sizes
  theme_classic() +
  theme(
    axis.title.x = element_text(size = 18),  # X-axis label font size
    axis.title.y = element_text(size = 18),   # Y-axis label font size
    axis.text.x = element_text(size = 14),   # X-axis tick labels
    axis.text.y = element_text(size = 14) )+ # Y-axis tick labels
  
  
  # Step 9: Remove redundant legend (since fill already labels conditions)
  guides(
    fill = "none",
    color = "none")

  # Violin plot 
  ggplot(time_subject, aes(x = condition, y = mean_total, fill = condition)) +
    geom_violin(
      trim = FALSE,
      alpha = 0.5,
      color = "black") +
    geom_line(
      aes(group = participant),
      color = "darkgray",
      alpha = 0.3) +
    geom_jitter(
      aes(color = condition),
      width = 0.1,
      alpha = 0.7,
      size = 2 ) +
    stat_summary(
      fun = mean,
      geom = "point",
      shape = 18,
      size = 4,
      color = "black") +
    stat_summary(
      fun.data = mean_se,
      geom = "errorbar",
      width = 0.2,
      linewidth = 1.2,
      color = "black") +
    geom_hline(yintercept = 150, color = "red", linetype = "dashed", size = 1) +
    annotate("text", x = 1.5, y = 150, label = "Actual time", vjust = -1, fontface = "bold") +
    labs(
      title = "Average time estimates",
      x = "Condition",
      y = "Time (in seconds)") +
    scale_fill_manual(values = c(
      "blocked" = "lightblue",
      "shuffled" = "pink")) +
    scale_color_manual(values = c(
      "blocked" = "deepskyblue1",
      "shuffled" = "orchid")) +
    theme_classic() +
    guides(
      fill = "none",
      color = "none")
  
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
    .groups = "drop")

print(subject_stats)

#Plot ## Coming soon!
# I think you should have 2 plots:
# (1) for the effect of condition
# (2) for the effect of pairType
# This means you will have to subset the data similar how it's done during the analyses

#Plot for effect condition
df_condition_acc <- subset(subject_stats, pairType == "across-boundary")

ggplot (df_condition_acc, aes(x = condition, y = mean_corr, fill = condition)) +
  stat_summary(
    fun = mean,
    geom = "bar",
    alpha = 0.7   ) +
  stat_summary(
    fun.data = mean_se,
    geom = "errorbar",
    width = 0.2,
    linewidth = 1.2) +
  geom_line(
    aes(group = participant),
    color = "darkgray",
    alpha = 0.3) +
  geom_jitter(
    width = 0.1,
    alpha = 0.3,
    size = 2,
    aes(color = condition)) +
  scale_fill_manual(values = c(
    "blocked" = "lightblue2",
    "shuffled" = "palegreen3")) +
  scale_color_manual(values = c(
    "blocked" = "steelblue4",
    "shuffled" = "seagreen4" )) +
  labs(
    title = "",
    x = "Pair Type",
    y = "Mean") +
  theme_classic() +
  theme(
    axis.title.x = element_text(size = 18),  
    axis.title.y = element_text(size = 18),   
    axis.text.x = element_text(size = 14),   
    axis.text.y = element_text(size = 14) ) +
  guides(
    fill = "none",
    color = "none")

  
## You're missing the plot for the effect of pair type: 
  df_pairtype_acc <- subset(subject_stats, condition == "blocked")
  
  ggplot(df_pairtype_acc, aes(x = pairType, y = mean_corr, fill = pairType)) +
    stat_summary(
      fun = mean,
      geom = "bar",
      alpha = 0.7) +
    stat_summary(
      fun.data = mean_se,
      geom = "errorbar",
      width = 0.2,
      linewidth = 1.2) +
    geom_line(
      aes(group = participant),
      color = "darkgray",
      alpha = 0.3) +
    geom_jitter(
      width = 0.1,
      alpha = 0.4,
      size = 2,
      aes(color = pairType)) +
    scale_fill_manual(values = c(
      "within-boundary" = "navajowhite2",
      "across-boundary" = "thistle3")) +
    scale_color_manual(values = c(
      "within-boundary" = "sienna3",
      "across-boundary" = "mediumpurple4")) +
    labs(
      title = "",
      x = "Pair Type",
      y = "Proportion Correct") +
    theme_classic() +
    theme(
      axis.title.x = element_text(size = 18),  
      axis.title.y = element_text(size = 18),   
      axis.text.x = element_text(size = 14),   
      axis.text.y = element_text(size = 14) ) +
    guides(fill = "none", color = "none")
  
######################################################################
# Statistical test (glmm - generalized linear mixed effects model) ##
######################################################################
# Accuracy is binary (correct vs incorrect)
# We use logistic regression to model the probability of a correct response.
# Participant is included as a random effect to account for individual differences.

# 1. Effect of condition (shuffled vs blocked) for across-boundary pairs only

# Subset the data to only include "across" pairs
df_across <- subset(test_df, pairType == "across-boundary")

# Fit the logistic mixed-effects model
accuracy_condition <- glmer(
  TestLoop.TestResp.corr ~ condition + (1 | participant),
  data = df_across,
  family = binomial,
  control = glmerControl(optimizer = "bobyqa"))

summary(accuracy_condition)

# Convert coefficients to odds ratios for easier interpretation

exp(fixef(accuracy_condition))

# Interpretation notes
# Intercept: represents baseline accuracy for the reference condition and reference pair type
# OR > 1 for a predictor → the predictor increases the odds of a correct response
# OR < 1 for a predictor → the predictor decreases the odds of a correct response
# To convert OR to percentage change in odds: % change = (OR - 1) * 100
# - Positive % → predictor increases accuracy
# - Negative % → predictor decreases accuracy
# Probability of correct response can be calculated from odds using: probability = odds / (1 + odds)

# 2. Effect of pairType (within vs across) for blocked condition only

# Subset the data to only include blocked condition
df_blocked <- subset(test_df, condition == "blocked")

# Fit the logistic mixed-effects model
accuracy_pairType <- glmer(
  TestLoop.TestResp.corr ~ pairType + (1 | participant),
  data = df_blocked,
  family = binomial,
  control = glmerControl(optimizer = "bobyqa"))

summary(accuracy_pairType)

# Convert coefficients to odds ratios
exp(fixef(accuracy_pairType))

# Notes:
# 1. The first model tells you how accuracy differs between shuffled and blocked conditions,
# only for across pairs.

# 2. The second model tells you how accuracy differs between within- and across-boundary pairs,
# only in the blocked condition where both pair types exist.


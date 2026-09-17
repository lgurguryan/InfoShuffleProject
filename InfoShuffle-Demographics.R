library(readxl)
library(dplyr)


# Load data
file_path1 <- "/Users/laurigurguryan/Desktop/online-demo-IRB30014-20240927-approved (Responses).xlsx"
data1 <- read_excel(file_path1, sheet = "infoshuffle")

file_path2 <- "/Users/laurigurguryan/Desktop/online-demo-MASI-PILOT-IRB30014_Responses.xlsx"
data2 <- read_excel(file_path2, sheet = "infoshuffle2")

# Remove unwanted IDs
drop_ids <- c(109, 123, 131, 136, 145, 157, 161, 174, 175, 179, 182)

data1 <- data1 %>%
  filter(!`Subject ID` %in% drop_ids)

data2 <- data2 %>%
  filter(!SubID %in% drop_ids)


# Clean ID columns 
data1_ids <- as.numeric(data1$`Subject ID`)
data2_ids <- as.numeric(data2$SubID)

# Combine IDs
combined_ids <- unique(c(data1_ids, data2_ids))

# Reference ID list
IDs <- c(4, 5, 6, 7, 9, 10, 100, 101, 102, 103, 104, 105, 106, 107, 108,
         11, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119,
         12, 120, 121, 122, 124, 125, 126, 127, 128, 129,
         13, 130, 132, 133, 134, 135, 137, 138, 139, 140, 141, 142, 143,
         144, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156,
         158, 159, 160, 162, 163, 164, 165, 166, 167, 168, 169, 170,
         171, 172, 173, 176, 177, 178, 180, 181, 183, 184, 185, 186,
         187, 188, 189, 190, 191)

IDs <- as.numeric(IDs)

# Find missing 
missing_ids <- sort(setdiff(IDs, combined_ids))
extra_ids   <- sort(setdiff(combined_ids, IDs))

cat("MISSING FROM DATA (in reference but not in data):\n")
print(missing_ids)

cat("\nEXTRA IN DATA (in data but not in reference):\n")
print(extra_ids)

# Gneder 
cat("\nData1:\n")
print(
  data1 %>%
    count(`Please Indicate your gender:`)
)

cat("\nData2:\n")
print(
  data2 %>%
    count(Gender)
)

# Age (missing 9 cuz DOB stored weird)
age_data1 <- data1 %>%
  select(ID = `Subject ID`, Age) %>%
  mutate(
    Age = as.numeric(Age),
    dataset = "data1")

age_data2 <- data2 %>%
  select(ID = SubID, Age) %>%
  mutate(
    Age = as.numeric(Age),
    dataset = "data2")

# Combine datasets
age_all <- bind_rows(age_data1, age_data2)

# Ensure Age is numeric
age_all <- age_all %>%
  mutate(Age = as.numeric(Age))

# Keep only valid (non-missing) ages
age_valid <- age_all %>%
  filter(!is.na(Age))

cat("VALID IDS USED IN AGE CALCULATION:\n")
print(sort(unique(age_valid$ID)))

# These participants did not enter correct DOB (entered actual date)
age_invalid <- age_all %>%
  filter(is.na(Age))

cat("NON-VALID AGE IDS (missing or non-numeric ages):\n")
print(sort(unique(age_invalid$ID)))

cat("\nFull non-valid rows:\n")
print(age_invalid)

mean_age <- mean(age_valid$Age, na.rm = TRUE)
sd_age   <- sd(age_valid$Age, na.rm = TRUE)
n_valid  <- nrow(age_valid)

cat("\nN used:", n_valid, "\n")
cat("Mean age:", mean_age, "\n")
cat("SD age:", sd_age, "\n")
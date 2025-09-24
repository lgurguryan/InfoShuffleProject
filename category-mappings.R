# List names 
List <- c(1, "a", 2, "b", 3, "c", 4, "d", 5, "e", 
          6, "f", 7, "g", 8, "h", 9, "i", 10, "j")

# ListType 
original_ListType <- rep(c("shuffled", "blocked"), times = 10)

# CategoryNum 
cat_nums <- paste0("cat", 1:5)

# CategoryNames for each List
category_names_list <- list(
  `1` = c("icecream", "coffee-mug", "binoculars", "baseball-gloves", "headphones"),
  `a` = c("icecream", "coffee-mug", "binoculars", "baseball-gloves", "headphones"),
  `2` = c("hibiscus", "ewer", "screwdriver", "chess-board", "necktie"),
  `b` = c("hibiscus", "ewer", "screwdriver", "chess-board", "necktie"),
  `3` = c("hamburger", "cactus", "football-helmet", "diamond-ring", "calculator"),
  `c` = c("hamburger", "cactus", "football-helmet", "diamond-ring", "calculator"),
  `4` = c("grapes", "hourglass", "cereal-box", "megaphone", "electric guitar"),
  `d` = c("grapes", "hourglass", "cereal-box", "megaphone", "electric guitar"),
  `5` = c("owl", "toaster", "desk-globe", "teddy-bear", "t-shirt"),
  `e` = c("owl", "toaster", "desk-globe", "teddy-bear", "t-shirt"),
  `6` = c("cake", "watch", "spaghetti", "dice", "backpack"),
  `f` = c("cake", "watch", "spaghetti", "dice", "backpack"),
  `7` = c("computer-keyboard", "fire-extinguisher", "mushroom", "cowboy-hat", "skateboard"),
  `g` = c("computer-keyboard", "fire-extinguisher", "mushroom", "cowboy-hat", "skateboard"),
  `8` = c("dog", "chopstick", "dumbell", "boombox", "flashlight"),
  `h` = c("dog", "chopstick", "dumbell", "boombox", "flashlight"),
  `9` = c("duck", "sneaker", "sushi", "teapot", "soccer-ball"),
  `i` = c("duck", "sneaker", "sushi", "teapot", "soccer-ball"),
  `10` = c("frog", "rotary-phone", "frying-pan", "tweezer", "xylophone"),
  `j` = c("frog", "rotary-phone", "frying-pan", "tweezer", "xylophone")
)

# Empty vectors 
List_expanded <- c()
ListType_expanded <- c()
CategoryNum_expanded <- c()
CategoryName_expanded <- c()

# Fill
for(i in seq_along(List)) {
  current_list <- List[i]
  current_type <- original_ListType[i]
  current_categories <- category_names_list[[as.character(current_list)]]
  
  List_expanded <- c(List_expanded, rep(current_list, 5))
  ListType_expanded <- c(ListType_expanded, rep(current_type, 5))
  CategoryNum_expanded <- c(CategoryNum_expanded, cat_nums)
  CategoryName_expanded <- c(CategoryName_expanded, current_categories)
}

# Build dataframe
df <- data.frame(
  List = List_expanded,
  ListType = ListType_expanded,
  CategoryNum = CategoryNum_expanded,
  CategoryName = CategoryName_expanded
)

# Save CSV
write.csv(df, "category-mappings.csv", row.names = FALSE)

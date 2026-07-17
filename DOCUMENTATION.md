# Conary Syntax Documentation
> Reference guide for writing .cnry application software scripts and games.

Every Conary script file must use the .cnry file extension framework and initiate the internal core engine using the mandatory bootstrap statement at the absolute top of the stack.

---

## 🛠️ Core Keywords Reference

### 1. Engine Initialization
initialUI
# Required at Line 1 of every single file to configure runtime environments.

### 2. Variable Trackers & IO Systems
* Text values with spaces must be enclosed in double quotes (" ").

# Instantiate an active data memory address variable
setup_var player_score 500
setup_var greeting_msg "Welcome Player One"

# Request user physical input interface fields dynamically
input_var current_user "Enter your profile alias: "

# Print target variable values or raw string content layers directly
write greeting_msg
write "Complete Operation Sequence Successful."

### 3. Mathematical Manipulations
# Syntax format standard: math_var [variable] [operator] [modifier_value]
math_var player_score + 10
math_var player_score - 50
math_var player_score * 2

### 4. Game Utilities
# Generates a random integer between low and high (inclusive) and saves it to a variable.
get_random enemy_spawn 1 100

### 5. Control Architecture (Branches & Logic Blocks)
All conditional branches must end with the keyword end_block.

#### Human-Readable Conditional Gating
Supports logical comparator evaluation parameters: >, <, and ==.

if player_score meets condition > 750 do
    write "Status: Absolute Grandmaster!"
otherwise if player_score meets condition == 500 do
    write "Status: Right in the middle!"
otherwise do
    write "Status: Keep grinding!"
end_block

### 6. Turtle Graphics UI Engine
Directly interfaces with a desktop GUI canvas window for drawing interfaces and game elements.

# Initialize the 800x600 graphics engine window
ui_init

# Change the background window color
ui_bg_color "black"

# Teleport the drawing pen to an (X, Y) coordinate instantly
ui_move -100 50

# Draw a filled square with a target size and color
ui_draw_square 150 "cyan"

# Render text directly onto the graphical canvas window
ui_write "Score: 100"

# Wipe the canvas screen completely clear
ui_clear

### 7. Native SQL Relational Database System
Directly interfaces with embedded internal relational database structural layers.

# Open or generate an isolated local database schema asset file
db_connect network.db

# Inject clean SQL query scripts. Use '$' to swap tracked system variables dynamically
db_execute CREATE TABLE IF NOT EXISTS inventory (item TEXT, quantity INTEGER);
db_execute INSERT INTO inventory VALUES ('$current_user', $player_score);

# Extract active row outputs straight to the output display window
db_execute SELECT * FROM inventory;
db_fetch

# Sever active pipe resources safely
db_close

---

## 🚀 How To Run Your Scripts

Once you have written your code file and saved it with a .cnry extension, open your system terminal inside that file's folder and run the execution command:

conary your_filename.cnry
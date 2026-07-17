# Conary Syntax Documentation
> Reference guide for writing .cnry application software scripts.

Every Conary script file must use the .cnry file extension framework and initiate the internal core engine using the mandatory bootstrap statement at the absolute top of the stack.

---

## 🛠️ Core Keywords Reference

### 1. Engine Initialization
initialConary
# Required at Line 1 of every single file to configure runtime environments.

### 2. Variable Trackers & IO Systems
* Whitespace separations in raw string print commands are declared using underscore (_) syntax rules.

# Instantiate an active data memory address variable
setup_var player_score 500
setup_var greeting_msg Welcome_User

# Request user physical input interface fields dynamically
input_var current_user Enter_your_profile_alias:_

# Print target variable values or raw string content layers directly
write greeting_msg
write Complete_Operation_Sequence_Successful.

### 3. Mathematical Manipulations
# Syntax format standard: math_var [variable] [operator] [modifier_value]
math_var player_score + 10
math_var player_score - 50
math_var player_score * 2

### 4. Control Architecture (Branches & Loops)
All operational code block scopes must be cleanly terminated using end_block.

#### Conditional Checks
Supports logical comparator evaluation parameters: >, <, and ==.
if_var player_score > 750
    write System_Level_Passed!
else_var
    write Retrying_Sequence...
end_block

#### Repeating Counter Loops
Iterates a code logic block a fixed number of times based on an integer or tracked variable.
setup_var loop_limit 3
loop_var loop_limit
    write Sync_Pulse_Active...
end_block

### 5. Native SQL Relational Database System
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

Once you have written your code file and saved it with a `.cnry` extension, open your system terminal inside that file's folder and run the execution command:

conary your_filename.cnry
import sys
import os
import sqlite3
import turtle
import re

def run_conary(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return

    with open(filename, 'r') as f:
        lines = f.readlines()

    if not lines or lines[0].strip() != "initialUI":
        print("Syntax Error [Line 1]: Script must begin with 'initialUI'")
        return

    variables = {}
    db_conn = None
    db_cursor = None
    
    line_idx = 1
    total_lines = len(lines)
    
    turtle_screen = None
    t = None

    def parse_value(val_str):
        val_str = val_str.strip()
        if val_str.startswith('"') and val_str.endswith('"'):
            return val_str[1:-1]
        if val_str.isdigit():
            return int(val_str)
        try:
            return float(val_str)
        except ValueError:
            if val_str in variables:
                return variables[val_str]
            return val_str

    def tokenize(line_str):
        return re.findall(r'[^"\s]+|"[^"]*"', line_str)

    def evaluate_condition(tokens):
        try:
            var_name = tokens[1]
            comp = tokens[4]
            val_to_compare = parse_value(tokens[5])
            v1 = variables.get(var_name, var_name)
            
            if comp == ">": return float(v1) > float(val_to_compare)
            elif comp == "<": return float(v1) < float(val_to_compare)
            elif comp == "==": return str(v1) == str(val_to_compare)
            return False
        except Exception:
            return False

    while line_idx < total_lines:
        raw_line = lines[line_idx].strip()
        line_idx += 1
        
        if not raw_line or raw_line.startswith('#'):
            continue
            
        if ' #' in raw_line:
            raw_line = raw_line.split(' #', 1)[0].strip()
            
        tokens = tokenize(raw_line)
        if not tokens:
            continue
            
        cmd = tokens[0]

        # 1. VARIABLE SYSTEM
        if cmd == "setup_var":
            var_name = tokens[1]
            remainder = raw_line.split(var_name, 1)[1].strip()
            variables[var_name] = parse_value(remainder)

        elif cmd == "write":
            remainder = raw_line.split('write', 1)[1].strip()
            print(parse_value(remainder))

        elif cmd == "input_var":
            var_name = tokens[1]
            prompt = parse_value(raw_line.split(var_name, 1)[1].strip())
            variables[var_name] = input(str(prompt))

        # 2. MATH ENGINE
        elif cmd == "math_var":
            var_name = tokens[1]
            op = tokens[2]
            mod_val = parse_value(tokens[3])
            if var_name in variables:
                if op == "+": variables[var_name] += mod_val
                elif op == "-": variables[var_name] -= mod_val
                elif op == "*": variables[var_name] *= mod_val
                elif op == "/": variables[var_name] /= mod_val

        # 3. TURTLE UI ENGINE
        elif cmd == "ui_init":
            turtle.setup(800, 600)
            turtle_screen = turtle.Screen()
            turtle_screen.title("Conary Graphical Engine Engine")
            t = turtle.Turtle()
            t.speed(0)

        elif cmd == "ui_bg_color":
            turtle.bgcolor(parse_value(tokens[1]))

        elif cmd == "ui_draw_square":
            size = int(parse_value(tokens[1]))
            color = parse_value(tokens[2])
            if t:
                t.color(color)
                t.begin_fill()
                for _ in range(4):
                    t.forward(size)
                    t.right(90)
                t.end_fill()

        elif cmd == "ui_move":
            if t:
                t.penup()
                t.goto(int(parse_value(tokens[1])), int(parse_value(tokens[2])))
                t.pendown()

        elif cmd == "ui_write":
            if t: t.write(parse_value(raw_line.split('ui_write', 1)[1].strip()), font=("Arial", 16, "bold"))

        elif cmd == "ui_clear":
            if t: t.clear()

        # 4. GAME UTILITIES
        elif cmd == "get_random":
            import random
            variables[tokens[1]] = random.randint(int(parse_value(tokens[2])), int(parse_value(tokens[3])))

        # 5. CUSTOM CONDITIONAL ARCHITECTURE
        elif cmd == "if" and tokens[2] == "meets" and tokens[3] == "condition":
            condition_met = evaluate_condition(tokens)
            
            if not condition_met:
                depth = 1
                while line_idx < total_lines and depth > 0:
                    next_line = lines[line_idx].strip()
                    next_tokens = tokenize(next_line)
                    
                    if next_line.startswith("if "): depth += 1
                    elif next_line.startswith("end_block"): depth -= 1
                    
                    elif next_line.startswith("otherwise if") and depth == 1:
                        if evaluate_condition(next_tokens[1:]):
                            line_idx += 1
                            break
                    
                    elif next_line.startswith("otherwise do") and depth == 1:
                        line_idx += 1
                        break
                        
                    line_idx += 1

        elif cmd == "otherwise" and tokens[1] == "if":
            depth = 1
            while line_idx < total_lines and depth > 0:
                next_line = lines[line_idx].strip()
                if next_line.startswith("if "): depth += 1
                elif next_line.startswith("end_block"): depth -= 1
                line_idx += 1

        elif cmd == "otherwise" and tokens[1] == "do":
            depth = 1
            while line_idx < total_lines and depth > 0:
                next_line = lines[line_idx].strip()
                if next_line.startswith("if "): depth += 1
                elif next_line.startswith("end_block"): depth -= 1
                line_idx += 1

        elif cmd == "loop_var":
            continue

        elif cmd == "end_block":
            continue

        # 6. SQL EMBEDDED ENGINE
        elif cmd == "db_connect":
            db_conn = sqlite3.connect(parse_value(tokens[1]))
            db_cursor = db_conn.cursor()
        elif cmd == "db_execute":
            stmt = raw_line.split('db_execute ', 1)[1]
            for var, val in variables.items():
                stmt = stmt.replace(f"${var}", str(val))
            if db_cursor: db_cursor.execute(stmt)
        elif cmd == "db_fetch":
            if db_cursor:
                for row in db_cursor.fetchall(): print(row)
        elif cmd == "db_close":
            if db_conn:
                db_conn.commit()
                db_conn.close()

    if turtle_screen:
        print("UI Rendering Complete. Click the window to close.")
        turtle_screen.exitonclick()

if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: conary <filename.cnry>")
    else: run_conary(sys.argv[1])

def main_cli():
    if len(sys.argv) < 2:
        print("Usage: conary <filename.cnry>")
    else:
        run_conary(sys.argv[1])

if __name__ == "__main__":
    main_cli()
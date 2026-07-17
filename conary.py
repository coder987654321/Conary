import sys
import os
import sqlite3

def run_conary(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    variables = {}
    db_conn = None
    db_cursor = None
    line_idx = 0
    is_initialized = False

    while line_idx < len(lines):
        line = lines[line_idx]
        if not line or line.startswith('#'):
            line_idx += 1
            continue

        tokens = line.split()
        cmd = tokens[0]

        if cmd == "initialConary":
            is_initialized = True
            line_idx += 1
            continue

        if not is_initialized:
            print(f"Runtime Error [Line {line_idx+1}]: Language not initialized. Add 'initialConary' at the top.")
            return

        # 1. Variables & Data Inputs
        if cmd == "setup_var":
            val_str = line.split(' ', 2)[2]
            variables[tokens[1]] = int(val_str) if val_str.isdigit() else val_str
            
        elif cmd == "input_var":
            var_name = tokens[1]
            prompt_text = " ".join(tokens[2:]).replace("_", " ") if len(tokens) > 2 else "> "
            variables[var_name] = input(prompt_text)

        elif cmd == "math_var":
            var_name, op, val = tokens[1], tokens[2], tokens[3]
            v_val = variables[val] if val in variables else int(val)
            if op == "+": variables[var_name] += v_val
            elif op == "-": variables[var_name] -= v_val
            elif op == "*": variables[var_name] *= v_val

        elif cmd == "write":
            target = tokens[1]
            if target in variables:
                print(variables[target])
            else:
                print(" ".join(tokens[1:]).replace("_", " "))

        # 2. SQL Database Commands
        elif cmd == "db_connect":
            db_name = tokens[1]
            db_conn = sqlite3.connect(db_name)
            db_cursor = db_conn.cursor()

        elif cmd == "db_execute":
            if not db_cursor:
                print(f"Database Error [Line {line_idx+1}]: No active connection.")
                return
            sql_query = line.split(' ', 1)[1]
            for var, val in variables.items():
                sql_query = sql_query.replace(f"${var}", str(val))
            db_cursor.execute(sql_query)
            db_conn.commit()

        elif cmd == "db_fetch":
            if not db_cursor: return
            rows = db_cursor.fetchall()
            for row in rows:
                print(row)

        elif cmd == "db_close":
            if db_conn:
                db_conn.close()

        # 3. Code Flow Control (If statements & Loops)
        elif cmd == "if_var":
            var_name, op, val = tokens[1], tokens[2], tokens[3]
            v_left = variables[var_name]
            v_right = variables[val] if val in variables else (int(val) if val.isdigit() else val)
            
            condition = False
            if op == ">" and int(v_left) > int(v_right): condition = True
            elif op == "<" and int(v_left) < int(v_right): condition = True
            elif op == "==" and str(v_left) == str(v_right): condition = True
            
            else_idx = next((i for i, l in enumerate(lines) if l.startswith("else_var")), len(lines))
            end_idx = next((i for i, l in enumerate(lines) if l.startswith("end_block")), len(lines))
            
            if condition:
                line_idx += 1; continue
            elif else_idx < end_idx:
                line_idx = else_idx + 1; continue
            else:
                line_idx = end_idx + 1; continue

        elif cmd == "loop_var":
            count = int(variables[tokens[1]]) if tokens[1] in variables else int(tokens[1])
            end_idx = next((i for i, l in enumerate(lines[line_idx:]) if l.startswith("end_block")), len(lines)) + line_idx
            loop_lines = lines[line_idx + 1:end_idx]
            
            for _ in range(count):
                for loop_line in loop_lines:
                    ltokens = loop_line.split()
                    if not ltokens: continue
                    if ltokens[0] == "write":
                        print(variables.get(ltokens[1], " ".join(ltokens[1:]).replace("_", " ")))
            line_idx = end_idx

        line_idx += 1

def main_cli():
    if len(sys.argv) > 1:
        run_conary(sys.argv[1])
    else:
        print("Conary Development Language Running. (High level and low level coding combined)")

if __name__ == "__main__":
    main_cli()
#!/usr/bin/env python3
import sys
import os
import sqlite3
import turtle
import re
import random

class ConaryEngine:
    def __init__(self):
        self.variables = {}
        self.screen = None
        self.pen = None
        self.ui_loop_callback = None
        self.in_ui_loop = False
        self.db_conn = None
        self.db_cursor = None
        self.init_database()

    def init_database(self):
        # Automatically connects to a local runtime database for your storage commands
        try:
            self.db_conn = sqlite3.connect("conary_runtime.db")
            self.db_cursor = self.db_conn.cursor()
            self.db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS storage (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            self.db_conn.commit()
        except Exception as e:
            print(f"Database Warning: Could not initialize local storage backend: {e}")

    def parse_and_run(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)

        cleaned_lines = [line.strip() for line in lines]
        self.execute_block(cleaned_lines)

        # If an initialUI graphics loop block was registered, boot up the main Turtle loop
        if self.ui_loop_callback and self.screen:
            self.in_ui_loop = True
            self.run_ui_loop()
            turtle.done()

    def execute_block(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i]
            if not line or line.startswith('#'):
                i += 1
                continue

            # Standard regex token splitting to keep quotes intact
            parts = re.findall(r'[^"\s]+|"[^"]*"', line)
            if not parts:
                i += 1
                continue
                
            cmd = parts[0]

            # 1. CORE LOGIC / VARIABLE COMMANDS
            if cmd == "setup_var":
                name = parts[1]
                val = " ".join(parts[2:])
                self.variables[name] = self.evaluate_value(val)

            elif cmd == "math_var":
                name = parts[1]
                op = parts[2]
                val = self.evaluate_value(" ".join(parts[3:]))
                if name in self.variables:
                    if op == "+": self.variables[name] += val
                    elif op == "-": self.variables[name] -= val
                    elif op == "*": self.variables[name] *= val
                    elif op == "/": self.variables[name] /= val

            elif cmd == "get_random":
                name = parts[1]
                low = int(self.evaluate_value(parts[2]))
                high = int(self.evaluate_value(parts[3]))
                self.variables[name] = random.randint(low, high)

            elif cmd == "write":
                content = " ".join(parts[1:])
                print(self.evaluate_value(content))

            # 2. TURTLE UI GRAPHICS COMMANDS
            elif cmd == "ui_init":
                w = int(self.evaluate_value(parts[1]))
                h = int(self.evaluate_value(parts[2]))
                self.screen = turtle.Screen()
                self.screen.setup(w, h)
                self.screen.title("Conary Arcade Engine")
                self.pen = turtle.Turtle()
                self.pen.speed(0)
                self.pen.hideturtle()
                self.pen.penup()

            elif cmd == "ui_bg_color":
                color = self.evaluate_value(" ".join(parts[1:])).strip('"')
                if self.screen:
                    self.screen.bgcolor(color)

            elif cmd == "ui_move":
                x = int(self.evaluate_value(parts[1]))
                y = int(self.evaluate_value(parts[2]))
                if self.pen:
                    self.pen.goto(x, y)

            elif cmd == "ui_draw_square":
                size = int(self.evaluate_value(parts[1]))
                color = self.evaluate_value(" ".join(parts[2:])).strip('"')
                if self.pen:
                    self.pen.pendown()
                    self.pen.fillcolor(color)
                    self.pen.begin_fill()
                    for _ in range(4):
                        self.pen.forward(size)
                        self.pen.left(90)
                    self.pen.end_fill()
                    self.pen.penup()

            elif cmd == "ui_write":
                text = str(self.evaluate_value(parts[1])).strip('"')
                color = self.evaluate_value(" ".join(parts[2:])).strip('"')
                if self.pen:
                    current_color = self.pen.pencolor()
                    self.pen.pencolor(color)
                    self.pen.write(text, font=("Courier", 16, "normal"))
                    self.pen.pencolor(current_color)

            # 3. CONTROL BLOCK / LOOP ROUTING
            elif cmd == "initialUI":
                block_lines = []
                depth = 1
                i += 1
                while i < len(lines):
                    if lines[i].startswith("initialUI") or lines[i].startswith("if "):
                        depth += 1
                    elif lines[i] == "end_block":
                        depth -= 1
                        if depth == 0:
                            break
                    block_lines.append(lines[i])
                    i += 1
                self.ui_loop_callback = block_lines
                continue

            elif cmd == "if":
                var_name = parts[1]
                op = parts[4]
                target_val = self.evaluate_value(parts[5])
                
                block_lines = []
                i += 1
                while i < len(lines) and lines[i] != "end_block":
                    block_lines.append(lines[i])
                    i += 1
                
                var_val = self.variables.get(var_name, 0)
                condition_met = False
                if op == "==" and var_val == target_val: condition_met = True
                elif op == ">" and var_val > target_val: condition_met = True
                elif op == "<" and var_val < target_val: condition_met = True
                
                if condition_met:
                    self.execute_block(block_lines)
                continue

            i += 1

    def run_ui_loop(self):
        if self.in_ui_loop and self.ui_loop_callback:
            if self.pen:
                self.pen.clear()
            self.execute_block(self.ui_loop_callback)
            if self.screen:
                self.screen.ontimer(self.run_ui_loop, 33) # ~30 FPS frame rate timing target

    def evaluate_value(self, val_str):
        val_str = val_str.strip()
        if val_str.startswith('"') and val_str.endswith('"'):
            return val_str.strip('"')
        if val_str in self.variables:
            return self.variables[val_str]
        try:
            if '.' in val_str: return float(val_str)
            return int(val_str)
        except ValueError:
            return val_str

    def __del__(self):
        if self.db_conn:
            self.db_conn.close()

def main_cli():
    if len(sys.argv) < 2:
        print("Usage: conary <filename.cnry>")
        sys.exit(1)
    engine = ConaryEngine()
    engine.parse_and_run(sys.argv[1])

if __name__ == "__main__":
    main_cli()
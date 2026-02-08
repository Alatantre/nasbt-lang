import sys
from random import randint
from datetime import datetime, time

VERSION = "NASBT V1.0 — TURTLE (RELEASE)"

class NasbtError(Exception):
    pass

def is_number(*x):
    try:
        for i in x:
            int(i)
        return True
    except ValueError:
        return False

instrs = (
    ( # NO ARG INSTRUCTIONS
        "POP",
        "REMOVE",
        "TOP",
        "BOTTOM",
        "INPUT",
        "OUTPUT",
        "CLEAR",
        "INCREMENT",
        "DECREMENT",
        "LENGTH",
        "STACK",
        "TELEPORT",
        "HALT"
    ),
    ( # SINGLE ARG INSTRUCTIONS
        ( # NUMBER BASED ARGS
            "PUSH",
        ),
        ( # TEXT BASED ARGS
            "MOVE",
            "MESSAGE",
            "ERROR"
        )
    ),
    ( # MULTIPLE ARG INSTRUCTIONS
        "JUMP",
        "RAND"
    )
)

# this shit is messy af i swear
def parse(file):
    with open(file, "r") as f:
        contents = f.read()
    
    if contents:
        lines = contents.splitlines()
    else:
        print("\n---PROGRAM FINISHED---")
        sys.exit(1)
    
    parsed = {}
    for i, line in enumerate(lines, 1):
        parts = line.split(" ", 1)
        parts.append(None)
        instr = parts[0]
        arg = parts[1]
        
        if instr in instrs[0]:
            parsed[i] = (instr, None)
        elif line.startswith(";"):
            parsed[0] = (line, None)
        elif instr in instrs[1][0]:
            if is_number(arg):
                parts_a = [instr, int(arg)]
                parsed[i] = tuple(parts_a)
            else:
                if instr == "PUSH":
                    raise NasbtError(f"ARGUMENT FOR PUSH IS A NON-NUMBER: {arg}")
        elif instr in instrs[1][1]:
            if instr == "MOVE":
                if arg == "LEFT" or arg == "RIGHT":
                    pass
                else:
                    raise NasbtError(f"ARGUMENT FOR MOVE IS INVALID: {arg}")
                    
            parsed[i] = (instr, parts[1], None)
        elif instr in instrs[2]:
            parts_b = arg.split(" ")
            if instr == "JUMP":
                if len(parts) == 3 and is_number(parts[1]):
                    parsed[i] = (instr, int(parts[1]), None)
                elif len(parts) == 3 and is_number(parts_b[0], parts_b[2]):
                    if not parts_b[1] in ("IF", "IFNOT"):
                        raise NasbtError(f"INVALID CONDITION FOR JUMP: {parts_b[1]}")
                    else:
                        parsed[i] = (instr, int(parts_b[0]), parts_b[1], int(parts_b[2]), None)
                else:
                    if len(parts) == 1:
                        raise NasbtError("ARGUMENTS FOR JUMP MISSING, EXPECTED AT LEAST 1")
                    else:
                        for part in parts_b:
                            if part != "IF" or part != "IFNOT":
                                if not is_number(part):
                                    raise NasbtError(f"INVALID ARG FOR JUMP: {part}")
            
    return parsed

def execute(parsed_lines):
    stack = []
    ptr = 0
    ip = 1
    max_line = max(parsed_lines.keys())
    
    while ip <= max_line:
        parts = parsed_lines[ip]
        instr = parts[0].upper()
        try:
            # CORE/BASIC INSTRUCTIONS
            if instr == "PUSH":
                stack.append(parts[1])
            elif instr == "POP":
                if stack:
                    stack.pop()
                else:
                    raise NasbtError("TRIED TO POP A VALUE WHEN STACK WAS EMPTY")
            elif instr == "REMOVE":
                if stack:
                    stack.pop(ptr)
                else:
                    raise NasbtError("TRIED TO REMOVE A VALUE WHEN STACK WAS EMPTY")
            elif instr == "CLEAR":
                stack.clear()
            elif instr == "INPUT":
                user_input = input()
                
                if user_input:
                    for char in user_input:
                        stack.append(ord(char))
            elif instr == "OUTPUT":
                if stack:
                    print(chr(stack[ptr]), end="", flush=True)
            elif instr == "MESSAGE":
                print(parts[1], end="", flush=True)
            elif instr == "INCREMENT":
                if stack:
                    stack[ptr] += 1
            elif instr == "DECREMENT":
                if stack:
                    stack[ptr] -= 1
            elif instr == "STACK":
                print(stack, end="", flush=True)
            
            # POINTER MOVEMENT
            elif instr == "MOVE":
                if parts[1] == "LEFT":
                    ptr = (ptr - 1) % len(stack)
                elif parts[1] == "RIGHT":
                    ptr = (ptr + 1) % len(stack)
            elif instr == "TOP":
                if stack:
                    ptr = len(stack) - 1
            elif instr == "BOTTOM":
                ptr = 0
            elif instr == "TELEPORT":
                ptr = stack[ptr] % len(stack)
            
            # CONTROL FLOW
            elif instr == "JUMP":
                target_line = int(parts[1])
                
                if target_line < 1:
                    target_line = 1
                elif target_line > max_line:
                    target_line = max_line
                
                if len(parts) == 3:
                    ip = target_line
                    continue
                elif len(parts) == 5:
                    condition = (parts[2], int(parts[3]))
                    
                    if condition[0] == "IF":
                        if condition[1] == stack[ptr]:
                            ip = target_line
                            continue
                    elif condition[0] == "IFNOT":
                        if condition[1] != stack[ptr]:
                            ip = target_line
                            continue
            elif instr == "ERROR":
                raise NasbtError(parts[1])
            elif instr == "HALT":
                print(f"\n---PROGRAM HALTED IN LINE {ip}---")
                break
            
            # OTHER
            elif instr == "RAND":
                min_ = parts[1]
                max_ = parts[2]
                try:
                    stack.append(min_, max_)
                except ValueError:
                    stack.append(min_, max_)
            elif instr == "INSTRUCTION": # most useful instr oat
                pass
            elif instr.startswith(";"):
                pass
            
            ip += 1
        except NasbtError as e:
            print(f"ERROR IN LINE {ip}: {e}")
            break
        except KeyboardInterrupt:
            print("\n---PROGRAM HALTED---")
            break
    else:
        print("\n---PROGRAM FINISHED---")

def main(argv):
    if len(argv) < 2:
        print("USAGE: python nasbt.py <filename>.nasbt")
        sys.exit(1)
    if argv[1]:
        if argv[1] == "--version":
            print(VERSION)
        else:
            try:
                execute(parse(argv[1]))
            except FileNotFoundError:
                print("FILE NOT FOUND")
            except PermissionError:
                print("PERMISSION DENIED")
            except NasbtError as e:
                print(e)

if __name__ == "__main__":
    main(sys.argv)

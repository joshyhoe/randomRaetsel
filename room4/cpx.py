#!/usr/bin/env python3
import sys
import struct
import os

# ------------------------------------------------------------
# Register Setup
# ------------------------------------------------------------

REG_COUNT = 16
REG_DIR = "registers/"
registers = [0] * REG_COUNT

def load_registers():
    for i in range(REG_COUNT):
        path = os.path.join(REG_DIR, f"x{i}.bin")
        if os.path.exists(path):
            with open(path, "rb") as f:
                registers[i] = struct.unpack(">I", f.read())[0]
        else:
            registers[i] = 0

def save_registers():
    for i in range(REG_COUNT):
        path = os.path.join(REG_DIR, f"x{i}.bin")
        with open(path, "wb") as f:
            f.write(struct.pack(">I", registers[i] & 0xFFFFFFFF))

load_registers()

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def reg_index(token):
    if not token.startswith("x"):
        raise ValueError(f"Invalid register name: {token}")
    idx = int(token[1:])
    if idx < 0 or idx >= REG_COUNT:
        raise ValueError(f"Register index out of range: {token}")
    return idx

# ------------------------------------------------------------
# Instruction Handlers
# ------------------------------------------------------------

def instr_add(dst, src):
    di = reg_index(dst)
    si = reg_index(src)
    registers[di] = (registers[di] + registers[si]) & 0xFFFFFFFF

def instr_sub(dst, src):
    di = reg_index(dst)
    si = reg_index(src)
    registers[di] = (registers[di] - registers[si]) & 0xFFFFFFFF

def instr_sll(src, dst, shift_reg):
    si = reg_index(src)
    di = reg_index(dst)
    shi = reg_index(shift_reg)
    shift_amount = registers[shi] & 31
    registers[di] = (registers[si] << shift_amount) & 0xFFFFFFFF

def instr_srl(src, dst, shift_reg):
    si = reg_index(src)
    di = reg_index(dst)
    shi = reg_index(shift_reg)
    shift_amount = registers[shi] & 31
    registers[di] = (registers[si] >> shift_amount) & 0xFFFFFFFF

def instr_shw(src):
    si = reg_index(src)
    print(registers[si])

# ------------------------------------------------------------
# Program Execution
# ------------------------------------------------------------

def execute(program_lines):
    line_number = 0
    while line_number < len(program_lines):
        line = program_lines[line_number].strip()
        if not line or line.startswith("#"):
            line_number += 1
            continue

        parts = line.split()
        cmd = parts[0]

        try:
            if cmd == "add":
                instr_add(parts[1], parts[2])
            elif cmd == "sub":
                instr_sub(parts[1], parts[2])
            elif cmd == "sll":
                instr_sll(parts[1], parts[2], parts[3])
            elif cmd == "srl":
                instr_srl(parts[1], parts[2], parts[3])
            elif cmd == "shw":
                instr_shw(parts[1])
            elif cmd == "halt":
                save_registers()
                return
            else:
                raise ValueError(f"Unknown instruction: {cmd}")

        except Exception as e:
            print(f"ERROR at line {line_number+1}: '{line}' -> {e}")
            save_registers()
            return

        line_number += 1

       save_registers()

# ------------------------------------------------------------
# Entry
# ------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage: cpx.py pseudo_assembly_file")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        program_lines = f.readlines()
    execute(program_lines)

if __name__ == "__main__":
    main()

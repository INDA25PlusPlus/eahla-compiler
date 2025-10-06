import sys
from tokenizer import tokenize
from parser import parse, print_AST_info, print_pretty_AST
from nhg_compiler import compile_to_nhg
from cpp_compiler import compile_to_cpp

# input file, code copied from: https://www.tutorialspoint.com/How-to-read-a-file-from-command-line-using-Python
if len(sys.argv) < 3:
    print("Missing input file argument. Usage: python3 main.py <source_filename> <output_filename>")
    sys.exit(1)

# read source file contents
source = sys.argv[1]

try:
    with open(source, 'rb') as file:
        program = file.read()
except FileNotFoundError:
    print(f"Error: File '{source}' not found.")
    sys.exit(1)
except IOError:
    print(f"Error: Cannot read file '{source}'.")
    sys.exit(1)

# tokenize source file contents
tokens = tokenize(program)
# print('tokens:', tokens)

# parse/build syntax tree from tokens
tree = parse(tokens)
# print_pretty_AST(tree)

# compile to c++ or nhg
# compile_to_cpp(tree, sys.argv[2])
compile_to_nhg(tree, sys.argv[2])

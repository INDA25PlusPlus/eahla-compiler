import sys
from tokenizer import tokenize
from parser import parse, print_AST_info, print_pretty_AST
from nhg_compiler import compile_to_nhg
from cpp_compiler import compile_to_cpp

# input file, code copied from: https://www.tutorialspoint.com/How-to-read-a-file-from-command-line-using-Python
if len(sys.argv) < 4:
    print("Missing argument/-s. Usage: python3 main.py <'c++' or 'nhg'> <source_filename> <output_filename>")
    sys.exit(1)

# read source file contents
source = sys.argv[2]

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
print_pretty_AST(tree)

# compile to c++ or nhg
if sys.argv[1] == "c++":
    compile_to_cpp(tree, sys.argv[3])
elif sys.argv[1] == "nhg":
    compile_to_nhg(tree, sys.argv[3])
else:
    print(f"Error: Cannot compile to '{sys.argv[1]}'. Change to 'c++' or 'nhg'.")

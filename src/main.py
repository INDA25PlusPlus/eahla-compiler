import sys

# input file, code copied from: https://www.tutorialspoint.com/How-to-read-a-file-from-command-line-using-Python
if len(sys.argv) < 3:
    print("Missing input file argument. Usage: (python3) main.py <source_filename> <output_filename>")
    sys.exit(1)

source_code = sys.argv[1]

try:
    with open(source_code, 'rb') as file:
        program = file.read()
except FileNotFoundError:
    print(f"Error: File '{source_code}' not found.")
    sys.exit(1)
except IOError:
    print(f"Error: Cannot read file '{source_code}'.")
    sys.exit(1)

# program = b"a = 0; b = 1; i = 0; while i < 10 { i = i + 1; print a; c = b; b = a + b; a = c; }; " # fibonacci (first 10)
# program = b"a = 10; sum = 1; i = 1; while i < a { i = i + 1; prev = sum; j = 1; while j < i { j = j + 1; sum = sum + prev; }; }; print sum; " # factorial (of a)
# program = b"i = 0; while i < 1 { a = i; i = i + 1; }; print a; " # test scope # is this program even valid? language in and out should be different so yes. but now boring fix.

def is_letter(ch):
    if (b'a'[0] <= ch[0] <= b'z'[0]) or (b'A'[0] <= ch[0] <= b'Z'[0]) or (ch == b'_'):
        return True
    return False

def is_number(ch):
    if (b'0'[0] <= ch[0] <= b'9'[0]):
        return True
    return False

# first tokenize (like make nodes, make it like I already think it is, grouping)
tokens = []
i = 0
while i < len(program):
    # print("while!, i:", i)
    ch = program[i:i+1]
    # print("char! :", ch)

    if ch == b' ':
        i += 1
        continue
    
    elif is_letter(ch): # case name
        j = i + 1
        while j < len(program):
            if not is_letter(program[j:j+1]):
                break
            j += 1
        name = program[i:j]
        i = j - 1

        if name == b"while":
            tokens.append(("while", "while"))
        elif name == b"print":
            tokens.append(("print", "print"))
        else:
            tokens.append(("variable", name.decode()))
            
    elif is_number(ch):
        j = i + 1
        while j < len(program):
            if not is_number(program[j:j+1]):
                break
            j += 1
        number = program[i:j]
        i = j - 1

        tokens.append(("number", number.decode()))

    elif ch == b'=' or ch == b'<' or ch == b'}' or ch == b'+' or ch == b';' or ch == b'{':
        tokens.append((ch.decode(), ch.decode()))

    else:
        print("What is this!!??", ch)
    
    i += 1

# print(tokens)

# then parse
def add_to_tree(node_kind, parent):
    # node_kind: string, parent: int, children: int[]
    tree.append((node_kind, parent, []))
    if parent != -1:
        tree[parent][2].append(len(tree) - 1) # update parent children info
    return len(tree) - 1

tree = []

def rec_parse(current_case, token_to_parse, parent_node):
    # global tree? reference pass? python, no need hm

    match current_case:
        case "statement_list": # <statement_list> ::= <statement> "; " | <statement> "; " <statement_list>
            # top node or while_do
            node = add_to_tree(["statement_list"], parent_node)
            # depth first build
            while token_to_parse < len(tokens):
                # skip ;
                if tokens[token_to_parse][1] == ';':
                    token_to_parse += 1
                    continue
                if tokens[token_to_parse][1] == '}':
                    return token_to_parse + 1
                token_to_parse = rec_parse("statement", token_to_parse, node)
            return token_to_parse
        case "statement": # <statement> ::= <assignment> | <control> | <print>
            # assignment if var =
            # control if while
            # print if print
            # call rec with correct, let it make node
            if tokens[token_to_parse][0] == "while":
                return rec_parse("control", token_to_parse, parent_node)
            elif tokens[token_to_parse][0] == "print":
                return rec_parse("print", token_to_parse, parent_node)
            else:
                # assignment
                return rec_parse("assignment", token_to_parse, parent_node)
        case "assignment":
            # <assignment> ::= <name> " = " <expr> | <name> " = " <expr> " + " <expr>
            # + should be a node. is a token? each token should be case?
            # assignment node
            node = add_to_tree(["assignment"], parent_node)

            token_to_parse = rec_parse("variable", token_to_parse, node)
            token_to_parse += 1 # skip =

            if tokens[token_to_parse + 1][1] == '+':
                token_to_parse += 1 # go to +
                token_to_parse = rec_parse("+", token_to_parse, node)
            else:
                token_to_parse = rec_parse("expr", token_to_parse, node)
            return token_to_parse
        case "control":
            node = add_to_tree(["while"], parent_node)
            token_to_parse += 2 # jump to <
            token_to_parse = rec_parse("condition", token_to_parse, node)
            token_to_parse += 1 # skip {
            return rec_parse("statement_list", token_to_parse, node)
        case "print":
            node = add_to_tree(["print"], parent_node)
            return rec_parse("expr", token_to_parse + 1, node)
        case "condition":
            node = add_to_tree(["condition", '<'], parent_node)
            rec_parse("expr", token_to_parse - 1, node)
            return rec_parse("expr", token_to_parse + 1, node)
        case "expr":
            add_to_tree(tokens[token_to_parse], parent_node) # well
            return token_to_parse + 1
        case "number":
            add_to_tree(["number", tokens[token_to_parse][1]], parent_node)
            return token_to_parse + 1
        # case "trailing_numbers":
        #     ...
        # case "name": # always variable
        #     ...
        # case "letter":
        #     ...
        case "+":
            node = add_to_tree(["+", "+"], parent_node)
            rec_parse("expr", token_to_parse - 1, node)
            rec_parse("expr", token_to_parse + 1, node)
            return token_to_parse + 2
        case "variable": # hm
            add_to_tree(["variable", tokens[token_to_parse][1]], parent_node)
            return token_to_parse + 1

rec_parse("statement_list", 0, -1)

# info tree
# for i in range(len(tree)):
#     print("node", i, ":", tree[i])

# prettier tree
def dfs(node, depth):
    print(node, end=' ')
    print(" "*(depth*4), end=' ')
    # print("node", node, ":", tree[node])
    print(tree[node][0])
    for child in tree[node][2]:
        dfs(child, depth + 1)

# print("syntax tree:")
# print()
# dfs(0, 0)

# "compile"/translate
cpp_code = b'#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n'
cpp_code_add_to_start = b""
cpp_code_end = b'}'

initialized_vars = [] # how handle scopes? todo!? # (currently(?)) only in assignments

def dfs_compile_to_cpp(node):
    global cpp_code_add_to_start
    # print(tree[node][0][0])
    match tree[node][0][0]:
        case "statement_list":
            ret = b""
            for kid in tree[node][2]:
                ret += dfs_compile_to_cpp(kid)
            return ret
        case "assignment":
            # add int (or ?) if first occurence
            # always (currently) 2 kids
            # (int?) var = kid2
            if tree[tree[node][2][0]][0][1] not in initialized_vars:
                cpp_code_add_to_start += b"long long " + tree[tree[node][2][0]][0][1].encode() + b";\n"
                initialized_vars.append(tree[tree[node][2][0]][0][1])
            return dfs_compile_to_cpp(tree[node][2][0]) + b" = " + dfs_compile_to_cpp(tree[node][2][1]) + b";\n"
            # todo! name can be string
        case "while":
            # while (<condition>) {<sl>}
            return b"while (" + dfs_compile_to_cpp(tree[node][2][0]) + b") {\n" + dfs_compile_to_cpp(tree[node][2][1]) + b"}\n"
        case "print":
            # cout << <expr> << endl;
            return b"cout << " + dfs_compile_to_cpp(tree[node][2][0]) + b" << endl;\n"
        case "condition":
            return dfs_compile_to_cpp(tree[node][2][0]) + tree[node][0][1].encode() + dfs_compile_to_cpp(tree[node][2][1])
        case "+":
            return dfs_compile_to_cpp(tree[node][2][0]) + tree[node][0][1].encode() + dfs_compile_to_cpp(tree[node][2][1])
        case "variable":
            return tree[node][0][1].encode()
        case "number":
            return tree[node][0][1].encode()
        case _:
            print("waaa!", node)

def compile_to_cpp():
    main_code = dfs_compile_to_cpp(0)
    # https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file
    with open(sys.argv[2], "w") as f:
      print((cpp_code + cpp_code_add_to_start + main_code + cpp_code_end).decode(), file=f)


def dfs_compile_to_nhg(node):
    # print(tree[node][0][0])
    match tree[node][0][0]:
        case "statement_list":
            ret = b""
            for kid in tree[node][2]:
                ret += dfs_compile_to_nhg(kid)
            return ret
        case "assignment":
            # always (currently) 2 kids?
            return b"The " + dfs_compile_to_nhg(tree[node][2][0]) + b" transforms into " + dfs_compile_to_nhg(tree[node][2][1]) + b".\n"
            # todo! name can be string
        case "while":
            # or # > enter <place> while
            # and # > leave <place>
            # while (<condition>) {<sl>}
            return b"The story continues as long as " + dfs_compile_to_nhg(tree[node][2][0]) + b" remains true.\n" + dfs_compile_to_nhg(tree[node][2][1]) # !?
        case "print":
            return b"You speak of " + dfs_compile_to_nhg(tree[node][2][0]) + b".\n"
        case "condition":
            return dfs_compile_to_nhg(tree[node][2][0]) + b" stands before " + dfs_compile_to_nhg(tree[node][2][1])
        case "+":
            return b"You reflect on all you have learned: " + dfs_compile_to_nhg(tree[node][2][0]) + b" and " + dfs_compile_to_nhg(tree[node][2][1])
        case "variable":
            return tree[node][0][1].encode()
        case "number":
            if tree[node][0][1] == '0':
                return b"nothing"
            if tree[node][0][1] == '1':
                return b"everything"
            return tree[node][0][1].encode()
        case _:
            print("waaa!", node)

def compile_to_nhg():
    nhg_start_code = b"The adventure begins.\n\n"
    nhg_code_body = dfs_compile_to_nhg(0)
    nhg_end_code = b"\nThe adventure ends.\n"
    # https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file
    with open(sys.argv[2], "w") as f:
        print((nhg_start_code + nhg_code_body + nhg_end_code).decode(), file=f)

# compile to_cpp()
compile_to_nhg()

# print()
# print()
# print("c++ code:")
# print()
# print((cpp_code + cpp_code_add_to_start + main_code + cpp_code_end).decode())
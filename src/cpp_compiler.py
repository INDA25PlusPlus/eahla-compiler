def compile_to_cpp(tree, output_file):
    # "compile"/translate
    cpp_code = b'#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n'
    cpp_code_add_to_start = b""
    cpp_code_end = b'}'

    initialized_vars = [] # how handle scopes? todo!? # (currently(?)) only in assignments

    def dfs_compile_to_cpp(node):
        nonlocal cpp_code_add_to_start
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

    main_code = dfs_compile_to_cpp(0)
    # https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file
    with open(output_file, "w") as f:
      print((cpp_code + cpp_code_add_to_start + main_code + cpp_code_end).decode(), file=f)
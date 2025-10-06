def compile_to_nhg(tree, output_file):
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

    nhg_start_code = b"The adventure begins.\n\n"
    nhg_code_body = dfs_compile_to_nhg(0)
    nhg_end_code = b"\nThe adventure ends.\n"
    # https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file
    with open(output_file, "w") as f:
        print((nhg_start_code + nhg_code_body + nhg_end_code).decode(), file=f)
# then parse
def parse(tokens):
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

    return tree


# info tree
def print_AST_info(tree):
    for i in range(len(tree)):
        print("node", i, ":", tree[i])

def print_pretty_AST(tree):
    # prettier tree
    def dfs(node, depth):
        print(node, end=' ')
        print(" "*(depth*4), end=' ')
        # print("node", node, ":", tree[node])
        print(tree[node][0])
        for child in tree[node][2]:
            dfs(child, depth + 1)
    
    print("syntax tree:")
    print()
    dfs(0, 0)
def is_letter(ch):
    if (b'a'[0] <= ch[0] <= b'z'[0]) or (b'A'[0] <= ch[0] <= b'Z'[0]) or (ch == b'_'):
        return True
    return False

def is_number(ch):
    if (b'0'[0] <= ch[0] <= b'9'[0]):
        return True
    return False

# first tokenize (like make nodes, make it like I already think it is, grouping)
def tokenize(program):
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
    
    return tokens
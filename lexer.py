import sys
variables = dict()

progname = sys.argv[1]
with open(progname, "r") as f:
    code = f.read().replace("\n", ";.").replace(" ", "")

i = 0
lex = []
cur = ''
while i < len(code):
    char = code[i]
    cur += char
    while cur.isalpha():
        i += 1
        cur += code[i]

    while cur.isdigit():
        i += 1
        cur += code[i]

    char = cur[-1]
    cur = cur[:-1]

    if any(x == cur for x in ['int', 'float', 'bool', 'print', 'input', 'if', 'while', 'else', 'or', 'and', 'not']):
        lex.append(cur)
    else:
        if cur.startswith("int"):
            lex.append("int")
            lex.append(cur[3:])
            variables[cur[3:]] = None
        elif cur.startswith("float"):
            lex.append("float")
            lex.append(cur[5:])
            variables[cur[5:]] = None
        elif cur.startswith("bool"):
            lex.append("bool")
            lex.append(cur[4:])
            variables[cur[4:]] = None
        elif cur.startswith("or"):
            lex.append("or")
            lex.append(cur[2:])
        elif cur.startswith("and"):
            lex.append("and")
            lex.append(cur[3:])
        elif cur.startswith("not"):
            lex.append("not")
            lex.append(cur[3:])
        else:
            lex.append(cur)
            if cur.isalpha():
                variables[cur] = None

    if char in '{}!=.-+/*(),;:%><':
        if char == ':' and i < len(code) - 1 and code[i + 1] == '=':
            lex.append(':=')
            flag = True
        elif char == '=' and i < len(code) - 1 and code[i + 1] == '=':
            lex.append('==')
            flag = True
        elif char == '<' and i < len(code) - 1 and code[i + 1] == '=':
            lex.append('<=')
            flag = True
        elif char == '>' and i < len(code) - 1 and code[i + 1] == '=':
            lex.append('>=')
            flag = True
        elif char == '!' and i < len(code) - 1 and code[i + 1] == '=':
            lex.append('!=')
            flag = True
        elif char == ';' and i < len(code) - 1 and code[i + 1] == '.':
            lex.append(';.')
            flag = True
        else:
            lex.append(char)
            i -= 1
        i += 1
    else:
        if char.isalpha():
            i -= 1

    i += 1
    cur = ''

lex = list(filter(lambda x: x, lex))
special = lex.copy()
lex = list(filter(lambda x: x != ";.", lex))
lex.append("☀")
# print(lex)

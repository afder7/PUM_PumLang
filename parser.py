from lexer import lex, variables, progname, special

priority = {'not': 5,
            'and': 4,
            'or': 3,
            '<=': 2,
            '!=': 2,
            '==': 2,
            '>': 2,
            '>=': 2,
            '<': 2,
            ':=': 1,
            'int': 0,
            'bool': 0,
            'float': 0,
            'input': 0,
            'print': 0,
            'if': 0,
            'else': 0,
            'while': 0,
            '(': 6,
            '+': 7,
            '-': 8,
            '*': 9,
            '/': 10,
            '%': 10,
            '//': 10,
            '^': 11,
            '~': 12}
# parser

i = 0
postfix = []
parstack = []

Operators = {"+", "-", "*", "/", "//", "%", ">", "<", ">=", "<=", "==", "!=", "or", "and", "not"}

Priority = {"or": 4, "and": 5, "not": 6, ">": 3, "<": 3, ">=": 3, "<=": 3, "==": 3, "!=": 3, "+": 0, "-": 0, "*": 1,
            "/": 1, "//": 1, "%": 1, ")": 2, "(": 2}


def toPostfix(infix):
    stack = []
    postfix = []

    for c in infix:
        if c not in Operators:
            postfix.append(c)
        else:
            if c == ")":
                stack.append(c)
            elif c == "(":
                operator = stack.pop()
                while not operator == ")":
                    postfix.append(operator)
                    operator = stack.pop()
            else:
                while stack and Priority[c] >= Priority[stack[-1]]:
                    postfix.append(stack.pop())
                stack.append(c)

    while stack:
        postfix.append(stack.pop())
    return list(filter(lambda x: x not in "()", postfix))


def P():
    global i

    B()
    if lex[i] != "☀":
        print(f"Program ended without sun symbol: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in FIle {progname}")
        exit()


def B():
    global i

    if lex[i] != "{":
        print(f"No brace before the start of the new block: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
        exit()

    i += 1

    try:
        lex.index("}", i)
    except ValueError:
        print(f"No ending brace for this block: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
        exit()

    while lex[i] != "}":
        S()

    i += 1
    if lex[i] != ";" and lex[i] != "☀":
        print(f"No semicolon in the end of the block: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
        exit()

    # i += 1


def S():
    global i, parstack, postfix

    if lex[i] not in variables:
        parstack.append(lex[i])

    e = []

    if lex[i] == "int" or lex[i] == "float" or lex[i] == "bool":

        i += 1
        while i < len(lex):
            if lex[i] == ":=":
                e.append(lex[i - 1])
                i += 1

                strt = i
                E()
                expr = lex[strt:i]
                e += toPostfix(expr)

                e.append(":=")
            if lex[i] == ";":
                break
            if lex[i] != ",":
                postfix.append(lex[i])
                IKR()
            i += 1

        postfix.append(parstack.pop(-1))
        postfix += e
    elif lex[i] in variables:

        postfix.append(lex[i])

        i += 1
        if lex[i] != ":=":
            print(f"Invalid variable operation:  String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()

        if lex[i] not in [";", ")", "}"]:
            parstack.append(lex[i])
            nst = []
            for u in parstack:
                if priority[u] > priority[lex[i]]:
                    postfix.append(u)
                else:
                    nst.append(u)
            parstack = nst.copy()
        elif lex[i] == ")" and "(" in parstack:
            postfix.extend(parstack[parstack.index("(") + 1:])
            parstack = parstack[:parstack.index(")")]
        i += 1

        strt = i
        E()
        expr = lex[strt:i]
        postfix += toPostfix(expr)

        postfix.append(parstack.pop(-1))
    elif lex[i] == "while":

        i += 1
        if lex[i] != "(":
            print(f"Invalid use of while: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()
        i += 1

        es = len(postfix)
        strt = i
        E()
        expr = lex[strt:i]
        postfix += toPostfix(expr)
        gt = len(postfix)

        if lex[i] != ")":
            print(f"Invalid use of while: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()

        postfix.append(parstack.pop(-1))
        i += 1
        B()

        postfix.append(es)
        postfix.append('goto')

        postfix = postfix[:gt] + [len(postfix) + 1] + postfix[gt:]
    elif lex[i] == "if":

        i += 1
        if lex[i] != "(":
            print(f"Invalid use of if: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()
        i += 1

        es = len(postfix)
        strt = i
        E()
        expr = lex[strt:i]
        postfix += toPostfix(expr)
        gt = len(postfix)

        if lex[i] != ")":
            print(f"Invalid use of if: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()

        postfix.append(parstack.pop(-1))
        i += 1
        B()

        i += 1

        if lex[i] != "else":
            i -= 1

            postfix = postfix[:gt] + [len(postfix) + 1] + postfix[gt:]
        else:
            postfix = postfix[:gt] + [len(postfix) + 3] + postfix[gt:]

            postfix.append("else")
            i += 1
            B()

            postfix = postfix[:gt + 1] + [len(postfix) + 1] + postfix[gt + 1:]
    elif lex[i] == "input":
        i += 1
        try:
            if lex[i] != "(":
                print(f"Invalid use of input function: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
                exit()
        except IndexError:
            print(f"Invalid use of input function: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()

        i += 1
        postfix.append(lex[i])
        IKR()
        i += 1

        if lex[i] != ")":
            print(f"Invalid use of input function: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()
        i += 1

        postfix.append(parstack.pop(-1))
    elif lex[i] == "print":

        i += 1
        try:
            if lex[i] != "(":
                print(f"Invalid use of print function: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
                exit()
        except IndexError:
            print(f"Invalid use of print function: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()
        i += 1

        strt = i
        E()
        expr = lex[strt:i]
        postfix += toPostfix(expr)

        if lex[i] != ")":
            print(f"Invalid use of print function: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()
        i += 1

        postfix.append(parstack.pop(-1))
    else:
        print(f"Invalid statement or the variable you use was not yet defined: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
        exit()

    if lex[i] != ";" and lex[i + 1] != "}":
        print(f"No semicolon in the end of the line or invalid expression: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
        exit()

    i += 1


def E():
    global i

    E1()

    if lex[i] in [">", "<", "==", "!=", ">=", "<="]:
        i += 1

        E1()


def E1():
    global i, parstack

    T()

    while lex[i] in ["+", "-", "or"]:

        if lex[i] != "or":
            i += 1

            T()
        else:
            i += 1

            E()


def T():
    global i, parstack

    F()

    while lex[i] in ["*", "/", "//", "%", "and"]:
        i += 1

        F()


def F():
    global i

    if lex[i].isalpha():
        if lex[i] not in ["true", "false", "not"]:
            IKR()
        else:
            if lex[i] != "not":
                print(lex[i])
                L()
            else:
                i += 1
                F()

                i += 1
    elif lex[i].replace(".", "").isdigit():
        N()
    else:
        if lex[i] != "(":
            print(f"Expression written not in () or is invalid: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()
        i += 1
        E()

        if lex[i] != ")":
            print(f"Expression written not in () or is invalid: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
            exit()
    i += 1


def L():
    global i

    # postfix.append(lex[i])

    if lex[i] not in ["true", "false"]:
        print(f"Wrong logical expression: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
        exit()


def N():
    global i

    # postfix.append(lex[i])

    if lex[i].count(".") > 1:
        print(f"Invalid number: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
        exit()

    if any(not x.isdigit() and x != "." for x in lex[i]):
        print(f"invalid number: String {special[:(special[:i].count(';.') + i)].count(';.') + 1} in File {progname}")
        exit()


def IKR():
    global i

    # postfix.append(lex[i])

    if not all(x.isalpha() for x in lex[i]):
        print(f"invalid variable name: String {special[:(special[:i].count(';.') + 1 + i)].count(';.') + 1} in File {progname}")
        exit()


P()
a = 0

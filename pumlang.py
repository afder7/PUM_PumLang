from lexer import variables
from parser import postfix


def Int(*args):
    for a in args:
        variables[a] = [int, None]
    return


def Bool(*args):
    for a in args:
        variables[a] = [bool, None]
    return


def Float(*args):
    for a in args:
        variables[a] = [float, None]
    return


def Assign(a, val):
    if val in variables:
        val = variables[val][1]
    if variables[a] is None or type(val) != variables[a][0]:
        print(f"wrong typing for {a}: value of another type (checking out the semicolons in your variable init strings may also work out)")
        exit()
    variables[a][1] = variables[a][0](val)
    return


def Plus(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b):
        print("you can't sum two values of different type")
        exit()
    if type(a) != bool:
        return a + b
    else:
        return a or b


def Minus(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b) or type(a) == bool:
        print("you can't subtract two values of different type")
        exit()
    return a - b


def Multiply(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b):
        print("you can't multiply two values of different type")
        exit()
    if type(a) != bool:
        return a * b
    else:
        return a and b


def Divide(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b) or type(a) == bool:
        print("you can't divide two values of different type or of a type bool")
        exit()
    return a / b


def IntDivide(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b) or type(a) != int:
        print("you can't divide as integers two values of different type or not of int type")
        exit()
    return a // b


def Modulo(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b) or type(a) != int:
        print("you can't divide with remainder two values of different type or not of int type")
        exit()
    return a % b


def More(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b) or type(a) == bool:
        print("you can't compare two values of different type or of bool type")
        exit()
    return a > b


def Less(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b) or type(a) == bool:
        print("you can't compare two values of different type or of bool type")
        exit()
    return a < b


def MoreOrEqual(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b) or type(a) == bool:
        print("you can't compare two values of different type or of bool type")
        exit()
    return a >= b


def LessOrEqual(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b) or type(a) == bool:
        print("you can't compare two values of different type or of bool type")
        exit()
    return a <= b


def Equal(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b) or type(a) == bool:
        print("you can't compare two values of different type or of bool type")
        exit()
    return a == b


def NotEqual(a, b):
    if a in variables:
        a = variables[a][1]
    if b in variables:
        b = variables[b][1]
    if type(a) != type(b) or type(a) == bool:
        print("you can't compare two values of different type or of bool type")
        exit()
    return a != b


def Or(a, b):
    if type(a) != type(b) or type(a) != bool:
        print("use bool type for logical operations")
        exit()
    return a or b


def And(a, b):
    if type(a) != type(b) or type(a) != bool:
        print("use bool type for logical operations")
        exit()
    return a and b


def Not(a):
    if type(a) != bool:
        print("use bool type for logical operations")
        exit()
    return not a


def Print(a):
    if a in variables:
        a = variables[a][1]
    print(a)
    return


def Input(a):
    try:
        variables[a][1] = variables[a][0](input())
    except ValueError:
        print("wrong input typing")
        exit()
    return


def While(expr, go, start):
    global stack
    top = expr.copy()
    while top[0]:
        c = start
        skip = 0
        for i in postfix[start + 1:]:
            if i == 'goto':
                gta = stack.pop()
                break
            if isinstance(skip, int) and c < skip:
                c += 1
                continue
            elif isinstance(skip, tuple):
                if c > skip[0] and c < skip[1]:
                    c += 1
                    continue
            if i not in functions:
                stack.append(i)
            else:
                if i in [':=', '+', '-', '*', '/', '//', '%', '>', '<', '>=', '<=', '==', '!=', 'or', 'and']:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(functions[i](b, a))
                elif i == 'not':
                    stack.append(functions[i](stack.pop()))
                elif i in ['input', 'print']:
                    functions[i](stack.pop())
                elif i in ['int', 'bool', 'float']:
                    functions[i](*stack)
                    stack = []
                elif i in ['while', 'if']:
                    if i == "while":
                        skip = functions[i](stack[:-1], stack[-1], c)
                    else:
                        skip = functions[i]()
                    stack = []
            c += 1

        top = []
        for i in postfix[gta:]:
            if i == 'while':
                break
            if i not in functions:
                top.append(i)
            else:
                if i in [':=', '+', '-', '*', '/', '//', '%', '>', '<', '>=', '<=', '==', '!=']:
                    a = top.pop()
                    b = top.pop()
                    top.append(functions[i](b, a))
    return top[1]


def If():
    else_begin = stack.pop()
    if isinstance(stack[-1], int):
        else_finish = stack.pop()
    if else_finish and isinstance(else_finish, bool):
        return 0
    if not else_finish and isinstance(else_finish, bool):
        return else_begin
    if stack.pop():
        return (else_finish, else_begin)
    else:
        return else_finish


def Else():
    pass


for k in range(len(postfix)):
    if isinstance(postfix[k], int):
        continue
    if postfix[k].isdigit():
        postfix[k] = int(postfix[k])
    elif postfix[k] == 'true':
        postfix[k] = True
    elif postfix[k] == 'false':
        postfix[k] = False
    elif postfix[k].replace('.', '').isdigit():
        postfix[k] = float(postfix[k])
functions = {'int': Int, 'bool': Bool, 'float': Float, ':=': Assign, '+': Plus, '-': Minus,
             '*': Multiply, '/': Divide, '//': IntDivide, '%': Modulo, '>': More, '<': Less, '>=': MoreOrEqual,
             '<=': LessOrEqual, '==': Equal, '!=': NotEqual, 'input': Input,
             'print': Print, 'while': While, 'if': If, 'else': Else, 'or': Or, 'and': And, 'not': Not}

stack = []
c = 0
skip = 0
for i in postfix:
    if isinstance(skip, int) and c < skip:
        c += 1
        continue
    elif isinstance(skip, tuple):
        if c > skip[0] and c < skip[1]:
            c += 1
            continue
    if i not in functions:
        stack.append(i)
    elif stack:
        if i in [':=', '+', '-', '*', '/', '//', '%', '>', '<', '>=', '<=', '==', '!=', 'or', 'and']:
            a = stack.pop()
            b = stack.pop()
            if i != ":=":
                stack.append(functions[i](b, a))
            else:
                functions[i](b, a)
        elif i == 'not':
            stack.append(functions[i](stack.pop()))
        elif i in ['input', 'print']:
            functions[i](stack.pop())
        elif i in ['int', 'bool', 'float']:
            functions[i](*stack)
            stack = []
        elif i in ['while', 'if']:
            if i == "while":
                skip = functions[i](stack[:-1], stack[-1], c)
            else:
                skip = functions[i]()
            stack = []
    c += 1

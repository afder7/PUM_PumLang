import os
from subprocess import Popen, PIPE, STDOUT


TESTS_COUNT = 30
TASKS = 6


tests = [t for t in os.listdir("test") if t.isdigit()]
correct_tasks = 0
for t in tests:
    print(f"========= TASK {t} =========")
    print(open(f"test/{t}/statement.txt").read())
    n = 0
    for i in range(1, TESTS_COUNT + 1):
        print(f"TEST {i}: ", end='')
        p = Popen(["python", "pumlang.py", f"test/{t}/main.plg"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        input_ = open(f"test/{t}/tests/{i}").read()
        output = p.communicate(input=input_.encode())[0].decode().strip()
        correct = open(f"test/{t}/tests/{i}.a").read().strip()
        if output != correct:
            print("FAILED")
            print("Input:")
            print(input_)
            print("Output:")
            print(output)
            print("Correct:")
            print(correct)
            break
        n += 1
        print("OK")
    if n == TESTS_COUNT:
        correct_tasks += 1

print("TASKS RESULTS")
if correct_tasks == TASKS:
    print("ALL RIGHT")
else:
    print(f"OK: {correct_tasks}, FAILED: {TASKS - correct_tasks}")
    exit(1)

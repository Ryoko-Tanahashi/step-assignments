#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multi(line, index):
    token = {'type': 'MULTI'}
    return token, index + 1

def read_div(line, index):
    token = {'type': 'DIV'}
    return token, index + 1

def read_start(line, index):
    token = {'type': 'START'}
    return token, index + 1

def read_end(line, index):
    token = {'type': 'END'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multi(line, index)
        elif line[index] == '/':
            (token, index) = read_div(line, index)
        elif line[index] == '(':
            (token, index) = read_start(line, index)
        elif line[index] == ')':
            (token, index) = read_end(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def evaluate_addsub(tokens):
    answer = 0

    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def evaluate_muldiv(tokens):
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    newTokens = [] # Token list after multiplying and dividing
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULTI':
                before = newTokens.pop()
                number = before['number'] * tokens[index]['number']
                newTokens.append({'type': 'NUMBER', 'number':number})
            elif tokens[index - 1]['type'] == 'DIV':
                before = newTokens.pop()
                number = before['number'] / tokens[index]['number']
                newTokens.append({'type': 'NUMBER', 'number':number})
            else: # If tokens[index - 1] is '+' or '-', directly add the token and number to the newToken list
                newTokens.extend([tokens[index - 1], tokens[index]])
        index += 1

    return evaluate_addsub(newTokens)

# If brackets in formula, calculate and add number token first
def evaluate_formula(tokens):
    newTokens = []
    index = 0
    while index < len(tokens):
        partialTokens = []
        if tokens[index]['type'] == 'START':
            startCount = 1
            index += 1
            while startCount != 0: # Find the matching END token
                if tokens[index]['type'] == 'START':
                    startCount += 1
                elif tokens[index]['type'] == 'END':
                    startCount -=1
                partialTokens.append(tokens[index])
                index += 1
            partialTokens.pop() # Remove the last END token
            newTokens.append({'type': 'NUMBER', 'number': evaluate_formula(partialTokens)})
        else:
            newTokens.append(tokens[index])
            index += 1

    return evaluate_muldiv(newTokens) # Calculate mult and div after removing all brackets


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate_formula(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1")
    test("-1")
    test("1+2")
    test("1.0+2")
    test("1.0+2.1-3")
    test("3*4")
    test("3.0*4")
    test("3.0*4.2")
    test("3/2")
    test("5.0000/2")
    test("5.0/3.0")
    test("5.0*2.0/3")
    test("3.0+4*2-1/5")
    test("5*(3+4)")
    test("(3.0+4*(2-1))/5")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate_formula(tokens)
    print("answer = %f\n" % answer)
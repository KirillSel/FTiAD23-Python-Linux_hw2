from flask import Flask, request, jsonify

app = Flask(__name__)

class Calculator:
    
    def __init__(self, row):
        
        self.row = list(row.replace(' ', ''))
        self.oper_list = ['-','+','*','^','/','(',')']
        self.oper_dict = {'-': 1, '+': 1, '*': 2, '/': 2, '^': 3, '(': None, ')': None}

    def normalization(self):
        
        row = self.row
        oper_list = self.oper_list
        norm_row = []
        save_row = []
        for i in range(len(row)):
            if row[i] in oper_list:
                try:
                    if row[i - 1] in oper_list[:-1] and row[i] == '-':
                        save_row.append(row[i])
                    else:
                        norm_row.append(''.join(save_row))
                        norm_row.append(row[i])
                        save_row = []
                except IndexError:
                    norm_row.append(''.join(save_row))
                    norm_row.append(row[i])
                    save_row = []
            else:
                save_row.append(row[i])
            if i == len(row) - 1:
                norm_row.append(''.join(save_row))
        norm_row = list(filter(lambda a: a != '', norm_row))
        if norm_row[-1] == ')':
            norm_row += ['+', '0']
        return norm_row

    def operations(self, operator, a, b):
        if operator == '-':
            return float(a) - float(b)
        elif operator == '+':
            return float(a) + float(b)
        elif operator == '/':
            return float(a) / float(b)
        elif operator == '*':
            return float(a) * float(b)
        else:
            return float(a) ** float(b)

    def calculation(self):
        norm_row = self.normalization()
        oper_dict = self.oper_dict

        stack_1 = []
        stack_2_1 = []
        stack_2_2 = []

        for i in range(len(norm_row)):
            if norm_row[i] in oper_dict.keys():
                stack_2_1.append(norm_row[i])
                stack_2_2.append(oper_dict[norm_row[i]])
            else:
                stack_1.append(norm_row[i])
            try:
                if stack_2_1[-1] == ')':
                    del stack_2_1[-1], stack_2_2[-1]
                    while stack_2_1[-1] != '(':
                        operator = stack_2_1[-1]
                        number_1 = stack_1[-1]
                        number_2 = stack_1[-2]
                        del stack_2_1[-1], stack_1[-2::], stack_2_2[-1]
                        stack_1.append(self.operations(operator, number_2, number_1))
                    del stack_2_1[-1], stack_2_2[-1]
            except IndexError:
                None
            if (i == len(norm_row) - 1) & (norm_row[-1] == ')'):
                return stack_1[0]
            try:
                while stack_2_2[-1] <= stack_2_2[-2]:
                    operator = stack_2_1[-2]
                    number_1 = stack_1[-1]
                    number_2 = stack_1[-2]
                    del stack_2_1[-2], stack_1[-2::], stack_2_2[-2]
                    stack_1.append(str(self.operations(operator, number_2, number_1)))
            except IndexError:
                None
            except TypeError:
                None
            if (i == len(norm_row) - 1) & (norm_row[-1] != ')'):
                while len(stack_2_1) > 0:
                    operator = stack_2_1[-1]
                    number_1 = stack_1[-1]
                    number_2 = stack_1[-2]
                    del stack_2_1[-1], stack_1[-2::], stack_2_2[-1]
                    stack_1.append(str(self.operations(operator, number_2, number_1)))
                return stack_1[0]

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    if 'expression' not in data:
        return jsonify({'error': 'Expression is missing'}), 400

    expression = data['expression']

    try:
        formula = Calculator(expression)
        result = formula.calculation()
        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero is not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)

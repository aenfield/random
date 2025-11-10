def fizzbuzz(n):
    rules = {3: 'Fizz', 5: 'Buzz'}

    for v in range(1, n + 1):
        output = ''
        for divisor, label in rules.items():
            if v % divisor == 0:
                output += label
        
        print(output or v)

        # if v % 3 == 0:
        #     print('Fizz', end='')
        
        # if v % 5 == 0:
        #     print('Buzz', end='')

        # if not ((v % 3 == 0) or (v % 5 == 0)):
        #     print(v, end='')

        # print()

if __name__ == '__main__':
    fizzbuzz(16)


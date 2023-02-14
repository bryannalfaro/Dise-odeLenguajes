from expr_postfix import PostfixConverter

#initialize alphabet
#expression = input("Enter an expression: ")

#for every expression in pruebas.txt print the postfix expression
with open('pruebas.txt') as f:
    for expression in f:
        print(expression)
        expression_postfix = PostfixConverter(expression)
        expression_postfix.build_Alphabet()
        expression_postfix.convertToPostfix()

#expression_postfix = PostfixConverter(expression)
#expression_postfix.build_Alphabet()
#expression_postfix.convertToPostfix()




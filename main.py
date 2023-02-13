from expr_postfix import PostfixConverter

#initialize alphabet
expression = input("Enter an expression: ")

expression_postfix = PostfixConverter(expression)
expression_postfix.build_Alphabet()
expression_postfix.convertToPostfix()




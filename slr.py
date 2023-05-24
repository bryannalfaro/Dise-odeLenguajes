from generated_scanner import ScannerSLR
from generated_parser import ParserSLR

scanner = ScannerSLR()
scanner.load_dfa()

tokens = []
for token in scanner.get_identified:
    if type(token) == str:
        print(token)
    else:
        tokens.append(token.token)

parser = ParserSLR(tokens)
parser.load_construct()
parser.simulate()

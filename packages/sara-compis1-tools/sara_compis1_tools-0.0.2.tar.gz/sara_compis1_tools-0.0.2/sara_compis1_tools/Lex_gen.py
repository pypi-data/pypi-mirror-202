
import sys
import sara_compis1_tools.readLex as tool

# if len(sys.argv) < 2:
#     print("Por favor ingrese el archivo .yal")
#     sys.exit(1)

yal_file = 'sara_compis1_tools/lexer.yal'

yal_file = sys.argv[1]
lex_var = tool.Lexer(yal_file)
    
lex_var.read()
lex_var.generate_automatas()
# mega_content = lexerr.generate_automatas()
# mega_automata = lexerr.unify(mega_content)
# lexerr.draw_mega_afd(mega_automata)
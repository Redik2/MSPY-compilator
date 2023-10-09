from compilator import Compilator
import sys

if __name__ == '__main__':
	comp = Compilator(sys.argv[0])
	print("-" * 10 + "LOGS" + "-" * 10)
	compiled = comp.compile()
	print("-" * 9 + "OUTPUT" + "-" * 9)
	print(compiled)
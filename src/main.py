from compilator import Compilator
import sys

if __name__ == '__main__':
	path = str(sys.argv[1])
	comp = Compilator(path)
	print("-" * 10 + "LOGS" + "-" * 10)
	compiled = comp.compile()
	print("-" * 9 + "OUTPUT" + "-" * 9)
	print(compiled)
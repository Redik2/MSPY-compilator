import codepart
from parser import Parser


class Compilator:
	def __init__(self, fp: str):
		self.fp = fp
		self.parts: list[codepart.CodePart] = []
		self.lines = self.prepare_lines().split("\n")
		self.cache = {"arrays": {}}

	@staticmethod
	def find_func_id(lines: list[str], name: str) -> int:
		i = 0
		for line in lines:
			if line.endswith("func") and line.split()[-1][:-4] == name:
				return i
			i += 1
		return -1

	def scriptLikeCompile(self):
		self.lines.append("stop")


	def compressing(self) -> str:
		return "\n".join(self.lines)


	def compileJumps(self):
		compiled_lines: list[str] = []
		line_n = 0
		for line in self.lines:
			if line.startswith("jump"):
				splitted = line.split()
				print(splitted)
				compiled_lines.append(f"jump {int(splitted[1]) + line_n} " + " ".join(splitted[2:]))
			else:
				compiled_lines.append(line)
			line_n += 1
		self.lines = compiled_lines

	def compile(self) -> str:
		self.pre_compile()
		self.getCache()
		self.compileLines()
		self.scriptLikeCompile()
		self.compileFuncs()
		self.compileArrays()
		self.compileJumps()

		return self.compressing()

	def prepare_lines(self) -> str:
		pre_script = list(open(self.fp, "r").read())
		script = []
		script_i = -1
		for i in range(len(pre_script)):
			if i != " ":
				script.append(pre_script[i])
				script_i += 1
			if pre_script[i] in ["{", "}"] and pre_script[i - 1] != "\n":
				script.insert(script_i, "\n")
				script_i += 1
			if i == len(pre_script) - 1:
				continue
			if pre_script[i] in ["{", "}"] and pre_script[i + 1] != "\n" and pre_script[i + 1] not in ["{", "}"]:
				script.append("\n")
				script_i += 1

		print("".join(script) + "\n-----------")
		return "".join(script)

	def pre_compile(self):
		compiled_lines = []
		line_n = 0


		while line_n < len(self.lines):
			line = self.lines[line_n].replace("\n", "")
			while line.startswith(" "):
				line = line[1:]
			compiled_lines.append(line)
			line_n += 1
		self.lines = compiled_lines
		self.parts = codepart.pre_compile(self.lines)

	def getCache(self):
		for part in self.parts:
			if isinstance(part, codepart.ArraySetName):
				name, cell = part.get_cache()
				self.cache["arrays"][name] = cell

	def compileLines(self):
		compiled_lines: list[str] = []
		for part in self.parts:
			compiled_lines += part.compile()
		self.lines = compiled_lines

	def compileFuncs(self):
		compiled_lines: list[str] = []
		for line in self.lines:
			if line.endswith("()"):
				id_ = Compilator.find_func_id(compiled_lines, line[:line.index("(")])
				compiled_lines.append(f"set @counter {id_}")
			else:
				compiled_lines.append(line)
		self.lines = compiled_lines

		compiled_lines: list[str] = []
		for line in self.lines:
			if line.endswith("func"):
				compiled_lines.append(" ".join(line.split()[:-1]))
			else:
				compiled_lines.append(line)
		self.lines = compiled_lines

	def compileArrays(self):
		compiled_lines: list[str] = []
		for line in self.lines:
			if line.endswith("ARRAYNAMINGUSE"):
				splitted = line.split()
				name = self.cache["arrays"][splitted[2]]
				compiled_lines.append(f"{splitted[0]} {splitted[1]} {name} {splitted[3]}")
			else:
				compiled_lines.append(line)
		self.lines = compiled_lines

if __name__ == '__main__':
	path = "test.mspy"
	compilator = Compilator(path)
	compiled = compilator.compile()
	print("-------------------------OUTPUT-------------------------")
	print(compiled)

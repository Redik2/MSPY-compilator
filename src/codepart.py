import enum
from parser import Parser
from constants import sensors, defaultLibs


def getMindustryMethod(lib, method):
	match lib:
		case "memory":
			match method:
				case "write":
					return "write"
				case "read":
					return "read"
				case _:
					return "invalid method"
		case "draw":
			match method:
				case "flush":
					return "draw flush"
				case "clear":
					return "draw clear"
				case "color":
					return "draw color"
				case "col":
					return "draw col"
				case "stroke":
					return "draw stroke"
				case "line":
					return "draw line"
				case "rect":
					return "draw rect"
				case "lineRect":
					return "draw lineRect"
				case "poly":
					return "draw poly"
				case "linePoly":
					return "draw linePoly"
				case "triangle":
					return "draw triangle"
				case "image":
					return "draw image"
				case _:
					return "invalid method"
		case "print":
			match method:
				case "add":
					return "print"
				case "flush":
					return "printflush"
				case _:
					return "invalid method"
		case "block":
			match method:
				case "enabled":
					return "control enabled"
				case "shoot":
					return "control shoot"
				case "shootp":
					return "control shootp"
				case "color":
					return "control color"
				case "sensor":
					return "sensor"
				case "radar":
					return "radar"
				case "getlink":
					return "getlink"
				case _:
					return "invalid method"
		case "utils":
			match method:
				case "stop":
					return "stop"
				case "end":
					return "end"
				case "wait":
					return "wait"
				case _:
					return "invalid method"
		case "unit":
			match method:
				case "move":
					return "ucontrol move"
				case "idle":
					return "ucontrol idle"
				case "stop":
					return "ucontrol stop"
				case "bind":
					return "ubind"
				case "flag":
					return "ucontrol flag"
				case "approach":
					return "ucontrol approach"
				case "pathfind":
					return "ucontrol pathfind"
				case "autoPathfind":
					return "ucontrol autoPathfind"
				case "boost":
					return "ucontrol boost"
				case "target":
					return "ucontrol target"
				case "targetp":
					return "ucontrol targetp"
				case "itemTake":
					return "ucontrol itemTake"
				case "itemDrop":
					return "ucontrol itemDrop"
				case "payTake":
					return "ucontrolpayTake "
				case "payDrop":
					return "ucontrol payDrop"
				case "payEnter":
					return "ucontrol payEnter"
				case "mine":
					return "ucontrol mine"
				case "build":
					return "ucontrol build"
				case "getBlock":
					return "ucontrol getBlock"
				case "within":
					return "ucontrol within"
				case "radar":
					return "uradar"
				case "locateBuilding":
					return "ulocate building"
				case "locateOre":
					return "ulocate ore core true"
				case "locateSpawn":
					return "ulocate spawn core true @copper"
				case "locateDamaged":
					return "ulocate damaged core true @copper"

				case _:
					return "invalid method"
		case _:
			return "invalid lib"


def available_libs() -> list[str]:
	return list(defaultLibs.keys())


def available_methods(lib: str) -> list[str]:
	return list(defaultLibs[lib].keys())


class CodePart:
	def __init__(self):
		pass

	def __str__(self):
		return str(self.compile())

	def compile(self) -> list[str]:
		return ["invalid"]


class MultiCodePart(CodePart):
	def __init__(self, lines: list[str]):
		super().__init__()
		self.include = pre_compile(lines)

	def compile(self) -> list[str]:
		compiled = []
		for include in self.include:
			compiled += include.compile()
		return compiled


def pre_compile(lines) -> list[CodePart]:
	parts = []
	print("".join(lines))
	print("\n" * 3)
	line_i = 0
	while line_i < len(lines):
		line = Parser.line_precompile(lines[line_i])
		if line.startswith("func"):
			parsed = Parser.parseFunc(lines, line_i)
			name = line[4:]
			parts.append(Func(parsed, name))
			line_i += len(parsed)
		elif line.startswith("while"):
			parsed = Parser.parseFunc(lines, line_i)
			parts.append(While(parsed, Parser.parse_args(line)[0]))
			line_i += len(parsed)
		elif line.startswith("if"):
			parsed = Parser.parseFunc(lines, line_i)
			print(parsed)
			if_ = If(parsed, Parser.parse_args(line)[0])
			line_i += len(parsed)
			add = 2
			opened = 0
			while line_i + add < len(lines) and opened == 0:
				print(lines[line_i + add])
				if "{" in lines[line_i + add]:
					opened += 1
				if "}" in lines[line_i + add]:
					opened -= 1
				if lines[line_i + add].find('else') != -1:
					line_i += add
					parsed = Parser.parseFunc(lines, line_i)
					if_.else_ = Else(parsed)
					line_i += len(parsed)
					break
				add += 1

			parts.append(if_)
			print("\n".join(parsed))
		elif line.startswith("else"):
			pass
		elif line.find("=") != -1:
			if line.split("=")[1].find("[") != -1:
				parts.append(ArrayGet(line))
			elif line.split("=")[0].find("[") != -1:
				parts.append(ArrayWrite(line))
			else:
				parts.append(Equate(line))
		elif line.endswith("()") and "." not in line:
			parts.append(CallFunc(line))
		elif line.find("[") != -1:
			parts.append(ArraySetName(line))
		else:
			parts.append(SingleLine(line))
		line_i += 1
	return parts


class Sensor(CodePart):
	def __init__(self, line: str):
		super().__init__()
		line = line.replace(" ", "")
		self.var = line.split("=")[0]
		self.obj = line.split("=")[1].split(".")[0]
		self.find = line.split("=")[1].split(".")[1]

	def compile(self) -> list[str]:
		return [f"sensor {self.var} {self.obj} @{self.find}"]


class Equate(CodePart):
	def __init__(self, line: str):
		super().__init__()
		line = line.replace(" ", "")
		self.vars = line.split("=")[0].split(",")
		self.type = "None"
		self.line = line

		def operation_test(line):
			for i in line.split("=", 1)[1]:
				if i in ["+", "-", "*", "/", "%", "=", "|", "&", "!"]:
					return True
			return False


		if line.split("=", 1)[1].find(".") != -1 and line.split("=", 1)[1].split(".")[1] in sensors and not line.split("=", 1)[1].split(".")[1].endswith(")"):
			self.type = "sensor"
			self.obj = line.split("=", 1)[1].split(".")[0]
			self.find = line.split("=", 1)[1].split(".")[1]
		elif line.split("=")[1].find(".") != -1 and line.split("=", 1)[1].split(".")[0] in list(defaultLibs.keys()):
			self.type = "method"
			self.lib = line.split("=", 1)[1].split(".")[0]
			self.method = line.split("=", 1)[1].split(".")[1][:line.split("=", 1)[1].split(".")[1].index("(")]
		elif operation_test(line):
			self.type = "operation"
			self.operation = ""
			for i in line.split("=", 1)[1]:
				if i in ["+", "-", "*", "/", "%", "=", "|", "&", "!"]:
					self.operation += i
			self.values = line.split("=", 1)[1].split(self.operation)
		else:
			self.type = "set"
			self.value = line.split("=")[1]

	def compile(self) -> list[str]:
		match self.type:
			case "sensor":
				return [f"sensor {self.vars[0]} {self.obj} @{self.find}"]
			case "method":
				args = Parser.parse_args(self.line)
				return [compileLine(getMindustryMethod(self.lib, self.method), defaultLibs[self.lib][self.method], args, self.vars)]
			case "operation":
				match self.operation:
					case "+":
						return [f"op add {self.vars[0]} {self.values[0]} {self.values[1]}"]
					case "-":
						return [f"op sub {self.vars[0]} {self.values[0]} {self.values[1]}"]
					case "*":
						return [f"op mul {self.vars[0]} {self.values[0]} {self.values[1]}"]
					case "/":
						return [f"op div {self.vars[0]} {self.values[0]} {self.values[1]}"]
					case "//":
						return [f"op idiv {self.vars[0]} {self.values[0]} {self.values[1]}"]
					case "%":
						return [f"op mod {self.vars[0]} {self.values[0]} {self.values[1]}"]
					case "**":
						return [f"op pow {self.vars[0]} {self.values[0]} {self.values[1]}"]
					case "==":
						return [f"op equal {self.vars[0]} {self.values[0]} {self.values[1]}"]
					case "!=":
						return [f"op notEqual {self.vars[0]} {self.values[0]} {self.values[1]}"]
					case "&&":
						return [f"op land {self.vars[0]} {self.values[0]} {self.values[1]}"]
					case "||":
						return [f"op or {self.vars[0]} {self.values[0]} {self.values[1]}"]
			case "set":
				return [f"set {self.vars[0]} {self.value}"]


class Func(MultiCodePart):
	def __init__(self, lines: list[str], name: str):
		super().__init__(lines)
		self.name = name

	def compile(self) -> list[str]:
		compiled = [f"jump {len(super().compile()) + 2} always"]
		compiled += super().compile()
		compiled += ["set @counter return"]
		compiled[1] += f" {self.name}func"

		return compiled


class CallFunc(CodePart):
	def __init__(self, line: str):
		super().__init__()
		self.line = line

	def compile(self) -> list[str]:
		compiled = ["op add return @counter 1", self.line]
		return compiled


class While(MultiCodePart):
	def __init__(self, lines: list[str], condition: str):
		super().__init__(lines)
		self.condition = condition

	def compile(self) -> list[str]:
		print(self.condition)
		true_condition = Parser.condition2true_condition(self.condition)
		if true_condition == "equalTrue":
			compared_vars = self.condition.replace(" ", "").split(Parser.true_condition2condition(true_condition))
			compiled = [f"jump {len(super().compile()) + 2} notEqual {compared_vars[0]} 1"]
		else:
			compared_vars = self.condition.replace(" ", "").split(Parser.true_condition2condition(true_condition))
			compiled = [f"jump {len(super().compile()) + 2} {Parser.revers_condition(true_condition)} {compared_vars[0]} {compared_vars[1]}"]
		compiled += super().compile()
		compiled += [f"jump -{len(super().compile()) + 1} always"]
		for line_i in range(len(compiled)):
			if compiled[line_i] == "break":
				compiled[line_i] = f"jump {len(super().compile()) + 2 - line_i} always"
			elif compiled[line_i] == "continue":
				compiled[line_i] = f"jump -{line_i} always"

		return compiled


class If(MultiCodePart):
	def __init__(self, lines: list[str], condition: str):
		super().__init__(lines)
		self.condition = condition
		self.else_: Else | None = None

	def compile(self) -> list[str]:
		print(self.condition)
		true_condition = Parser.condition2true_condition(self.condition)
		if true_condition == "equalTrue":
			compared_vars = self.condition.replace(" ", "").split(Parser.true_condition2condition(true_condition))
			compiled = [f"jump {len(super().compile()) + 1 + isinstance(self.else_, Else)} notEqual {compared_vars[0]} 1"]
		else:
			compared_vars = self.condition.replace(" ", "").split(Parser.true_condition2condition(true_condition))
			compiled = [f"jump {len(super().compile()) + 1 + isinstance(self.else_, Else)} {Parser.revers_condition(true_condition)} {compared_vars[0]} {compared_vars[1]}"]
		compiled += super().compile()
		if isinstance(self.else_, Else):
			compiled += self.else_.compile()

		return compiled


class Else(MultiCodePart):
	def __init__(self, lines: list[str]):
		super().__init__(lines)

	def compile(self) -> list[str]:
		compiled = [f"jump {len(super().compile()) + 1} always"]
		compiled += super().compile()

		return compiled



def compileLine(method, params: list[str], args: list[str], vars: list[str] = []) -> str:
	output = method
	mindustry_args = []
	v = 0
	a = 0
	for param in params:
		if param.find("var") != -1:
			if method.startswith("ulocate building") and v == 0:
				mindustry_args.append("@copper")
			mindustry_args.append(vars[v])
			v += 1
		else:
			mindustry_args.append(args[a])
			a += 1

	output += " " + " ".join(mindustry_args)
	return output


class ArraySetName(CodePart):
	def __init__(self, line: str):
		super().__init__()
		self.line = line

	def compile(self) -> list[str]:
		return []

	def get_cache(self) -> tuple[str, str]:
		name = self.line.split("[")[0]
		cell = self.line[self.line.index("[") + 1:self.line.index("]")]
		return name, cell


class ArrayWrite(CodePart):
	def __init__(self, line: str):
		super().__init__()
		self.line = line.replace(" ", "")

	def compile(self) -> list[str]:
		var = self.line.split("=")[1]
		name = self.line.split("=")[0][:self.line.split("=")[0].index("[")]
		index = self.line.split("=")[0][self.line.split("=")[0].index("[") + 1:self.line.split("=")[0].index("]")]
		return [f"write {var} {name} {index} ARRAYNAMINGUSE"]


class ArrayGet(CodePart):
	def __init__(self, line: str):
		super().__init__()
		self.line = line.replace(" ", "")

	def compile(self) -> list[str]:
		var = self.line.split("=")[0]
		name = self.line.split("=")[1][:self.line.split("=")[1].index("[")]
		index = self.line.split("=")[1][self.line.split("=")[1].index("[") + 1:self.line.split("=")[1].index("]")]
		return [f"read {var} {name} {index} ARRAYNAMINGUSE"]


class SingleLine(CodePart):
	def __init__(self, line: str):
		super().__init__()
		self.line = line

	def compile(self) -> list[str]:
		if self.line.replace(" ", "") in ["{", "}", ""]: return []
		if self.line.replace(" ", "") == "return": return ["set @counter return"]
		if self.line.replace(" ", "") == "break": return ["break"]
		if self.line.replace(" ", "") == "continue": return ["continue"]

		if self.line.find("(") == -1: return [self.line + " / invalid"]
		args = Parser.parse_args(self.line)

		lib = self.line[:self.line.index("(")].split(".")[0]
		if lib not in available_libs(): return [self.line + " / invalid lib"]

		method = self.line[:self.line.index("(")].split(".")[1]
		if method not in available_methods(lib): return [self.line + " / invalid method"]
		return [compileLine(getMindustryMethod(lib, method), defaultLibs[lib][method], args)]





if __name__ == '__main__':
	pass

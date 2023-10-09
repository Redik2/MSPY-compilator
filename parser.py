


class Parser:
	@staticmethod
	def parseFunc(lines: list[str], func_line: int) -> list[str]:
		line_i = func_line
		opened = 0
		lines_in = []
		while line_i < len(lines):
			line_i += 1
			line = Parser.line_precompile(lines[line_i])
			opened += line.startswith("{") - line.endswith("}")
			if opened == 0:
				return lines_in
			else:
				lines_in.append(line)
		return ["invalid"]

	@staticmethod
	def line_precompile(line: str):
		while line.startswith(" "):
			line = line[1:]
		return line.replace("\n", "")

	@staticmethod
	def parse_args(line: str):
		return line[line.index("(") + 1:line.index(")")].replace(", ", ",").split(",")

	@staticmethod
	def condition2true_condition(condition: str):
		true_condition = ""
		for i in list(condition):
			if i in ["=", "!", "<", ">"]:
				true_condition += i
		if true_condition == "":
			return 'equalTrue'
		match true_condition:
			case "==":
				return "equal"
			case "!=":
				return "notEqual"
			case "<":
				return "lessThan"
			case "<=":
				return "lessThanEq"
			case ">":
				return "greaterThan"
			case ">=":
				return "greaterThanEq"
			case _:
				return "invalid condition"

	@staticmethod
	def true_condition2condition(true_condition: str):
		match true_condition:
			case "equal":
				return "=="
			case "notEqual":
				return "!="
			case "lessThan":
				return "<"
			case "lessThanEq":
				return "<="
			case "greaterThan":
				return ">"
			case "greaterThanEq":
				return ">="
			case _:
				return "invalid condition"

	@staticmethod
	def revers_condition(true_condition: str):
		match true_condition:
			case "equal":
				return "notEqual"
			case "notEqual":
				return "equal"
			case "lessThan":
				return "greaterThanEq"
			case "lessThaneq":
				return "greaterThan"
			case "greaterThan":
				return "lessThanEq"
			case "greaterThanEq":
				return "lessThan"
			case _:
				return "invalid condition"


if __name__ == '__main__':
	pass

import random as rnd


operations = {
	"+": ("add", 0),
	"-": ("sub", 0),
	"*": ("mul", 1),
	"/": ("div", 1)
}


class Operation:
	def __init__(self, operation: str, var1: str, var2: str):
		self.operation, self.order = operation
		self.var1 = var1
		self.var2 = var2
		self.temp_name = "temp"
		for i in range(10):
			self.temp_name += str(rnd.randint(0, 9))

	def compile(self) -> list[str]:
		return [f"op {operations[self.operation]} {self.temp_name} {self.var1} {self.var2}"]


class MathCompilator:
	def __init__(self, output_var: str, operation: str):
		self.output_var = output_var
		self.operation = operation

if __name__ == '__main__':
	pass

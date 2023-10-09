from constants import sensors, defaultLibs, consts

if __name__ == '__main__':
	text = "{\n"
	for sensor in sensors:
			string = '"sensor": {"prefix": [".sensor"],"body": [".sensor"],"description": "Sensor type"},\n'
			string = string.replace("sensor", sensor)
			text += string
	text = text[:-2] + "\n}"
	print("\n\n\n----------SENSOR----------")
	print(text)
	open("C:\Py.projects\MSPY_compilator\mspy-snippets\snippets\\sensor.json", "w").write(text)

	text = "{\n"
	for const in consts:
			string = '"const": {"prefix": ["const"],"body": ["const"],"description": "Constant"},\n'
			string = string.replace("const", const)
			text += string
	text = text[:-2] + "\n}"
	print("\n\n\n----------CONSTS----------")
	print(text)
	open("C:\Py.projects\MSPY_compilator\mspy-snippets\snippets\\consts.json", "w").write(text)

	text = "{\n"
	for lib in defaultLibs.keys():
		string = '"lib": {"prefix": ["lib"],"body": ["lib$0"],"description": "Default lib."},\n'
		string = string.replace("lib", lib)
		text += string
		for method in defaultLibs[lib].keys():
			args = ""
			i = 1
			for arg in defaultLibs[lib][method]:
				args += "${" + str(i) + f":{arg}" + "}, "
				i += 1
			args = args[:-2]
			string = '"lib.method": {"prefix": ["lib.method"],"body": ["lib.method(args)$0"],"description": "Default func."},\n'
			string = string.replace("lib", lib).replace("method", method).replace("args", args)
			text += string
	text = text[:-2] + "\n}"
	print("\n\n\n----------LIBS----------")
	print(text)
	open("C:\Py.projects\MSPY_compilator\mspy-snippets\snippets\\default_libs.json", "w").write(text)

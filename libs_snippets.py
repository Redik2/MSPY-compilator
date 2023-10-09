from codepart import defaultLibs

if __name__ == '__main__':
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
	print(text)

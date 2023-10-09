

if __name__ == '__main__':
	text = "{\n"
	for sensor in sensors:
			string = '"sensor": {"prefix": [".sensor"],"body": [".sensor"],"description": "@sensor"},\n'
			string = string.replace("sensor", sensor)
			text += string
	text = text[:-2] + "\n}"
	print(text)

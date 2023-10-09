from constants import consts

if __name__ == '__main__':
	text = ""
	for const in consts:
		text += const + "|"
	print(text[:-1])

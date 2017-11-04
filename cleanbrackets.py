import csv, re, sys

writefile = open(sys.argv[2], 'w+')

with open(sys.argv[1], 'r') as f:
	reader = csv.reader(f, delimiter = '|')
	for row in reader:
		for idx, i in enumerate(row):
			i = re.sub(r'''<(?:[^>=]|='[^']*'|="[^"]*"|=[^'"][^\s>]*)*>''', '', i)
			if idx < (len(row) - 1):
				writefile.write(str(i) + '|')
			else:
				writefile.write(str(i) + '\n')

writefile.close()
f.close()



import os
import re
import argparse

parser = argparse.ArgumentParser(description='Query files on backup dvds.')
parser.add_argument('--md5')
parser.add_argument('--names', help='A file containing something like the output of "find * -type f".')
args = parser.parse_args()

dir = '.prev.md5'
ls = os.listdir(dir)
files = dict()

def addfile(file_path, loc):
	with open(file_path) as f:
		while True:
			line = f.readline()
			if not line:
				break
			m = re.match('([0-9a-f]{32}) [ \\*](.+)', line)
			if m.group(2) == 'query.py':
				continue
			if not m.group(2) in files:
				files[m.group(2)] = {'md5': m.group(1), 'locs': set()}
			file = files[m.group(2)]
			file['locs'].add(loc)

for fn in ls:
	addfile(dir+'/'+fn, fn)

addfile('.checksum.md5', 'this')

if args.names:
	with open(args.names) as f:
		while True:
			line = f.readline()
			if not line:
				break
			name = line.strip('\n')
			if not name in files:
				print('-', name)
	quit()

for i in files:
	file = files[i]
	if args.md5:
		if file['md5'] != args.md5:
			continue
	print(i, file)

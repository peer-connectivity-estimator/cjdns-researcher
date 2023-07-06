import os
import sys
import subprocess
import time

# Send a command to the Linux terminal
def terminal(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	stdout, _ = process.communicate()
	return stdout.decode('utf-8')

t1 = time.time()
result = terminal('cd peers; python3 testAvailable.py')
lines = result.splitlines()

prevPath = ''
prevPathSuccesses = 0
successfulPaths = []
for line in lines:
	if line.startswith('Pinging '):
		if prevPathSuccesses > 0:
			print(f'Found successful path with {prevPathSuccesses} successes')
			successfulPaths.append(prevPath)
		prevPath = line[8:]
		prevPathSuccesses = 0
	elif line.endswith(' is ok'):
		prevPathSuccesses += 1
	print('Line:', line)
	for i in range(len(line)):
		print(f'    Char "{line[i]}" has charcode {ord(line[i])}')
		if i > 10: break

if prevPathSuccesses > 0:
	print(f'Found successful path with {prevPathSuccesses} successes')
	successfulPaths.append(prevPath)

t2 = time.time()

print()
print('Successful paths:', successfulPaths)
print(f'That took {t2 - t1} seconds')
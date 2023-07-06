import os
import sys
import subprocess
import time
import re
import json


maxConnectionsToAdd = 10

# Send a command to the Linux terminal
def terminal(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	stdout, _ = process.communicate()
	return stdout.decode('utf-8')

def escape_ansi(line):
	ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
	return ansi_escape.sub('', line)

print('Fetching list of working CJDNS addresses (approximately 3 minutes)...')
t1 = time.time()
result = terminal('cd peers; python3 testAvailable.py')
lines = result.splitlines()

prevPath = ''
prevPathSuccesses = 0
successfulPaths = []
for line in lines:
	line = escape_ansi(line).strip()
	if line.startswith('Pinging '):
		if prevPathSuccesses > 0:
			#print(f'Found successful path with {prevPathSuccesses} successes')
			if prevPath.startswith('./') or prevPath.startswith('.\\'): prevPath = prevPath[2:]
			prevPath = os.path.join('peers', prevPath)
			successfulPaths.append(prevPath)
		prevPath = line[8:]
		prevPathSuccesses = 0
	elif line.endswith(' is ok'):
		prevPathSuccesses += 1

if prevPathSuccesses > 0:
	#print(f'Found successful path with {prevPathSuccesses} successes')
	if prevPath.startswith('./') or prevPath.startswith('.\\'): prevPath = prevPath[2:]
	prevPath = os.path.join('peers', prevPath)
	successfulPaths.append(prevPath)

pathPingTime = {}
for path in successfulPaths:
	with open(path, 'r') as file:
		obj = json.load(file)
		for ipport in obj:
			split = ipport.split(':')
			if len(split) != 2: continue
			ip = split[0]

			if 'publicKey' not in obj[ipport]: continue
			pubkey = obj[ipport]['publicKey']

			result = terminal(f'ping -c 3 -q {ip} | grep "min/avg"')
			match = re.match(f'[^=]+= [0-9\.]+\/([0-9\.]+)', result)
			if match is not None:
				print(f'Ping from {ip} took {match.group(1)} milliseconds')
				pingTime = float(match.group(1))
				pathPingTime[pubkey] = pingTime
		
pathPingTime = dict(sorted(pathPingTime.items(), key=lambda item: int(item[1]), reverse=False))

print()
print('Successful paths:', pathPingTime)
print()

configFile = open('cjdroute.conf', 'r')
configFileLines = configFile.readlines()
configFile.close()


startIndex = None
endIndex = None
for i in range(len(configFileLines)):
	if '"outgoingConnections": [' in configFileLines[i]:
		startIndex = i
	
	if startIndex is not None:
		print('Located in configuration:', configFileLines[i].strip())
		if ']' in configFileLines[i]:
			endIndex = i
			break
if startIndex is None or endIndex is None:
	print('ERROR: Could not find \'"outgoingConnections": [\' in cjdroute.conf')
	sys.exit()

print()

while startIndex <= endIndex - 2:
	print('Removed config line:', configFileLines.pop(startIndex + 1).strip())
	endIndex -= 1

print()

for i, path in enumerate(pathPingTime):
	comma = ',' if i < min(len(pathPingTime), maxConnectionsToAdd) - 1 else ''
	configFileLines.insert(startIndex + i + 1, (' ' * 16) + '"' + path + '"' + comma + '\n')

	print('Added config line:', configFileLines[startIndex + i + 1].strip())
	if i > maxConnectionsToAdd - 2: break

configFile = open('cjdroute.conf', 'w')
configFileLines = configFile.writelines(configFileLines)
configFile.close()

t2 = time.time()

print()
print('Config file cjdroute.conf was successfully edited!')
print()
print(f'That took {t2 - t1} seconds')
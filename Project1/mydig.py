import myRes
import sys
import socket
import time

f = open('mydig_output.txt','a')
qn = sys.argv[1]
tp = sys.argv[2]
result = myRes.myResolver(qn,tp,0)[0]
mystr = myRes.myResolver(qn,tp,0)[2]
num = len(result)
if num == 1:
	num = 1 + result[0].to_text().count('\n')
num = num + len(mystr)
count = myRes.myResolver(qn,tp,0)[1]
myServer = socket.gethostbyname(socket.gethostname())
myDate = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
f.write('#########Trial at ' + myDate + '##########\n\n')
f.write('>>> python mydig.py ' + sys.argv[1] + ' ' + sys.argv[2] + '\n\n')
print('QUERY: 1, ANSWER: ' + str(num) + ', AUTHORITY: 0, ADDITIONAL: 0\n')
print(';; QUESTION SECTION:')
print(';' + qn + '. IN ' + tp + '\n')
print(';; ANSWER SECTION:')
f.write('QUERY: 1, ANSWER: ' + str(num) + ', AUTHORITY: 0, ADDITIONAL: 0\n\n')
f.write(';; QUESTION SECTION:\n')
f.write(';' + qn + '. IN ' + tp + '\n\n')
f.write(';; ANSWER SECTION:\n')
if len(mystr):
	for i in range(len(mystr)):
		f.write(mystr[i] + '\n')
		print(mystr[i])
for i in range(len(result)):
	f.write(result[i].to_text() + "\n")
	print(result[i].to_text())
print('\n;; Query time: ' + str(count) + ' msec')
print(';; SERVER: ' + myServer)
print(';; WHEN: ' + myDate)
f.write('\n;; Query time: ' + str(count) + ' msec\n')
f.write(';; SERVER: ' + myServer + '\n')
f.write(';; WHEN: ' + myDate + '\n\n\n\n\n')

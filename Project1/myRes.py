import dns.query
import dns.resolver
import dns.name
import dns
import sys
import time

def findIp(text):
	ind = text.rindex(' ')
	return text[ind + 1:]

def myResolver(qn,tp = 'A',p = 1,dnsServer = 0):
	defaultR = dns.resolver.Resolver()
	str1 = []
	roots = ['198.41.0.4','192.228.79.201','192.33.4.12','199.7.91.13','192.203.230.10','192.5.5.241','192.112.36.4','198.97.190.53','192.36.148.17','192.58.128.30','193.0.14.129','199.7.83.42','202.12.27.33']
	if dnsServer == 1:
		roots = defaultR.nameservers
	if dnsServer == 2:
		roots = ['8.8.8.8','4.4.4.4']
	nameservers = roots
	start = time.time()
	req = dns.message.make_query(qn,tp)
	while True:
		for ns in nameservers:
			response = dns.query.udp(req,ns)
			if len(response.answer) or len(response.authority):
				break
	
		if len(response.answer):
			str0 = response.answer[len(response.answer)-1].to_text()
			if not 'IN ' + tp in str0:
				str1.append(str0)
				new_q = str0[str0.rindex(' ') + 1:]
				req = dns.message.make_query(new_q,tp)
				nameservers = roots
				continue
			else:
				finish = time.time()
				break

		nameservers = []
		if len(response.additional) > 0:
			for items in response.additional:
				nameservers.append(findIp(items.to_text()))
		else:
			for items in response.authority:
				my_qn = findIp(items.to_text())
				ans = defaultR.query(my_qn,'A').answer
				new_ip = findIp(ans[0].to_text())
				nameservers.append(new_ip)
	
	if len(str1):
		if p:
			for i in range(len(str1)):
				print(str1[i])
	for i in range(len(response.answer)):
		if p:
			print(response.answer[i].to_text())
	if len(response.answer) == 0:
		print('Error happened!')

	else:
		tx = response.answer[len(response.answer)-1].to_text()
		if p:
			print('The ip address:')
			while 'IN ' + tp in tx:
				if '\n' in tx:
					print(tx[tx.index('IN') + 4 + len(tp):tx.index('\n')])
					tx = tx[tx.index('\n')+1:]
				else:
					print(tx[tx.index('IN') + 4 + len(tp):])
					tx = []
	return [response.answer,int(1000 * (finish - start)),str1]
		


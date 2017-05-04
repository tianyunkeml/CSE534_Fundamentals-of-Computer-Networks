import myRes
import numpy as np
import matplotlib.pyplot as plt

myRunTime = 10
numBin = 12

sites = ['www.google.com','www.youtube.com','www.blogger.com','www.twitter.com','www.live.com','www.taobao.com','www.ask.com','www.msn.com','www.yahoo.co.jp','www.linkedin.com','www.weibo.com','www.bing.com','www.yandex.ru','www.ebay.com','www.mail.ru','www.reddit.com','www.stonybrook.edu','www.paypal.com','www.microsoft.com','www.wordpress.com','www.blogspot.com','www.imgur.com','www.onclickads.net','www.aliexpress.com','www.ok.ru']
time1,time2,time3 = [],[],[]
print('Using my DNS server:')
for site in sites:
	timeSet = []
	for i in range(myRunTime):
		print(site + '     Resolved!')
		this_time = myRes.myResolver(site,'A',0,0)[1]
		timeSet.append(this_time)
	avg = float(sum(timeSet))/len(timeSet)
	time1.append(avg)

print('Using local DNS server:')
for site in sites:
	timeSet = []
	for i in range(10):
		print(site + '     Resolved!')
		this_time = myRes.myResolver(site,'A',0,1)[1]
		timeSet.append(this_time)
	avg = float(sum(timeSet))/len(timeSet)
	time2.append(avg)

print('Using Google public DNS server:')
for site in sites:
	timeSet = []
	for i in range(10):
		print(site + '     Resolved!')
		this_time = myRes.myResolver(site,'A',0,2)[1]
		timeSet.append(this_time)
	avg = float(sum(timeSet))/len(timeSet)
	time3.append(avg)

print(time1)
print(time2)
print(time3)

counts1, bin_edges1 = np.histogram(time1, bins=numBin, normed=True)
counts2, bin_edges2 = np.histogram(time2, bins=numBin, normed=True)
counts3, bin_edges3 = np.histogram(time3, bins=numBin, normed=True)
cdf1 = np.cumsum(counts1)
cdf2 = np.cumsum(counts2)
cdf3 = np.cumsum(counts3)
plt.plot(bin_edges1[1:],cdf1,label = 'my DNS server')
plt.plot(bin_edges2[1:],cdf2,label = 'local DNS server')
plt.plot(bin_edges3[1:],cdf3,label = 'Google DNS server')
plt.title('CDF for 3 Resolvers')
plt.xlabel('Resolution Time(msec)')
plt.ylabel('Cumulative Probability')
plt.legend(loc = 'upper right')
plt.savefig('CDF_Plot.png')
plt.show()

import dpkt
import myParser
import sys
import matplotlib.pyplot as plt

def change(ini,cwnd,ssthresh,loss):
    if not loss:
        if cwnd < ssthresh:
            return [2 * cwnd,ssthresh]
        else:
            return [cwnd + 1,ssthresh]
    else:
        return [ini,cwnd / 2]

def RTO_Update(R,RTTVAR,SRTT):
    res_rttvar = (3.0 / 4) * RTTVAR + (1.0 / 4) * abs(SRTT - R)
    res_srtt = (7.0 / 8) * SRTT + (1.0 / 8) * R
    res_rto = res_srtt + max(1,4 * res_rttvar)
    return [res_rto,res_rttvar,res_srtt]

f = open('output3.txt','w')

[ts,direct,status,seq,ack,wdsz,length,buf] = myParser.goParse('HTTP_Sample_Big_Packet.pcap',0)

MSS = ord(buf[0][56]) * 256 + ord(buf[0][57])

if MSS >= 2190:
    ini_wnd = 2 * MSS
if MSS < 2190 and MSS > 1095:
    ini_wnd = 4380
if MSS <= 1095:
    ini_wnd = 4 * MSS

ssthresh = 65535
cwnd = [ini_wnd]

former = 0
for i in range(len(ts)):
    if direct[i] == 2:
        if seq[i] != former:
            loss = 0
        else:
            loss = 1
        [new_cwnd,ssthresh] = change(ini_wnd,cwnd[-1],ssthresh,loss)
        cwnd.append(new_cwnd)
    if len(cwnd) > 20:
        break

x_axis = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
plt.scatter(x_axis,cwnd)
plt.title('Congestion Window Size')
plt.xlabel('# of RTT')
plt.ylabel('CWND')
plt.savefig('CWND.png')
plt.show()
print 'CWND SIZE:\n' + str(cwnd) + '\n'
f.write('Congestion Window Sizes are:\n')
f.write(str(cwnd))

myrto = []
rtt = []
sign = 1
for i in range(len(ts)):
    if 'SYN' not in status[i]:
        if direct[i + 1] == sign:
            if sign == 1:
                begin = ts[i + 1]
                sign = 3 - sign
            else:
                end = ts[i + 1]
                sign = 3 - sign
                rtt.append(end - begin)
    if len(rtt) > 3:
        break

SRTT = rtt[0]
RTTVAR = rtt[0] / 2
RTO = SRTT + max(1,4 * RTTVAR)
myrto.append(RTO)

[RTO,RTTVAR,SRTT] = RTO_Update(rtt[1],RTTVAR,SRTT)
myrto.append(RTO)

[RTO,RTTVAR,SRTT] = RTO_Update(rtt[2],RTTVAR,SRTT)
myrto.append(RTO)

print 'First three RTOs:\n' + str(myrto)
f.write('\n\n\nFirst Three RTOs are:\n')
f.write(str(myrto))

f.close()

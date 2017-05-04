import dpkt
import sys
import myParser

def tcp_index(num,seqs):
    for i in range(len(seqs)):
        if abs(num - seqs[i]) < 10000:
            return i
    return -1

def cwnd_compute(MSS):
    if MSS >= 2190:
        return 2 * MSS
    if MSS < 2190 and MSS > 1095:
        return 4380
    if MSS <= 1095:
        return 4 * MSS

f = open('output2.txt','w')
[tsA,directA,statusA,seqA,ackA,wdszA,lenA,bufA] = myParser.goParse('HTTP_SampleA.pcap',0)
[tsB,directB,statusB,seqB,ackB,wdszB,lenB,bufB] = myParser.goParse('HTTP_SampleB.pcap',0)

tcp_connectA = []
tcp_connectB = []
tcp_ackA = []
tcp_ackB = []
throughputA = []
throughputB = []
goodputA = []
goodputB = []
avg_rttA = []
avg_rttB = []
iwsA = []
iwsB = []
signA = []
signB = []
rrtCountA = []
rrtCountB = []
beginA = []
beginB = []
for i in range(max(len(tsA),len(tsB))):
    if i < len(tsA):
        if statusA[i] == ' ACK SYN':
            tcp_connectA.append(seqA[i])
            tcp_ackA.append(ackA[i])
            throughputA.append(0)
            goodputA.append(0)
            avg_rttA.append(0)
            iwsA.append(0)
            signA.append(2)
            rrtCountA.append(0)
            beginA.append(0)

    if i < len(tsB):
        if statusB[i] == ' ACK SYN':
            tcp_connectB.append(seqB[i])
            tcp_ackB.append(ackB[i])
            throughputB.append(0)
            goodputB.append(0)
            avg_rttB.append(0)
            iwsB.append(0)
            signB.append(2)
            rrtCountB.append(0)
            beginB.append(0)

    if i < len(tsA):
        if statusA[i] == ' ACK    ' or ' ACK PSH':
            ind1 = tcp_index(seqA[i],tcp_connectA)
            ind2 = tcp_index(ackA[i],tcp_connectA)
            if ind1 != -1:
                throughputA[ind1] += lenA[i]
                if signA[ind1] == 2:
                    beginA[ind1] = tsA[i]
                    signA[ind1] = 3 - signA[ind1]
            if ind2 != -1:
                throughputA[ind2] += lenA[i]
                if signA[ind2] == 1:
                    avg_rttA[ind2] += tsA[i] - beginA[ind2]
                    rrtCountA[ind2] += 1
                    signA[ind2] = 3 - signA[ind2]
    if i < len(tsB):
        if statusB[i] == ' ACK    ' or ' ACK PSH':
            ind1 = tcp_index(seqB[i],tcp_connectB)
            ind2 = tcp_index(ackB[i],tcp_connectB)
            if ind1 != -1:
                throughputB[ind1] += lenB[i]
                if signB[ind1] == 2:
                    beginB[ind1] = tsB[i]
                    signB[ind1] = 3 - signB[ind1]

            if ind2 != -1:
                throughputB[ind2] += lenB[i]
                if signB[ind2] == 1:
                    avg_rttB[ind2] += tsB[i] - beginB[ind2]
                    rrtCountB[ind2] += 1
                    signB[ind2] = 3 - signB[ind2]

    if i < len(tsA):
        if 'FIN' in statusA[i]:
            ind1 = tcp_index(seqA[i],tcp_connectA)
            ind2 = tcp_index(ackA[i],tcp_connectA)
            if ind1 != -1:
                goodputA[ind1] = seqA[i] + ackA[i] - tcp_connectA[ind1] - tcp_ackA[ind1]
            if ind2 != -1:
                goodputA[ind2] = seqA[i] + ackA[i] - tcp_connectA[ind1] - tcp_ackA[ind1]
    
    if i < len(tsB):
        if 'FIN' in statusB[i]:
            ind1 = tcp_index(seqB[i],tcp_connectB)
            ind2 = tcp_index(ackB[i],tcp_connectB)
            if ind1 != -1:
                goodputB[ind1] = seqB[i] + ackB[i] - tcp_connectB[ind1] - tcp_ackB[ind1]
            if ind2 != -1:
                goodputB[ind2] = seqB[i] + ackB[i] - tcp_connectB[ind1] - tcp_ackB[ind1]

for i in range(max(len(tsA),len(tsB))):
    if i < len(tsA):
        if statusA[i] == ' SYN    ':
            ind = tcp_index(seqA[i],tcp_ackA)
            MSSA = ord(bufA[i][56]) * 256 + ord(bufA[i][57])
            iwsA[ind] = cwnd_compute(MSSA)
    if i < len(tsB):
        if i < len(tsB):
            if statusB[i] == ' SYN    ':
                ind = tcp_index(seqB[i],tcp_ackB)
                MSSB = ord(bufB[i][56]) * 256 + ord(bufA[i][57])
                iwsB[ind] = cwnd_compute(MSSB)

for i in range(len(avg_rttA)):
    avg_rttA[i] = avg_rttA[i] / rrtCountA[i]
for i in range(len(avg_rttB)):
    avg_rttB[i] = avg_rttB[i] / rrtCountB[i]

print 'For HTTP_SampleA.pcap:\n'
f.write('For HTTP_SampleA.pcap:\n\n')
for i in range(len(tcp_connectA)):
    print 'tcp' + str(i) + ':\nthroughput: %d'%throughputA[i] + '\ngoodput: %d'%goodputA[i] + '\navg RTT: %f'%avg_rttA[i] + '\ninitial cwnd size: %d'%iwsA[i]
    f.write('tcp' + str(i) + ':\nthroughput: %d'%throughputA[i] + '\ngoodput: %d'%goodputA[i] + '\navg RTT: %f'%avg_rttA[i] + '\ninitial cwnd size: %d'%iwsA[i] + '\n')
print '\n\n'
f.write('\n\n')

print 'For HTTP_SampleB.pcap:\n'
f.write('For HTTP_SampleB.pcap:\n\n')
for i in range(len(tcp_connectB)):
    print 'tcp' + str(i) + ':\nthroughput: %d'%throughputB[i] + '\ngoodput: %d'%goodputB[i] + '\navg RTT: %f'%avg_rttB[i] + '\ninitial cwnd size: %d'%iwsB[i]
    f.write('tcp' + str(i) + ':\nthroughput: %d'%throughputB[i] + '\ngoodput: %d'%goodputB[i] + '\navg RTT: %f'%avg_rttB[i] + '\ninitial cwnd size: %d'%iwsB[i] + '\n')

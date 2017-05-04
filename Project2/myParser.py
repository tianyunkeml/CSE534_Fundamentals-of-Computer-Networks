import dpkt
import sys

def findMark(m):
    res = ''
    if m >= 128:
        res = res + (' CWR')
        m = m - 128
    if m >= 64:
        res = res + (' ECE')
        m = m - 64
    if m >= 32:
        res =  res + (' URG')
        m = m - 32
    if m >= 16:
        res =  res + (' ACK')
        m = m - 16
    if m >= 8:
        res =  res + (' PSH')
        m = m - 8
    if m >= 4:
        res =  res + (' RST')
        m = m - 4
    if m >= 2:
        res =  res + (' SYN')
        m = m - 2
    if m >= 1:
        res =  res + (' FIN')
        m = m - 1
    if len(res) < 6:
        res = res + '    '
    return res

def goParse(filename,prt):
    f = open(filename)
    myCap = dpkt.pcap.Reader(f)
    myBuf = []
    ts_res = []
    direct_res = []
    seq_res = []
    ack_res = []
    wdsz_res = []
    status_res = []
    len_res = []
    for ts,buf in myCap:
        if len(buf) > 52:
            myBuf.append(buf)
            ts_res.append(ts)
            len_res.append(len(buf))

    if filename == 'http_first_sample.pcap':
        output = open('output1.txt','w')
        output.write('TCP Flows:\n')

    serverPort = myBuf[0][36] + myBuf[0][37]
    for buf in myBuf:
        mark = findMark(ord(buf[47]))
        status_res.append(mark)
        sport = buf[34] + buf[35]
        ack = ord(buf[45]) + 256 * ord(buf[44]) + 256 * 256 * ord(buf[43]) + 256 * 256 * 256 * ord(buf[42])
        seq = ord(buf[41]) + 256 * ord(buf[40]) + 256 * 256 * ord(buf[39]) + 256 * 256 * 256 * ord(buf[38])
        wdsz = ord(buf[49]) + 256 * ord(buf[48])
        seq_res.append(seq)
        ack_res.append(ack)
        wdsz_res.append(wdsz)
        loc = buf[:100].find('HTTP')
        if loc != -1:
            if buf[loc:loc + 12].find('\r') != -1:
                temp = buf[54:loc - 1]
                temp_loc = temp.rfind(' ')
                httpSign = 'HTTP: ' + temp[:temp_loc]
            else:
                temp = buf[loc:loc + 50]
                temp_loc = temp.find(' ')
                temp_loc2 = temp.find('\r')
                httpSign = 'HTTP: ' + temp[temp_loc + 1:temp_loc2]
        else:
            httpSign = ''

        if sport == serverPort:
            arrow = '<--------'
            direct_res.append(2)
        else:
            arrow = '-------->'
            direct_res.append(1)
        if prt:
            print 'Client   ' + arrow + '   Server  ' + mark + '   ' + '(Seq = %d'%seq + ', ack = %d'%ack + ', window size = %d'%wdsz + ')' + ' ' + httpSign
        if filename == 'http_first_sample.pcap':
            output.write('Client   ' + arrow + '   Server  ' + mark + '   ' + '(Seq = %d'%seq + ', ack = %d'%ack + ', window size = %d'%wdsz + ')' + ' ' + httpSign + '\n')
    f.close()
    if filename == 'http_first_sample.pcap':
        output.close()
    return [ts_res,direct_res,status_res,seq_res,ack_res,wdsz_res,len_res,myBuf]


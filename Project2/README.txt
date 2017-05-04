# README FILE
# Yunke Tian
# 109929662
# yunke.tian@stonybrook.edu

1.OVERVIEW
In the root directory are the following files:
Source Code Files:
myParser.py: the module file of parsing packets
partA.py: Codes for partA questions
partB.py: Codes for partB questions
partC.py: Codes for partC questions

Output Files:
output1.txt: output for partA questions
output2.txt: output for partB questions
output3.txt: output for partC questions
CWND.png: the plot of Congestion Window Size for partC

Data Files:
http_first_sample.pcap
HTTP_SampleA.pcap
HTTP_SampleB.pcap
HTTP_Sample_Big_Packet.pcap

Documentation File:
Answers.txt: answers for every part questions
README.txt: this file

2.Library Used
I used dpkt library for .pcap file parsing
Also used matplotlib for visualization

3.How to Run
Make sure python version below 3.0 (best 2.7), and with the dpkt module (this module is not compatible with python 3.0+) and matplotlib.
Then, for partA, run:"python partA.py http_first_sample.pcap"
For partB, run:"python partB.py"
For partC, run:"python partC.py"

If any problem, please contact me at yunke.tian@stonybrook.edu

Thanks!

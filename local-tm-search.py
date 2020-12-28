#find and replace words from a tab seperated list into the input file
#how to run:? python3 local-tm-search.py inputfile.txt parallel_text.txt(tab seperated)
import sys
import re
from collections import deque
from argparse import ArgumentParser

parser = ArgumentParser(description='This script will search for input text in  local tm files\n\r'+
						"How to Run?\n" +
						"python3 " + sys.argv[0] + " -i=input.txt" + " -p=parallel_tab.txt"
						)
parser.add_argument("-i", "--input", dest="inputfile",
                    help="provide input file name",required=True)
parser.add_argument("-p", "--parallel", dest="parallelfile",
                    help="provide tab seperated file",required=True)
#parser.add_argument("-l", "--lang", dest="lang",
 #                   help="provide lang=hin/tel",required=True)
#parser.add_argument("-f", "--flag", dest="con_flag",
#                   help="choose this option for consistency in lexical items -f=y",required=False)

args = parser.parse_args()

inputfile = args.inputfile
parallelfile = args.parallelfile




#open file using open file mode
fp1 = open(inputfile) # Open file on read mode -- input file
input_lines = fp1.read().split("\n") # Create a list containing all lines
fp1.close() # Close file


fp2 = open(parallelfile) # Open file on read mode -- tab seperated list file
parallel_lines = fp2.read().split("\n") # Create a list containing all lines
fp2.close() # Close file

all_hash = {}


fp3 = open('out.txt', 'w')

for parallel_line in parallel_lines:

	parallel_line = parallel_line.strip()
	parallel_line = re.sub(r' +', ' ', parallel_line)
	parallel_line = parallel_line.lower()

	if(parallel_line != ""):
		src = parallel_line.split("\t")[0]	#contians tab seperated text
		tgt = parallel_line.split("\t")[1]
		
		src = src.strip()
		tgt = tgt.strip()

		all_hash[src] = tgt

total_lines = 0
replaced_lines = 0
not_replaced_lines = 0
for input_line in input_lines:

	total_lines = total_lines + 1

	if(input_line == ""):
		print(input_line)
		continue
	src_tgt = input_line.split("\t")

	src_bkp = src_tgt[0]
	src = src_tgt[0]
	tgt = src_tgt[1]

	src = src.strip()
	src = re.sub(r' +', ' ', src)

	src = src.lower()
	if(src != ""):
		if src in all_hash:
			#print(src_bkp, all_hash[src], sep="\t")
			fp3.write(src_bkp + "\t" + all_hash[src] + "\n")
			replaced_lines = replaced_lines + 1
		else:
			#print(input_line, "Not Found", "\t")
			fp3.write(input_line + "\n")
			not_replaced_lines = not_replaced_lines + 1


print("Total lines = %d, Match Found in %d lines, No Match in %d lines" %(total_lines-1, replaced_lines, not_replaced_lines))

fp3.close()

	

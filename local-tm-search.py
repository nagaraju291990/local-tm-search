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


for input_line in input_lines:


	tmp_line = input_line.strip()
	tmp_line = re.sub(r' +', ' ', tmp_line)

	tmp_line = tmp_line.lower()
	if(tmp_line != ""):
		if tmp_line in all_hash:
			print(input_line, all_hash[tmp_line], sep="\t")
		else:
			print(input_line, "Not Found", "\t")
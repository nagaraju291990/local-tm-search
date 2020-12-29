#find and replace words from a tab seperated list into the input file and output is out.txt
#how to run:? python3 local-tm-search.py inputfile.txt(tab separated) parallel_text.txt(tab separated)
import sys
import re
from collections import deque
from argparse import ArgumentParser
import logger as log

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

log.logging.info("Parsing command line arguments")
args = parser.parse_args()

inputfile = args.inputfile
parallelfile = args.parallelfile

def validate_file(func_lines, file_name):
	func_lines.pop()
	count = 0
	validate_flag = 0
	for f in func_lines:
		count = count + 1

		tabs_count = len(re.findall('\t', f))
		if(not re.search('\t', f)):
			log.logging.info("Tab missing at line %s in %s" %(count, file_name))
			print("Tab missing at line %s in %s" %(count, file_name))
			validate_flag = 1
		if(tabs_count > 1):
			validate_flag = 1
			log.logging.info("More than one tab found at line %s in %s" %(count, file_name))
			print("More than one tab found at line %s in %s" %(count, file_name))

	if(validate_flag == 1):
		log.logging.info("%s failed validation test." %(file_name))
		print("\n%s failed validation test.\n" %(file_name))
		exit()
	else:
		log.logging.info("%s passed the validation test." %(file_name))
		print("\n%s passed the validation test \n" %(file_name))

log.logging.info("Reading input file")
#open file using open file mode
fp1 = open(inputfile) # Open file on read mode -- input file
input_lines = fp1.read().split("\n") # Create a list containing all lines
fp1.close() # Close file

log.logging.info("Validating input file")
validate_file(input_lines, inputfile)

log.logging.info("Reading parallel file")
fp2 = open(parallelfile) # Open file on read mode -- tab seperated list file
parallel_lines = fp2.read().split("\n") # Create a list containing all lines
fp2.close() # Close file

log.logging.info("Validating parallel file")
validate_file(parallel_lines, parallelfile)


all_hash = {}


fp3 = open('out.txt', 'w')
fp4 = open('matched.txt', 'w')

count = 0
log.logging.info("Saving parallel file into hash")
for parallel_line in parallel_lines:
	count = count + 1

	parallel_line = parallel_line.strip()
	parallel_line = re.sub(r' +', ' ', parallel_line)
	parallel_line = parallel_line.lower()

	log.logging.debug("After stripping, Hash saving current line=%s" %(parallel_line))
	if(parallel_line != ""):

		try:
			src = parallel_line.split("\t")[0]
		except:
			src = "Sourcemissing"
			log.logging.info("Source/Target missing in pre translated file at line=%d, content=%s" %(count, parallel_line))

		#src = parallel_line.split("\t")[0]	#contians tab seperated text

		try:
			tgt = parallel_line.split("\t")[1]
		except:
			log.logging.info("Source/Target missing in pre translated file at line=%d, content=%s" %(count, parallel_line))
			tgt = "Targetmissing"
		#tgt = parallel_line.split("\t")[1]
		
		src = src.strip()
		tgt = tgt.strip()

		all_hash[src] = tgt

log.logging.debug("Hash contents %s" %(all_hash))

total_lines = 0
replaced_lines = 0
not_replaced_lines = 0

log.logging.info("Searching for source content in saved hash")
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
			log.logging.debug("hash key=%s, hash value=%s, inputline=%s" %(src, all_hash[src], input_line))
			#print(src_bkp, all_hash[src], sep="\t")
			fp3.write(src_bkp + "\t" + all_hash[src] + "\tMatched From TM\n")
			fp4.write(src_bkp + "\t" + all_hash[src] + "\n")
			replaced_lines = replaced_lines + 1
		else:
			log.logging.debug("hash key=%s,input line=%s Match not found" %(src, input_line))
			#print(input_line, "Not Found", "\t")
			fp3.write(input_line + "\n")
			not_replaced_lines = not_replaced_lines + 1

log.logging.info("Total lines = %d, Match Found in %d lines, No Match in %d lines" %(total_lines-1, replaced_lines, not_replaced_lines))

print("Total lines = %d, Match Found in %d lines, No Match in %d lines" %(total_lines-1, replaced_lines, not_replaced_lines))

fp3.close()

	

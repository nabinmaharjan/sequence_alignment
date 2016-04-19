from fmIndex import FMINDEX
import os
#python readSearch.py <genome_folder> <read_file> buildIndex{true,false} <index_file>

def getComplementGenome(SEQ,seqType = "dna"):
	COMP_SEQ = []
	for char in SEQ:
		if char == 'A':
			if seqType == "dna":
				COMP_SEQ.append('T')
			else:
				COMP_SEQ.append('U')
		elif char == 'T' or char == 'U':
			COMP_SEQ.append('A')
		elif char == 'C':
			COMP_SEQ.append('G')
		elif char == 'G':
			COMP_SEQ.append('C')
	return COMP_SEQ

def getAlignedLocationsFromIndividualGenomes(gen_loc,read_results):
	orig_gen_loc = []
	for read_results in readResults_Array:
		for loc in read_results:
			for gen in gen_loc.keys():
				if loc > gen_loc[gen][0] and loc < gen_loc[gen][1]:
					orig_gen_loc.append((gen,loc-gen_loc[gen][0])
					#print("genome is: ", gen, "loc in concatenated genome: ", loc, "loc in original genome:", loc-gen_loc[gen][0])
	return orig_gen_loc

def readPairEndReads(read_file1,read_file2):
	pass

def searchReadPairPattern(read1,read2):
	pass

def getConcatenatedGenome(genome_folder,GEN_DEL):
	seq = ''
	gen_loc = {}
	files = []
	for f in os.listdir(genome_folder):
		genome_file = os.path.join(genome_folder,f)
		if os.path.isfile(genome_file):
			if f.endswith(".fna"):
				files.append([f,genome_file])
	
	for i in range(len(files)):
		f,genome_file = files[i]
		print("genome_file",f)
		temp_SEQ = FMINDEX.readSequence(genome_file)
		last_SEQ_len = len(seq)
		if i == len(files)-1:
			seq = seq + temp_SEQ + "$"
		else:
			seq = seq + temp_SEQ + GEN_DEL
		gen_loc[f] = (last_SEQ_len,len(seq))
	return seq,gen_loc

def verifyReadResults(readResults,SEQ,read):
	readResults_eval = []
	correct_cnt = 0
	for loc in readResults:
		if SEQ[loc:len(read)]==read:
			correct_cnt += 1
			read_eval.append((loc,1))
		else:
			read_eval.append((loc,-1))
	return correct_cnt/len(read_results),readResults_eval



def main():
	import sys
	
	genome_folder = sys.argv[1]
	
	GEN_DEL = 'NNN' # delimiter for GENOMES
	
	# get the concatenated genome and dictinary of locations for individual genomes in the concatenated genome
	SEQ,gen_loc = getConcatenatedGenome(genome_folder,GEN_DEL)


	#print("SEQ: ", SEQ)
	fmIndex = FMINDEX()


	buildFMIndex = sys.argv[3]
	#index_file = "fmIndex.pkl"
	index_file = sys.argv[4]


	if buildFMIndex.lower()=="true":
		print("building FMINDEX...")
		fmIndex.buildFMIndex(SEQ)
		fmIndex.saveFMIndex(index_file)
	else:
		print("loading FMINDEX...")
		fmIndex_data = FMINDEX.loadFMIndex(index_file)
		#print(fmIndex_data.SYMBOLS,fmIndex_data.LEN)
		fmIndex.initialize(fmIndex_data)

	#read_file
	read_file = sys.argv[2]
	reads = FMINDEX.fetchReads(read_file)
	#print(reads)
	
	#read out_file
	readOut_file = 'read_output.txt'
	readResults_Array = []
	with open(readOut_file,"w") as f:
		for read_tuple in reads:
			read_id,read = read_tuple[0],read_tuple[1]
			print("read",read)
			read_results = fmIndex.searchPattern(read)
			read_accuracy,readResults_eval = verifyReadResults(read_results,SEQ,read)
			readResults_Array.append(read_results)
			out_line = read_id
			locations = ''
			for loc,error_flag in readResults_eval:
				if locations == "":
					locations = "{0}:{1}".format(loc,error_flag)
				else:
					locations = locations + ",{0}:{1}".format(loc,error_flag)
			out_line = out_line + "," + locations + "\n"
			f.write(out_line)



if __name__ == "__main__":main()
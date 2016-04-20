from fmIndex import FMINDEX
from genomeSequenceReader import GenomeSequenceReader
from readSequenceReader import ReadSequenceReader

#python readSearch.py <buildIndex{true|false}> <index_file> <genome_folder> <pairReadSearch{true|false}> <read_file1> <read_file2>


def performPairEndSearch(pairedReads,SEQ,gen_loc,GEN_DEL,readOut_file):
	pass

def performSingleReadSearch(reads,SEQ,gen_loc,GEN_DEL,readOut_file):
	with open(readOut_file,"w") as f:
		for read_tuple in reads:
			read_id,read = read_tuple[0],read_tuple[1]
			print("read",read)
			read_results = fmIndex.searchPattern(read)
			read_accuracy,readResults_eval = verifyReadResults(read_results,SEQ,read)
			out_line = "{0},read_accuracy= {1}".format(read_id,read_accuracy)
			locations = ''
			for loc,error_flag in readResults_eval:
				gene_id, loc_in_genome = GenomeSequenceReader.getOriginalLocFromIndividualGenome(gen_loc,loc,GEN_DEL,len(SEQ))
				locations = locations + " {0}:{1}:{2}".format(gene_id,loc_in_genome,error_flag)
			out_line = out_line + locations + "\n"
			f.write(out_line)

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
	
	genome_folder = sys.argv[3]
	
	GEN_DEL = 'NNN' # delimiter for GENOMES
	
	# get the concatenated genome and dictinary of locations for individual genomes in the concatenated genome
	SEQ,gen_loc = GenomeSequenceReader.getConcatenatedGenome(genome_folder,GEN_DEL)


	#print("SEQ: ", SEQ)
	fmIndex = FMINDEX()


	buildFMIndex = sys.argv[1]
	#index_file = "fmIndex.pkl"
	index_file = sys.argv[2]


	if buildFMIndex.lower()=="true":
		print("building FMINDEX...")
		fmIndex.buildFMIndex(SEQ)
		fmIndex.saveFMIndex(index_file)
	else:
		print("loading FMINDEX...")
		fmIndex_data = FMINDEX.loadFMIndex(index_file)
		#print(fmIndex_data.SYMBOLS,fmIndex_data.LEN)
		fmIndex.initialize(fmIndex_data)

	#read out_file
	readOut_file = 'read_output.txt'

	#read_file
	pairReadSearch = sys.argv[4]
	reads = []
	if pairReadSearch.lower()=="false":
		read_file = sys.argv[5]
		reads = ReadSequenceReader.fetchReads(read_file)
		print("performing Single Read Search...")
		performSingleReadSearch(reads,SEQ,gen_loc,GEN_DEL,readOut_file)
	else:
		performPairEndSearch(pairedReads,SEQ,gen_loc,GEN_DEL,readOut_file)


if __name__ == "__main__":main()
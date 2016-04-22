from fmIndex import FMINDEX
from genomeSequenceReader import GenomeSequenceReader
from readSequenceReader import ReadSequenceReader


'''
python readSearch.py <debug{true|false}> <applyStrictPairEndMatching{true|false} <buildIndex{true|false}> <index_file> <genome_folder> <pairReadSearch{true|false}> <read_file1> <read_file2>
author: nabin maharjan
'''
def main():
	import sys
	
	isDebugMode = False
	if sys.argv[1].lower() == "true":
		isDebugMode = True 

	applyStrictPairEndMatching = False 
	if sys.argv[2].lower() == "true":
		applyStrictPairEndMatching = True 

	genome_folder = sys.argv[5]
	
	GEN_DEL = 'NNN' # delimiter for GENOMES
	
	# get the concatenated genome and dictinary of locations for individual genomes in the concatenated genome
	SEQ,gen_loc = GenomeSequenceReader.getConcatenatedGenome(genome_folder,GEN_DEL)


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
		fmIndex_data = fmIndex.loadFMIndex(index_file)

	#read out_file
	readOut_file = 'read_output'

	if isDebugMode:
		readOut_file += "_debug"
	#read_file
	pairReadSearch = sys.argv[6]
	reads = []
	if pairReadSearch.lower()=="false":
		read_file = sys.argv[7]
		reads = ReadSequenceReader.fetchReads(read_file)
		print("performing Single Read Search...")
		fmIndex.performSingleReadSearch(reads,SEQ,gen_loc,GEN_DEL,readOut_file,isDebugMode)
	else:
		if applyStrictPairEndMatching:
			readOut_file += "_strict"
		read_file = sys.argv[7]
		read_file2 = sys.argv[8]
		pairedReads = ReadSequenceReader.readPairEndReads(read_file,read_file2)
		fmIndex.performPairEndSearch(pairedReads,SEQ,gen_loc,GEN_DEL,readOut_file,isDebugMode,applyStrictPairEndMatching)


if __name__ == "__main__":main()
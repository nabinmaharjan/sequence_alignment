from fmIndex import FMINDEX
from genomeSequenceReader import GenomeSequenceReader
from readSequenceReader import ReadSequenceReader
import os

'''
python pairEndReadSearch.py <debug{true|false}> <applyStrictPairEndMatching{true|false} <buildIndex{true|false}> <index_file> <genome_folder> <paired_read_folder> <read_output_folder>  
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
	read_folder = sys.argv[6]

	temp_read_files = {}
	read_files = []
	pairedReads = []

	#read out_file
	readOut_folder = sys.argv[7]
	
	if readOut_folder.endswith("/") or readOut_folder.endswith("\\"):
		readOut_file = readOut_folder + "read_output"
	else:
		readOut_file = readOut_folder + "/read_output"


	if isDebugMode:
		readOut_file += "_debug"
	
	if applyStrictPairEndMatching:
		readOut_file += "_strict"

	#read1 file and file 2 should differ by last 4 characters only "read_1.fq vs read_2.fq"
	for f in os.listdir(read_folder):
		read_file = os.path.join(read_folder,f)
		if os.path.isfile(read_file):
			if read_file.endswith(".fq"):
				if f[:-4] not in temp_read_files:
					temp_read_files[f[:-4]] = read_file
				else: # we have a read pair
					read_file1 = temp_read_files[f[:-4]]
					#print("fetching reads from file...",read_file1, " and ",read_file)
					pairedReads.extend(ReadSequenceReader.readPairEndReads(read_file1,read_file))

	
	fmIndex.performPairEndSearch(pairedReads,SEQ,gen_loc,GEN_DEL,readOut_file,isDebugMode,applyStrictPairEndMatching)


if __name__ == "__main__":main()
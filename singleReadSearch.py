'''
perform Singe Read Search in Reference genomes
'''

from fmIndex import FMINDEX
from genomeSequenceReader import GenomeSequenceReader
from readSequenceReader import ReadSequenceReader
import os
import time

'''
python singleReadSearch.py <debug{true|false}>  <buildIndex{true|false}> <index_file> <genome_folder> <read_folder> <read_output_folder>
author: nabin maharjan
'''
def main():
	import sys
	
	isDebugMode = False
	if sys.argv[1].lower() == "true":
		isDebugMode = True 

	
	genome_folder = sys.argv[4]
	
	GEN_DEL = 'NNN' # delimiter for GENOMES
	
	# get the concatenated genome and dictinary of locations for individual genomes in the concatenated genome
	SEQ,gen_loc = GenomeSequenceReader.getConcatenatedGenome(genome_folder,GEN_DEL)


	#print("SEQ: ", SEQ)
	fmIndex = FMINDEX()


	buildFMIndex = sys.argv[2]
	#index_file = "fmIndex.pkl"
	index_file = sys.argv[3]


	if buildFMIndex.lower()=="true":
		print("building FMINDEX...")
		start = time.clock()
		fmIndex.buildFMIndex(SEQ)
		end = time.clock()
		print("time required to build fmIndex for {0} is {1} seconds".format(genome_folder,end-start))
		fmIndex.saveFMIndex(index_file)
	else:
		print("loading FMINDEX...")
		fmIndex_data = fmIndex.loadFMIndex(index_file)

	reads = []
	read_folder = sys.argv[5]

	#read out_file
	readOut_folder = sys.argv[6]
	
	if readOut_folder.endswith("/") or readOut_folder.endswith("\\"):
		readOut_file = readOut_folder + "read_output"
	else:
		readOut_file = readOut_folder + "/read_output"

	if isDebugMode:
		readOut_file += "_debug"
	
	
	for f in os.listdir(read_folder):
		read_file = os.path.join(read_folder,f)
		if os.path.isfile(read_file):
			if read_file.endswith(".fq"):
				print("fetching reads from file...",read_file)
				reads.extend(ReadSequenceReader.fetchReads(read_file))


	fmIndex.performSingleReadSearch(reads,SEQ,gen_loc,len(GEN_DEL),readOut_file,isDebugMode)

if __name__ == "__main__":main()
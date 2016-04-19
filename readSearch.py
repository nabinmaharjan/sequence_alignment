from fmIndex import FMINDEX
import os
#python readSearch.py <genome_folder> <read_file> buildIndex{true,false} <index_file>
def main():
	import sys
	
	genome_folder = sys.argv[1]
	
	SEQ = ''
	GEN_DEL = 'NNN' # delimiter for GENOMES
	gen_loc = {} # store the locations of individual genomes in a combined reference genome
	
	files = []
	for f in os.listdir(genome_folder):
		genome_file = os.path.join(genome_folder,f)
		if os.path.isfile(genome_file):
			if f.endswith(".fna"):
				files.append([f,genome_file])
	
	for i in range(len(files)):
		f,genome_file = files[i]
		temp_SEQ = FMINDEX.readSequence(genome_file)
		last_SEQ_len = len(SEQ)
		if i == len(files)-1:
			SEQ = SEQ + temp_SEQ + "$"
		else:
			SEQ = SEQ + temp_SEQ + GEN_DEL
		gen_loc[f] = (last_SEQ_len,len(SEQ))



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

	with open(readOut_file,"w") as f:
		isTesting = True
		for read_tuple in reads:
			read_id,read = read_tuple[0],read_tuple[1]
			read_results = fmIndex.searchPattern(read)
			out_line = read_id
			for loc in read_results:
				out_line = out_line + "," + loc
			f.write(out_line)
			if isTesting:
				break
					
	read_results = fmIndex.searchPattern(read)
	for loc in read_results:
		for gen in gen_loc.keys():
			if loc > gen_loc[gen][0] and loc < gen_loc[gen][1]:
				print("genome is: ", gen, "loc in concatenated genome: ", loc, "loc in original genome:", loc-gen_loc[gen][0])




if __name__ == "__main__":main()
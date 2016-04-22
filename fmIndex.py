from SuffixArrayDC3 import SuffixArray
from genomeSequenceReader import GenomeSequenceReader
import pickle

'''FM Index
author: nabin maharjan
'''
class FMINDEX:
	def __init__(self):
		self.SA = [] #Suffix Array
		self.BWT = [] #BWT array
		self.C = {} #count map gives the starting position of each symbol in BWM
		self.EP = {} #ending row position of each symbol in BWM
		self.OCC = {} #co_occurance table
		self.F = {}
		self.SYMBOLS = []
		self.EOS_POS = -1
		self.LEN = -1

	def initialize(self,fmIndex_data):
		self.SA = 	fmIndex_data.SA
		self.BWT = fmIndex_data.BWT
		self.C = fmIndex_data.C
		self.EP = fmIndex_data.EP
		self.OCC = fmIndex_data.OCC
		self.F = fmIndex_data.F 
		self.SYMBOLS = fmIndex_data.SYMBOLS
		self.EOS_POS = fmIndex_data.EOS_POS
		self.LEN = fmIndex_data.LEN


	def buildFMIndex(self,SEQ):
		self.LEN = len(SEQ)
		self.buildSuffixArray(SEQ)
		self.buildBWT(SEQ)
		self.buildCountTable()
		self.buildOccuranceTable()

	#pickle file format to save	
	def saveFMIndex(self,index_file):
		with open(index_file,"wb") as output:
			pickle.dump(self,output,pickle.HIGHEST_PROTOCOL)
		
	def loadFMIndex(self,index_file)	:
		fmIndex_data = None
		with open(index_file,"rb") as input:
			fmIndex_data = pickle.load(input)
		self.initialize(fmIndex_data)


	#BWT = characters just to the left of the suffixes in the suffix array
	def buildBWT(self,SEQ):
		for i in range(len(self.SA)):
			if SEQ[i] not in self.F:
				self.F[SEQ[i]] = 0
				self.SYMBOLS.append(SEQ[i])
			self.F[SEQ[i]] += 1
			if self.SA[i] == 0:
				self.BWT.append("$")
				self.EOS_POS = i
				#self.BWT.append(SEQ[len(SEQ)-1])
			else:
				self.BWT.append(SEQ[self.SA[i]-1])

		#sort the SYMBOLS in the sequence
		self.SYMBOLS.sort()
		#print(self.BWT)

	def buildSuffixArray(self,SEQ):
		#self.SA = SuffixArray.buildNaiveSA(SEQ)


		INT_SEQ  = SuffixArray.convertToIntegerAlphabetSequence(SEQ)
		self.SA = SuffixArray.buildLinearSA(INT_SEQ)
		

	def buildCountTable(self):
		cumulativeSum = 0
		for  i in range(len(self.SYMBOLS)):
			alphabet = self.SYMBOLS[i]
			if i == 0:
				self.C[alphabet] = 0 # this is eof symbol $
			else:
				self.C[alphabet] = cumulativeSum
			cumulativeSum += self.F[alphabet]
			self.EP[alphabet] = cumulativeSum - 1 # ending position of current alphabet in the row
		#print(self.C)
		#print(self.EP)		

	def buildOccuranceTable(self):
		for i in range(len(self.SYMBOLS)):
			symbol = self.SYMBOLS[i]
			count_symbol = 0
			for j in range(len(self.BWT)):
				if symbol == self.BWT[j]:
					count_symbol += 1
				self.OCC[symbol,j] = count_symbol
		#print(self.OCC)
 
	'''FMIndex by Ferragina and M
	  - returns the range of rows in BWM matching the given pattern
	'''
	def searchByFMIndex(self,pattern):
		# we search from the last character of the pattern string
		i = len(pattern)-1
		char = pattern[i]
		#get the starting and last row for char in BWM
		sp = self.C[char]
		ep = self.EP[char]
		#now take character at i-1 in the pattern string
		i = i - 1
		while(sp<=ep and i>=0):
			char = pattern[i]
			sp = self.C[char] + self.OCC[char,sp-1] # in 1 based index, sp = self.C[char] + self.OCC[char,sp-1] + 1
			ep = self.C[char] + self.OCC[char,ep] - 1 # in 1 based index, ep = self.C[char] + self.OCC[char,ep]
			i = i - 1
		#if pattern is not found in SEQ, sp > ep
		if(sp>sp):
			return 0,-1
		else:
			return sp,ep


	def searchPattern(self,pattern):
		sp,ep = self.searchByFMIndex(pattern)
		resArray = []
		numberOfPatternOccurrences = ep - sp + 1 # this is 0 if pattern is not found in SEQ
		#print("sp = {0}, ep = {1} ,numberOfPatternOccurrences: {2}".format(sp,ep,numberOfPatternOccurrences))
		for i in range(numberOfPatternOccurrences):
			resArray.append(self.SA[sp+i])
		return resArray

	def performSingleReadSearch(self,reads,SEQ,gen_loc,GEN_DEL,readOut_file,debug = False):
		readOut_file = readOut_file + "_singleReadSearch.txt"
		with open(readOut_file,"w") as f:
			for read_tuple in reads:
				read_id,read,read_accuracy,read_gen_list,locations = self.getReadSearchOutput(read_tuple,SEQ,gen_loc,GEN_DEL)
				if len(read_gen_list) == 0:
					continue
				f.write(self.getStringFormattedReadOutput(read_id,read,read_accuracy,read_gen_list,locations,debug))

	def applyStrictPairEndMatching(self,read1_gen_list,locations1,read2_gen_list,locations2):
		#max distance gap between read1 and read1
		max_gap =  2000
		#keep track of genomes for which we already have a read pair match
		read_pair_aligned_gen_map = {}

		read1_gen_map = {}
		for gen_id1, loc_in_genome1 in locations1:
			if gen_id1 not in read1_gen_map:
				read1_gen_map[gen_id1] = []
			read1_gen_map[gen_id1].append(loc_in_genome1)

		read1_genomes = read1_gen_map.keys()

		read2_gen_map = {}
		for gen_id2, loc_in_genome2 in locations2:
			# we simpy discard the read2 match as there is no read1 match for this genome
			if gen_id2 not in read1_genomes:
				continue
			#initialize read_pair_aligned_gen_map[gen_id2] = False if its not already in map
			#check if current genome is reverse complement genome
			gen_key = gen_id2
			if gen_id2.endswith("_rev"):
				gen_key = gen_id2[:-4]
			#otherwise, curent genome is main genome...
			if gen_key not in read_pair_aligned_gen_map:
				read_pair_aligned_gen_map[gen_key] = False
			else:
				if read_pair_aligned_gen_map[gen_key]: # we already has R1 and R2 matched with this genome..no need to look at other repeat matches
					continue 
			read1_loc_list = read1_gen_map[gen_id2]
			for  loc1 in read1_loc_list:
				if abs(loc_in_genome2-loc1)<=max_gap:
					#we have a valid read-pair match in the genome. so discontinue pair match search
					read_pair_aligned_gen_map[gen_key]=True
					break
		#now return the list of genomes for which we have pair-end match for read1 and read1
		return [genome for genome in read_pair_aligned_gen_map if read_pair_aligned_gen_map[genome]]


	def getStringFormattedReadOutput(self,read_id,read,read_accuracy,read_gen_list,locations,debug):
		out_line = read_id
		if debug:
			out_line += "|{0}|read_accuracy= {1:.2f}".format(read,read_accuracy)
		read_gen_list = "|".join(read_gen_list) 
		out_line += "|" + read_gen_list + "\n"
		if debug:
			location_str = ''
			for gene_id, loc_in_genome in locations:
				location_str = location_str + " {0}:{1}".format(gene_id,loc_in_genome)
			out_line += location_str + "\n"
		return out_line


	def performPairEndSearch(self,pairedReads,SEQ,gen_loc,GEN_DEL,readOut_file,debug = False,applyStrictMatching=False):
		readOut_file = readOut_file + "_pairedEndReadSearch.txt"
		with open(readOut_file,"w") as f:
			for read1_tuple,read2_tuple in pairedReads:
				read1_id,read1,read1_accuracy,read1_gen_list,locations1 = self.getReadSearchOutput(read1_tuple,SEQ,gen_loc,GEN_DEL)
				#if no match for read1, no need to perform search for read2
				if len(read1_gen_list) == 0:
					continue
				#perform search for read2
				read2_id,read2,read2_accuracy,read2_gen_list,locations2 = self.getReadSearchOutput(read2_tuple,SEQ,gen_loc,GEN_DEL)
				#if no match for read2, we discard the match. 
				if len(read2_gen_list) == 0:
					continue

				#We follow strict matching where matching is valid if and only if both read1 and read2 match in the same genome
				if applyStrictMatching:
					read2_gen_list = self.applyStrictPairEndMatching(read1_gen_list,locations1,read2_gen_list,locations2)
					read1_gen_list = read2_gen_list
					if len(read1_gen_list)==0:
						print("no paired read {0}-{1} pattern match found in the sequence...".format(read1_id,read2_id))
						if not debug:
							continue

				f.write(self.getStringFormattedReadOutput(read1_id,read1,read1_accuracy,read1_gen_list,locations1,debug))
				f.write(self.getStringFormattedReadOutput(read2_id,read2,read2_accuracy,read2_gen_list,locations2,debug))

	def getReadSearchOutput(self,read_tuple,SEQ,gen_loc,GEN_DEL):
		read_id,read = read_tuple[0],read_tuple[1]

		#check whether the read is invalid i.e. contains 'N' char. we don't want to do search if it is a invalid read!
		if read.find('N')>-1:
			return (read_id,read,0,[],"")

		#print("read",read)
		read_results = self.searchPattern(read)

		#check if read pattern was found or not
		if len(read_results)==0:
			return (read_id,read,0,[],"")
		read_accuracy,readResults_eval,error_readResults = self.verifyReadResults(read_results,SEQ,read)
		
		locations = []

		#list to store the list of genomes where they are found
		read_gen_list = []
		
		for loc in readResults_eval:
			gene_id, loc_in_genome = GenomeSequenceReader.getOriginalLocFromIndividualGenome(gen_loc,loc,GEN_DEL,len(SEQ))
			locations.append((gene_id,loc_in_genome))
			if gene_id.endswith("_rev"):
				gene_id = gene_id[:-4]
			if gene_id not in read_gen_list:
				read_gen_list.append(gene_id)
		return (read_id,read,read_accuracy,read_gen_list,locations)

	def verifyReadResults(self,readResults,SEQ,read):
		readResults_eval = []
		error_readResults = []
		correct_cnt = 0
		for loc in readResults:
			#print("read in genome:",SEQ[loc:len(read)]," read:",read)
			if SEQ[loc:loc+len(read)]==read:
				correct_cnt += 1
				readResults_eval.append(loc)
			else: # can we simply discard the read results which are verified as negative???
				error_readResults.append(loc)
		return correct_cnt/len(readResults),readResults_eval,error_readResults	

def main():
	import sys
	genome_file = sys.argv[1]
	fmIndex = FMINDEX()
	SEQ = FMINDEX.readSequence(genome_file)
	fmIndex.buildFMIndex(SEQ)

	pattern = 'GTGT'



if __name__ == "__main__":main()

'''
#SEQ = 'yabbadabbado$'	
SEQ = 'TACCAAATCTCCTTAGTGTAAGTTCAGACCAATTCGTACTTCGTTCAGAACTCACATTTTAACAACAGAGGACACATGCCCTACCTCCATGATCTACTGACGTCCCTGAGGCTGCAATACATGTAACGAGGCAGTATCCGCGGTAAGTCCTAGTGCAATGGCGGTTTTTTACCCTCGTCCTGGAGAAGAGGGGACGCCGGTGCAGTCATCACTAATGTGGAAATTGGGAGGACTCTTGGCCCTCCGCCTTTAGGCGGTGCTTACTCTTTCATAAAGGGGCTGTTAGTTATGGCCTGCGAGGATTCAAAAAGGTGAGCGAACTCGGCCGATCCGGAGAGACGGGCTTCAAAGCTGCCTGACGACGGTTGCGGGTCCGTATCAAAATCCTCCCAATAAGCCCCCGTGACCGTTGGTTGAACAGCCCAGGACGGGCCGACCAGAAGCCCGATTATATCGCTTAACGGCTCTTGGGCCGGGGTGCGTTACCTTGCAGGAATCGAGGCCGTCCGTTAATTCCTCTTGCATTCATATCGCGTATTTTTGTCTCTTTACCCGCTTACTTGGATAAGGATGACATAGCTTCTTACCGGAGCGCCTCCGTACACGGTACGATCGCACGCCCCGTGAGATCAATACGTATACCAGGTGTCCTGTGAGCAGCGAAAGCCTAAACGGGAAATACGCCGCCAAAAGTCGGTGTGAATACGAGTCGTAGCAAATTTGGTCTGGCTATGATCTAGATATTCCAGGCGGTACGTCTGCTCTGGTCTGCCTCTAGTGGCTCGTTAGATAGTCTAGCCGCTGGTAAACACTCCATGACCTCGGCTCTCCATTGATGCTACGGCGATTCTTGGAGAGCCAGCAGCGACTGCAAATGTGAGATCAGAGTAATATTAGCAAGCGATAAGTCCCTAACTGGTTGTGGCCTTTTGTAGAGTGAACTTCATAACATATGCTGTCTCAGGCACGTGGATGGTTTGGACAAATCAGATTCAAGTCT$'
pattern = 'GTGT'
fmIndex = FMINDEX()
fmIndex.buildSuffixArray(SEQ)
fmIndex.buildBWT(SEQ)
fmIndex.buildCountTable()
fmIndex.buildOccuranceTable()
resArray = fmIndex.searchPattern(pattern)
for i in resArray:
	print("suffix matching " + pattern + " in " + SEQ[i:])
'''


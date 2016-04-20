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

	@staticmethod		
	def loadFMIndex(index_file)	:
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

	def performSingleReadSearch(self,reads,SEQ,gen_loc,GEN_DEL,readOut_file):
		readOut_file = readOut_file + "_singleReadSearch.txt"
		with open(readOut_file,"w") as f:
			for read_tuple in reads:
				read_id,read,read_accuracy,locations = self.getReadSearchOutput(read_tuple,SEQ,gen_loc,GEN_DEL)
				if locations == "":
					continue
				out_line = "{0}|{1}|read_accuracy= {2:.2f}\n".format(read_id,read,read_accuracy)
				f.write(out_line)
				f.write(locations + "\n")

	def performPairEndSearch(self,pairedReads,SEQ,gen_loc,GEN_DEL,readOut_file):
		readOut_file = readOut_file + "_pairedEndReadSearch.txt"
		with open(readOut_file,"w") as f:
			for read1_tuple,read2_tuple in reads:
				read1_id = read1_tuple[0]
				read1 = read1_tuple[1]


	def getReadSearchOutput(self,read_tuple,SEQ,gen_loc,GEN_DEL):
		read_id,read = read_tuple[0],read_tuple[1]
		#print("read",read)
		read_results = self.searchPattern(read)

		#check if read pattern was found or not
		if len(read_results)==0:
			return (read_id,read,0,"")
		read_accuracy,readResults_eval = self.verifyReadResults(read_results,SEQ,read)
		#out_line = "{0}|read_accuracy= {1}\n".format(read_id,read_accuracy)
		#f.write(out_line)
		locations = ''
		for loc,error_flag in readResults_eval:
			gene_id, loc_in_genome = GenomeSequenceReader.getOriginalLocFromIndividualGenome(gen_loc,loc,GEN_DEL,len(SEQ))
			locations = locations + " {0}:{1}:{2}".format(gene_id,loc_in_genome,error_flag)
		locations = locations
		return (read_id,read,read_accuracy,locations)

	def verifyReadResults(self,readResults,SEQ,read):
		readResults_eval = []
		correct_cnt = 0
		for loc in readResults:
			#print("read in genome:",SEQ[loc:len(read)]," read:",read)
			if SEQ[loc:loc+len(read)]==read:
				correct_cnt += 1
				readResults_eval.append((loc,1))
			else:
				readResults_eval.append((loc,-1))
		return correct_cnt/len(readResults),readResults_eval	

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


from SuffixArrayDC3 import SuffixArray
'''FM Index'''
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
		print("sp = {0}, ep = {1} ,numberOfPatternOccurrences: {2}".format(sp,ep,numberOfPatternOccurrences))
		for i in range(numberOfPatternOccurrences):
			resArray.append(self.SA[sp+i])
		return resArray


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


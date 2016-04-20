import os
'''
genome sequence fetcher
'''
class GenomeSequenceReader:

	'''
	gen_loc: hash with genome_id as keys and their locations (start,end) in the concatenated genome as values
	read_results: list of positions for a read 
	SEQ_len: length of the concatenated genome
	'''
	
	@staticmethod
	def getLocationsFromIndividualGenomes(gen_loc,read_results,GEN_DEL,SEQ_len):
		orig_gen_loc = []
		for loc in read_results:
			gen_id,loc = GenomeSequenceReader.getOriginalLocFromIndividualGenome(gen_loc,loc,GEN_DEL,SEQ_len)
			orig_gen_loc.append((gen_id,loc))
		return orig_gen_loc

	@staticmethod
	def getOriginalLocFromIndividualGenome(gen_loc,loc,GEN_DEL,SEQ_len)	:
		gen_id="n/a"
		loc_in_genome = -1
		for gen in gen_loc.keys():
			if loc >= gen_loc[gen][0] and loc < gen_loc[gen][1]:
				gen_id = gen
				loc_in_genome = loc-gen_loc[gen][0]
				#check if it is in main genome or the reverse complement genome which are delimited by single 'N' character
				main_genome_with_its_complement_len = gen_loc[gen][1] - gen_loc[gen][0]

				#check if its last genome or not. if it is, then last character is $ without NNN
				if  gen_loc[gen][1] == SEQ_len:
					main_genome_with_its_complement_len -= 1
				else:
					main_genome_with_its_complement_len -= GEN_DEL #subtract GEN_DEL

				#now get the main_genome_len
				main_genome_len = main_genome_with_its_complement_len//2
				if loc_in_genome > main_genome_len:
					#it is present in reverse complement genome
					gen_id = gen_id + '_rev'
					loc_in_genome = loc_in_genome - (main_genome_len+1)
		return (gen_id,loc_in_genome)

	@staticmethod
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
			temp_SEQ = GenomeSequenceReader.readSequence(genome_file)
			last_SEQ_len = len(seq)
			if i == len(files)-1:
				seq = seq + temp_SEQ + "$"
			else:
				seq = seq + temp_SEQ + GEN_DEL
			gen_loc[f] = (last_SEQ_len,len(seq))
		return seq,gen_loc

	'''
	>gi|31563518|ref|NP_852610.1| microtubule-associated proteins 1A/1B light chain 3A isoform b [Homo sapiens]
	MKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPSKIPVIIERYKGEKQLPVLDKTKFLVPDHVNMSELVKIIRRRLQLNPTQAFFLLVNQHSMVSVSTPIADIYEQEKDEDGFLYMVYASQETFGFIRENE
	'''	
	@staticmethod
	def readSequence(genome_file):
		SEQ = ''
		with open(genome_file,"r") as f:
			lines = f.readlines()
			for l in lines:
				if l[0] !=">":
					SEQ = SEQ + l.strip()

		#compute the reverse complement of the genome SEQ and append it
		rev_SEQ = GenomeSequenceReader.getComplementSequence(SEQ)

		#concatenate SEQ with its reverse complement SEQ
		SEQ = SEQ + "N" + rev_SEQ
		return SEQ

	@staticmethod	
	def getComplementSequence(SEQ,seqType = "dna"):
		COMP_SEQ = ''
		for char in SEQ:
			if char == 'A':
				if seqType == "dna":
					COMP_SEQ += 'T'
				else:
					COMP_SEQ += 'U'
			elif char == 'T' or char == 'U':
				COMP_SEQ += 'A'
			elif char == 'C':
				COMP_SEQ += 'G'
			elif char == 'G':
				COMP_SEQ += 'C'
			elif char == 'N':
				COMP_SEQ += 'N'
		return COMP_SEQ

def main():
	SEQ = "ACCCGTTNTGGGCAANNNGTATCTGAGNCATAGACTC$"
	SEQ1 = "ACCCGTT"
	rev_SEQ1 = "TGGGCAA"
	SEQ2 = "GTATCTGAG"
	rev_SEQ2 = "CATAGACTC"
	print(GenomeSequenceReader.getComplementSequence(SEQ))
	gen_loc = {}
	gen_loc["gen1"] = (0,18)
	gen_loc["gen2"] = (18,38)
	GEN_DEL = 3
	SEQ_len = len(SEQ)
	read_res = [1,13,18,30,32,28,26,36]

	print(GenomeSequenceReader.getLocationsFromIndividualGenomes(gen_loc,read_res,GEN_DEL,SEQ_len))
	print(SEQ[1],SEQ[13],SEQ[18],SEQ[30],SEQ[32],SEQ[28],SEQ[26],SEQ[36])
	print(SEQ1[1],rev_SEQ1[5],SEQ2[0],rev_SEQ2[2],rev_SEQ2[4],rev_SEQ2[0],SEQ2[8],rev_SEQ2[8])
	

if __name__ == "__main__":main()
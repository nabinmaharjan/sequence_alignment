from genomeSequenceReader import GenomeSequenceReader

'''
read sequence fetcher
'''

class ReadSequenceReader:

	def readPairEndReads(read_file1,read_file2):
		read1_list = ReadSequenceReader.fetchReads(read_file1)
		read2_list = ReadSequenceReader.fetchReads(read_file2)

		if len(read1_list) != len(read2_list):
			raise Exception("The number of reads in {0} and {1} don't match!!!".format(read_file1,read_file2))
		readPairList = []

		for i in range(len(read1_list)):
			#reverse the read2 seq so that both read1 and read2 will come from the same genome
			reverse_read2_seq = GenomeSequenceReader.getComplementSequence(read2_list[i][1])
			#print(read2_list[i][1],reverse_read2_seq)
			readPairList.append((read1_list[i],(read2_list[i][0],reverse_read2_seq)))

		return readPairList


	'''
	file in fastq format expected
	@r1.1|NC_022760.1-632710
	GTGGAACACGCCGGCAAGAT
	+ 
	!!!!!!!!!!!!!!!!!!!!
	'''	
	@staticmethod	
	def fetchReads(read_file):
		print("read file", read_file)
		reads = []
		with open(read_file,"r") as f:
			lines = f.readlines()
			for i in range(1,len(lines)+1):
				if i%4==2:
					fileName = ""
					if read_file.find("/")>-1:
						fileName = read_file[read_file.rfind('/')+1:]
					elif read_file.find("\\")>-1:
						fileName = read_file[read_file.rfind("\\")+1:]
					else:
						fileName = read_file
					read_id ="{0}_{1}".format(fileName ,(i//4 + 1))
					read_seq = lines[i-1].strip()
					reads.append((read_id,read_seq))
		return reads

def main():
	read_file1 = "data\dataset_noerror\metagenome1\metagenome1_1.fq"
	read_file2 = "data/dataset_noerror/metagenome1/metagenome1_2.fq"
	readPairList = ReadSequenceReader.readPairEndReads(read_file1,read_file2)
	print(readPairList)

if __name__ == "__main__":main()
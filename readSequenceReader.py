from genomeSequenceReader import GenomeSequenceReader

'''
read sequence fetcher
author: nabin maharjan
'''

class ReadSequenceReader:

	def readPairEndReads(read_file1,read_file2):
		read1_list = ReadSequenceReader.fetchReads(read_file1)
		read2_list = ReadSequenceReader.fetchReads(read_file2)

		if len(read1_list) != len(read2_list):
			raise Exception("The number of reads in {0} and {1} don't match!!!".format(read_file1,read_file2))
		readPairList = []

		for i in range(len(read1_list)):
			#reverse complement the read2 seq so that both read1 and read2 will come from the same genome
			reverse_read2_seq = GenomeSequenceReader.getReverseComplementSequence(read2_list[i][1])
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
	def fetchReads(read_file,use_source_file_in_id = False):
		print("read file", read_file)
		reads = []

		read_source_filename = ''
		if use_source_file_in_id:
			index = read_file.rfind('/')
			if index == -1:
				index = read_file.rfind('\\')

			if index == -1:
				read_source_filename = read_file
			else:
				read_source_filename = read_file[index+1:]

		#print("read source file",read_source_filename)

		with open(read_file,"r") as f:
			lines = f.readlines()
			for i in range(1,len(lines)+1):
				if i%4==2:
					read_id = lines[i-2].strip()#.split('|')[0]
					if use_source_file_in_id:
						read_id +=  "|" + read_source_filename
					read_seq = lines[i-1].strip()
					reads.append((read_id,read_seq))
		return reads

def main():
	read_file1 = "data\dataset_noerror\metagenome1\metagenome1_1.fq"
	read_file2 = "data/dataset_noerror/metagenome1/metagenome1_2.fq"
	readPairList = ReadSequenceReader.readPairEndReads(read_file1,read_file2)
	print(readPairList)

if __name__ == "__main__":main()
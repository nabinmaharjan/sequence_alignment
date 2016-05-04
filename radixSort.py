'''
author: nabin maharjan
'''
class RadixSort:
	@staticmethod
	def radix_sort(my_list):
		random_list = []
		modulus = 10
		div = 1
		max_value = my_list[0]
		for value in my_list:
			random_list.append(value)
			if max_value < value:
				max_value = value
		#number of digits in the largest integer     
		maxlength = len(str(max_value))
		while(maxlength>0):
			buckets = [[] for i in range(10)]
			for value in random_list:
				bucket = value%modulus
				bucket = bucket//div
				buckets[bucket].append(value)   
			random_list = []    
			for i in range(10):
				if len(buckets[i]) == 0:
					continue
				for value in buckets[i]:
					random_list.append(value)
			div *= 10
			modulus *= 10
			maxlength -= 1
		#print(random_list)
		return random_list

	
	@staticmethod 
	def radixPass(R,SEQ,alphabet_size):

		sorted_list = [0 for i in range(len(R))]

		#count buckets for the alphabets
		c = [0 for i in range(alphabet_size+1)] # including padding 0 alphabet

		#count occurrences of the alphabet
		for i in range(len(R)):
			c[SEQ[R[i]]] += 1

		sum = 0
		for i in range(alphabet_size+1)	:
			temp = c[i]
			c[i] = sum
			sum += temp

		#sort
		for i in range(len(R)):
			sorted_list[c[SEQ[R[i]]]] = R[i]
			c[SEQ[R[i]]] += 1

		#delete c	
		c = []
		return sorted_list

	@staticmethod
	def radixSortTriples(R,SEQ,alphabet_size):
		#In 1st pass, sort R by the end character in the R triples
		sorted_R =RadixSort.radixPass(R,SEQ[2:],alphabet_size)

		#In 2nd pass, sort R by the end character in the R triples
		sorted_R =RadixSort.radixPass(sorted_R,SEQ[1:],alphabet_size)

		#In 3rd pass, sort R by the end character in the R triples
		sorted_R =RadixSort.radixPass(sorted_R,SEQ,alphabet_size)

		return sorted_R	

	@staticmethod
	def getRankForSortedR(originalList,sortedList,SEQ):
		#ranked the sorted list from 1 to ...
		rank_map = {}
		rank = 0
		for i in range(len(sortedList)):
			triple_index = sortedList[i]
			value = tuple(SEQ[triple_index:triple_index+3])
			if  value not in rank_map:
				rank += 1
				rank_map[value] = rank
		#print(rank_map) 
		
		distinctRank = len(sortedList) == len(rank_map)
		#now rank the original list passed to the method
		ranks = []
		for triple_index in originalList:
			value = tuple(SEQ[triple_index:triple_index+3])
			ranks.append(rank_map[value])      
		return ranks,distinctRank

	@staticmethod
	def radix_sortPairedList(pairedList):
		random_list = [value for value in pairedList]
		for tuple_pos in range(1,3):
			bucket_map = {}
			for value in random_list:
				bucket = value[-tuple_pos]
				if bucket not in bucket_map:
					bucket_map[bucket] = []
				bucket_map[bucket].append(value)
			#sort the bucket keys
			#bucket_keys = sorted(bucket_map)
			keys = [ k for k in bucket_map.keys()]
			bucket_keys = RadixSort.radix_sort(keys)
			#print("bucket keys",bucket_keys)
			a = 0
			for b in bucket_keys:
				bucket = bucket_map[b]
				for value in bucket:
					random_list[a] = value
					a += 1
			#print(random_list)
		return random_list
	
	


	@staticmethod
	def getRankForSortedList(originalList,sortedList):
		#ranked the sorted list from 1 to ...
		rank_map = {}
		rank = 0
		for i in range(len(sortedList)):
			value = sortedList[i]
			if type(value) is list:
				value = tuple(value)
			if  value not in rank_map:
				rank += 1
				rank_map[value] = rank
		#print(rank_map) 
		
		distinctRank = len(sortedList) == len(rank_map)
		#now rank the original list passed to the method
		ranks = []
		for value in originalList:
			if type(value) is list:
				value = tuple(value)
			ranks.append(rank_map[value])      
		return ranks,distinctRank



'''random_data = ['abb', 'ada', 'bba', 'do#', 'bba', 'dab', 'bad', 'o##']
sortedData = RadixSort.radix_sortByCharacter(random_data,3)
print(random_data)
print(sortedData)
rank_map, areRankDistincts = RadixSort.getRankForSortedList(random_data,sortedData)
if not areRankDistincts:
	print("call algorithm recursively")
print(rank_map,areRankDistincts)'''


'''int_list = [12,2,6,3,6,2,100,30]
sortedList = RadixSort.radix_sort(int_list)
rank_map, areRankDistincts = RadixSort.getRankForSortedList(int_list,sortedList)
print(sortedList)
print(int_list)
print(rank_map)'''



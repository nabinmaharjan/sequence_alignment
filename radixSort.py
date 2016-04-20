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
	def radix_sortByCharacter(my_list,modulus):
		random_list = [value for value in my_list]
		for i in range(1,modulus+1):
			bucket_map = {} # hash of buckets
			for value in random_list:
				offset = -i
				#last_char = value[-i]
				last_char = value[offset]
				if last_char not in bucket_map:
					bucket_map[last_char] = []
				bucket_map[last_char].append(value)

			#sort the bucket keys
			bucket_keys = sorted(bucket_map)
			#bucket_keys = RadixSort.radix_sort([ k for k in bucket_map.keys()])
			
			a = 0
			for b in bucket_keys:
				bucket = bucket_map[b]
				for value in bucket:
					random_list[a] = value
					a += 1
		#print(random_list)
		return random_list
		
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
			bucket_keys = RadixSort.radix_sort([ k for k in bucket_map.keys()])
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
	def radix_sortIntegerString(intList,num_of_tuple_pos):
		random_list = [value for value in intList]
		for tuple_pos in range(1,num_of_tuple_pos+1):
			bucket_map = {}
			for value in random_list:
				bucket = value[-tuple_pos]
				if bucket not in bucket_map:
					bucket_map[bucket] = []
				bucket_map[bucket].append(value)
			#sort the bucket keys
			#bucket_keys = sorted(bucket_map)
			bucket_keys = RadixSort.radix_sort([ k for k in bucket_map.keys()])
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


'''
#pairedList = [(5,1),(1, 0),(0, 5), (3, 7),(4, 2)]
pairedList = [[1,5,1],[1,1, 0],[0,0, 5], [6,3, 7],[4,4, 2]]
print(pairedList)
sortedList = RadixSort.radix_sortIntegerString(pairedList,3)
print(sortedList)
rank_map, areRankDistincts = RadixSort.getRankForSortedList(pairedList,sortedList)
print(rank_map)
#print(sortedList)
'''


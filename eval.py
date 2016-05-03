import sys

#input1 is correct information
input1 = sys.argv[1] 
#input2 is result from your code
input2 = sys.argv[2]

f1 = open(input1, 'r')
f2 = open(input2, 'r')

G = {}
for line in f1:
	line = line.strip()
	part = line.split(',')
	G[part[0]] = part[1]
	
TP = 0
NA = 0
n = 0
count = 0

for line in f2:
	line = line.strip()
	part = line.split(',')
	n = n + 1
	if part[1] == G[part[0]]:
		TP = TP + 1
		count = count + 1
	elif part[1] == 'NA':
		NA = NA + 1
		count = count + 1


pres = float(TP)/(n - NA)
sens = float(TP)/n


print("Abundance file: ", input1)
print("Result file: ", input2)
print("Number of read in abundance file = ", len(G))
print("\n")
#print("Count = ", count)
print("Total reads = ", n)
print("Total assignments = ", n-NA)
print("Correct assignments = ", TP)
print("Not Assigned = ", NA)
print("Presicion = ", pres)
print("Sensitivity = ", sens)

f1.close()
f2.close()
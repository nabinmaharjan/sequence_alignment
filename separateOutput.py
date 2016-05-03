'''separate output into two inputs'''

def main():
	import sys
	infile = sys.argv[1]
	outfile1 = sys.argv[2]
	outfile2 = sys.argv[3]

	outlines1 = []
	outlines2 = []
	with open(infile,"r") as f:
			lines = f.readlines()
			for i in range(len(lines)):
				if i%2==0:
					outlines1.append(lines[i])
				else:
					outlines2.append(lines[i])


	with open(outfile1,"w") as f:
		for outline in outlines1:
			f.write(outline)

	with open(outfile2,"w") as f:
		for outline in outlines2:
			f.write(outline)

if __name__ == "__main__":main()
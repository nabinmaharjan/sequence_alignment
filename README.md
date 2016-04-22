
                          Read Search in Reference Genomes

  What is it?
  -----------

  This tools uses space and time efficient FMIndex index to quickly find out the list of reference genomes per read where reads match are found.


  Installation
  ------------

  Simply git clone the code repository. Alternatively, download the zip file and extract it to desired location in the disk.


  How to run the tool?
  ------------
  pre-requisite: python 3.5.1


  python readSearch.py debug{true|false} applyStrictPairEndMatching{true|false} buildIndex{true|false} index_file genome_folder pairReadSearch{true|false} read_file1 read_file2

  1. Building FMIndex and performing pair end read search
  The FMIndex needs to be built for the sequence of reference genomes for the first time. The tool constructs 

  python readSearch.py false true true fmIndex.pkl data/referenceGenome true data/reads/read1.fq data/reads/read2.fq

  The above commands scans  all the reference genomes in fasta format (.fna extension) and builds a single sequence by
  concatenating all the reference genomes and their reverse complements and, then builds a single concatenated reference genome. 

  The FMIndex is then built for the concatenated reference genome and later saved as fmIndex.pkl in pickle format. The FMIndex process duration linearly depends upon the length of the input sequence. The suffix array is created in linear time using DC3 algorithm. 

  Once FMIndex is built, it scans the pair reads from read1 and read2 files and uses FMIndex to perform pair end read search to
  find the pair read matches for the reference genomes. The read search results is saved to an output file.

  2. Loading FMIndex and performing pair end read search

  python readSearch.py false true false fmIndex.pkl data/referenceGenome true data/reads/read1.fq data/reads/read2.fq

  3. Performing pair end read search in strict mode

  python readSearch.py false true false fmIndex.pkl data/referenceGenome true data/reads/read1.fq data/reads/read2.fq

  In strict pair end read matching mode, the match is considered true if and only if both read pairs occur in the same reference genome (or its reverse complement) and the sequence gap between them is at most 2000. It's either 'All or None' assignment of read pairs to the reference genome. In loose matching, we assign a read to a reference genome agnostic to the match condition of  the second read. This is equivalent to performing Single Read Search.

  python readSearch.py false true false fmIndex.pkl data/referenceGenome true data/reads/read1.fq data/reads/read2.fq

  Applying the strict matching helps to increase the precision of the search result while loose matching will help to improve the recall.

  4. Performing Single Read Search

  Set pairReadSearch to false

  python readSearch.py false false false fmIndex.pkl data/referenceGenome false data/reads/read1.fq

  5. Running in debug mode
  
  Set debug to true. This will print the locations and genomes where read match occur.

  python readSearch.py true false false fmIndex.pkl data/referenceGenome false data/reads/read1.fq


  Input File Formats
  ---------

  Reference Genome File Format: fasta with .fna extension

  Read File Format: fastq with .fq extenstion

   Output File Format
  ---------
  Read Search Output
  each line is read_id| reference genomes where read match occurs

  @r4.1|NC_022760.1
  @r9.1|NC_022760.1

  Read Search output(Debug mode)
  each read has two lines for its ouput.
  1st line is read_id|read sequence|total read match| reference genomes where read match occurs
  2nd line is list of genome_id:location pairs indicating read match occurrences

  @r24.1|ACAAAGGACTGAATAAAATT|1|NC_022760.1
  NC_022760.1:155545
  @r24.2|CACGGTTAAAATAAGTCAGG|2|NC_022760.1
  NC_022760.1_rev:99918 NC_022760.1_rev:113971

  Licensing
  ---------

  Code freely available under GNU GPL v3.0

  
  Contacts
  --------

     o nabin247(at)gmail(dot)com



                          Read Search in Reference Genomes

  What is it?
  -----------

  This tools uses space and time efficient FMIndex index to quickly find out the list of reference genomes per read where reads match are found. The search can be performed in two modes <br/>
  Single Read Search Mode <br />
  Pair End Read Search Mode <br />


  Installation
  ------------

  Simply git clone the code repository. Alternatively, download the zip file and extract it to desired location in the disk.


  How to run the tool?
  ------------
  pre-requisite: python 3.5.1

  1. Single Read Search Mode <br />

  *python singleReadSearch.py debug{true|false}  buildIndex{true|false} index_file genome_folder read_folder read_output_folder* <br />

  2. Pair End Read Search Mode <br />

  *python pairEndReadSearch.py debug{true|false} applyStrictPairEndMatching{true|false} buildIndex{true|false} index_file genome_folder paired_read_folder read_output_folder* <br />

  3. Building FMIndex and performing pair end read search <br />
  The FMIndex needs to be built for the sequence of reference genomes for the first time. The tool constructs 

  *python pairEndReadSearch.py false true true fmIndex.pkl data/referenceGenome data/reads data/read_output* <br />

  The above commands scans  all the reference genomes (.fna fasta format) in data/referenceGenome folder and builds a single reference genome sequence by
  concatenating all the reference genomes and their reverse complements. 

  The FMIndex is then built for the concatenated reference genome and later saved as fmIndex.pkl in pickle format. The FMIndex process duration linearly depends upon the length of the input sequence. The suffix array is created in linear time using DC3 algorithm. 

  Once FMIndex is built, it scans the pair reads from read1 and read2 files in data/reads folder(Note that, read1 file and file 2 should differ by last 4 characters only "read_1.fq vs read_2.fq") and uses FMIndex to perform pair end read search to
  find the pair read matches for the reference genomes. The read search results is saved to read_output_folder folder.

  4. Loading FMIndex and performing pair end read search <br />

  *python pairEndReadSearch.py false true false fmIndex.pkl data/referenceGenome data/reads data/read_output* <br />

  5. Performing pair end read search in strict mode <br />

  *python pairEndReadSearch.py false true false fmIndex.pkl data/referenceGenome data/reads data/read_output* <br />

  In strict pair end read matching mode, the match is considered true if and only if both read pairs occur in the same reference genome (or its reverse complement) and the sequence gap between them is at most 2000. It's either 'All or None' assignment of read pairs to the reference genome. 
  
  6. Performing pair end read search in lenient mode
  In lenient matching, we assign a read to a reference genome agnostic to the match condition of  the second read. This is equivalent to performing Single Read Search. <br />

  *python pairEndReadSearch.py false false false fmIndex.pkl data/referenceGenome data/reads data/read_output* <br />

  **Note:** Applying strict matching helps to increase the precision of the search result while lenient matching  helps to improve the recall. <br />

  7. Performing Single Read Search<br />

   *python singleReadSearch.py false  false fmIndex.pkl data/referenceGenome data/reads data/read_output* <br />

  8. Running in debug mode<br />
  
  Set debug to true. This will print the locations and genomes where read match occur.<br />

   *python singleReadSearch.py true false fmIndex.pkl data/referenceGenome data/reads data/read_output* <br />


  Input File Formats
  ---------

  Reference Genome File Format: fasta with .fna extension<br />

  Read File Format: fastq with .fq extenstion<br />

   Output File Format
  ---------
  **Read Search Output** <br />
  each line is read_id|read_source_filename|reference genomes where read match occurs<br />

  @r4.1|small_data2_1.fq|NC_022760.1<br />
  @r9.1|small_data2_1.fq|NC_022760.1<br />
  @r11.1|small_data2_1.fq|NA<br />

  If read is not matched in any genome, it is assigned NA. For example read **@r11.1** in the above example output. <br/>

  **Read Search output(Debug mode)** <br />
  each read has two lines for its ouput.<br />
  1st line is read_id|read_source_filename|read sequence|total read match|reference genomes where read match occurs<br />
  2nd line is list of genome_id:location pairs indicating read match occurrences<br />

  @r24.1|small_data2_1.fq|ACAAAGGACTGAATAAAATT|1|NC_022760.1<br />
  NC_022760.1:155545<br />
  @r24.2|small_data2_1.fq|CACGGTTAAAATAAGTCAGG|2|NC_022760.1<br />
  NC_022760.1_rev:99918 NC_022760.1_rev:113971<br />
  @r91.2|GGTGCGGTGTGACTGATGAA|0|NA<br />
  <br />
   
  In debug mode, if there is no match for the read, it is assigned NA and empty line is generated for location information. For exampe, read **@r91.2** in the debug output.<br/>

  Licensing
  ---------

  Code freely available under GNU GPL v3.0

  
  Contacts
  --------

     o nabin247(at)gmail(dot)com


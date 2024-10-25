# biodatatools

biodatatools is a package that provides a collection of useful commands `biodatatools command ...`, and utility functions *biodatatools.utils* for bioinformatics analysis. 

All commands are version controlled based on `simplevc` for backward compatibility. All results are reproducible by specifying the exact command version (with a few exceptions due to the change of dependent packages and call to external tools in some commands). Certain biodatatools commands require external tools. These are not installed along with biodatatools by default. If users run a command without the required tools, biodatatools would raise an error about the missing tools. 

This manual is separated into three major parts:

- Specific analysis sections with sets of related commands
- File types and formats used in biodatatools
- Details of all available biodatatools commands



## Specific Analysis

Here we introduce sections of specific analysis that helps organize commands used in certain scenarios. This enables a better background and explanation of the connected commands. We also provide a series of standard analysis pipeline in rmsp-library, which allows readers to download and run an analysis pipeline directly. See https://github.com/aldenleung/rmsp-library/ for more details. 

### Fastq processing with complex read layout

For certain sequencing library, the sequences are built in specific layout which one may want to extract specific parts of the sequences for further analysis. biodatatools provide two commands, `process_sequencing_reads_to_delimited_sequences`, `process_delimited_sequences` and `generate_IDMap_from_delimited`. Since library layout could be complicated, the biodatatools command `plot_sequence_library_layouts` provides a way for you to quickly visualize your library layouts. This plot also serves as a QC method by looking at the representation of anchor sequences in the library. 

#### Extraction of fastq to delimited sequences 

*biodatatools command: `process_sequencing_reads_to_delimited_sequences`*  

Here we provide a simple layout scheme to describe the sequence library layout for easy extraction of information.  

##### Read layout

A "read layout" is described by a list of objects. 

- Anchor - some known and fixed sequence: e.g. "ACGTGGC"
- Barcodes/UMIs - Unknown sequence of interest, (sometimes represented as NNN...NNs in some plasmid description). An integer or a list of integer is accepted to indicate the expected length of the unknown sequence.

<u>Example 1</u>

Our reads have anchor sequence CTGCG (black). To capture information from the reads, we could define the layout below:

Reads:

<pre>
<span style="color:red">ATCGG</span><b>CTGCG</b><span style="color:green">TTTCTGGCCACCCC</span>
<span style="color:red">TGCAG</span><b>CTGCG</b><span style="color:green">CCCCGTTAAGGTGCA</span>
<span style="color:red">GAGAA</span><b>CTGCG</b><span style="color:green">TTTCTGGCCACC</span>
</pre>
Input layout:


```
[5, "CTGCG", -1]
 ^            ^
 Cap1, 5bp    |
              Cap2, -1 means capture till the end
```

Input column names:

```
E-UMI Element
```

Captured output:

```
E-UMI	Element
ATCGG	TTTCTGGCCACCCC
TGCAG	CCCCGTTAAGGTGC
GAGAA	TTTCTGGCCACC
```



<u>Example 2</u>

Our second example contain two fixed sequences, with certain unknown sequences in variable lengths. 

Reads:

<pre>
<span style="color:red">ATCGG</span><b>CTGCG</b><span style="color:blue">TGTACC</span><b>TGTTA</b><span style="color:green">TTTCTGGCCACCCC</span>
<span style="color:red">TGCAG</span><b>CTGCG</b><span style="color:blue">GGACCTT</span><b>TGTTA</b><span style="color:green">CCCCGTTAAGGTGCA</span>
<span style="color:red">GAGAA</span><b>CTGCG</b><span style="color:blue">CAGTA</span><b>TGTTA</b><span style="color:green">TTTCTGGCCACC</span>
</pre>

Input layout:


```
[5, "CTGCG", [5,6,7], "TGTTA", -1]
 ^            ^                 ^
 Cap1, 5bp    |                 |
              Cap2 5/6/7bp      |
                                Cap3, capture till the end
```

Input column names:

```
E-UMI Barcode Element
```

Captured output:

```
E-UMI	Barcode	Element
ATCGG	TGTACC	TTTCTGGCCACCCC
TGCAG	GGACCTT	CCCCGTTAAGGTGCA
GAGAA	CAGTA	TTTCTGGCCACC
```



<u>Example 3</u>

Sometimes, the last sub-sequence could be just another anchoring sequence that is not of much interest in the downstream analysis. We could still put the full expected anchor sequences in the layout. As the last object, this anchor sequence allows partial match. Note that read that does not match the anchor sequence will not be extracted

Reads:

<pre>
<span style="color:red">ATCGG</span><b>CTGCG</b><span style="color:blue">TGTACC</span><b>CCACCTGGGGGGTCACAGT</b>
<span style="color:red">TGCAG</span><b>CTGCG</b><span style="color:blue">GGACCTT</span><b>CCACCTGGGGG</b>
<span style="color:red">TGCAG</span><b>CTGCG</b><span style="color:blue">GGTCT</span><b>TGTGCAAGGCA</b>
<span style="color:red">GAGAA</span><b>CTGCG</b><span style="color:blue">CAGTA</span><b>CCACCTGGGGGGTCACAGTTGCC</b>
</pre>

Input layout:


```
[5, "CTGCG", [5,6,7], "CCACCTGGGGGGTCACAGTTGCCTTGCCCACCCGCATGGCC"]
 ^            ^                 
 Cap1, 5bp    |                 
              Cap2 5/6/7bp      
```

Input column names:

```
E-UMI Barcode
```

Captured output: (Note that the third read is not captured)

```
E-UMI	Barcode
ATCGG	TGTACC
TGCAG	GGACCTT
GAGAA	CAGTA
```



<u>Example 4</u>

Here we demonstrate an example of paired-end sequencing reads. Captured outputs are ordered by reads 1 first, then reads 2.

Reads 1:
<pre>
<span style="color:red">ATCGG</span><b>CTGCG</b><span style="color:blue">TGTACC</span><b>TGTTA</b><span style="color:green">TTTCTGGCCACCCC</span>
<span style="color:red">TGCAG</span><b>CTGCG</b><span style="color:blue">GGACCTT</span><b>TGTTA</b><span style="color:green">CCCCGTTAAGGTGCA</span>
<span style="color:red">GAGAA</span><b>CTGCG</b><span style="color:blue">CAGTA</span><b>TGTTA</b><span style="color:green">TTTCTGGCCACC</span>
</pre>
Reads 2:
<pre>
<span style="color:red">TAACC</span><b>TGACCCC</b><span style="color:blue">CCACT</span><b>TAAACCCCGGGT</b>
<span style="color:red">ACTAC</span><b>TGACCCC</b><span style="color:blue">TACGA</span><b>TAAACCCCGGGTGCATT</b>
<span style="color:red">ACGAG</span><b>TGACCCC</b><span style="color:blue">AAACC</span><b>TAAACCCCGGGTGCA</b>
</pre>

Input layouts:

```
Layout 1
[5, "CTGCG", [5,6,7], "TGTTA", -1]

Layout 2
[5, "TGACCCC", 5, "TAAACCCCGGGTGCATTACCACAGATTACACATGA"]
```

Input column names:

```
E-UMI1 Barcode1 Element E-UMI2 Barcode2
```

Captured output:

```
E-UMI1	Barcode1	Element E-UMI2	Barcode2
ATCGG	TGTACC	TTTCTGGCCACCCC	TAACC	CCACT
TGCAG	GGACCTT	CCCCGTTAAGGTGCA	ACTAC	TACGA
GAGAA	CAGTA	TTTCTGGCCACC	ACGAG	AAACC
```



#### Processing delimited sequences

*biodatatools command: `process_delimited_sequences`*  

Extracted delimited sequences are processed for more useful information. The command supports multiple processing functions which are detailed below.

##### Input

The basic input is a delimited sequence file that contains the extracted sequence information. 

Additional reference files are needed for certain functions. For `match` and `align`, reference sequences file (in `fasta` format) is required. For `map`, a reference map file (in tab-delimited format) is required. 

##### Output

A processed delimited sequence file is output as `{prefix}.tsv.gz`. 

For each clustering performed, two additional files are generated `{prefix}_cluster-{column_name}.fa.gz` and `{prefix}_cluster-{column_name}.tsv.gz`  that contains the clustering information. See the function `cluster` for more details. 

##### Functions

| Function | Description                                                  |
| -------- | ------------------------------------------------------------ |
| filter   | Remove certain rows (entries) that do not match the criteria. For example, if we want to remove any row with `"N"` in the Barcode1 and Barcode2 column, then the following could be added: ```-filter Barcode1 Barcode2 -filter_func 'lambda x: "N" not in x'``` |
| trim     | Trim target sequence by removing any identified query sequence and beyond. Example: `-trim 'column=Element;trimseq=ACGGT;direction=1'` |
| match    | Align sequence to the reference and retrieve the identity of it. Unlike the `align` function, it only reports the identity rather than the exact alignment position. If the sequence could be matched to multiple references with the same score, `__AMBIG__` is reported. If the sequence does not match to any reference, `__UNMATCH__` is reported. If `group` is applied, the intersection of matched references from all match columns is taken. Example: `-match 'column=Element;direction=1;strand=1'` |
| align    | Align sequence to the reference and retrieve the alignment position. Unlike the `match` function, it reports both the identity and the exact alignment position. If the sequence could be matched to multiple references, or multiple alignment positions in the same reference with the same score, `__AMBIG__` is reported. If the sequence does not match to any reference, `__UNMATCH__` is reported. Example: `-align 'column=Element'` |
| map      | Map the column values according to the reference map. `__UNMATCH__` is returned if the reference map does not contain the key. `-map 'column=EID;key=EID;value=Element'` |
| cluster  | Cluster the sequences. Two additional output files are generated - (1) `{prefix}_cluster-{column_name}.fa.gz` presents the representative sequence for each cluster in fasta format; (2) `{prefix}_cluster-{column_name}.tsv.gz` presents all sequences used in the clustering and the clusters they are assigned to. Example: `-cluster 'column=EID'` |
| quantify | Use the values from all non-quantify columns as unique keys to group sequences from the quantify columns. Cluster the sequences within each group and report the number of distinct clusters. |
| merge    | Merge values from the merge column grouped by non-merge columns as unique keys. |

##### Other options

- **-order**:  Indicate the output order of output columns. Any column not indicated in the order will not be output (this also affect the unique keys in `quantify` and `merge`)
- **-nthread**: Number of threads used in certain functions

##### Notes on clustering in multiple library layouts

If you have multiple files from the same library layout, usually simply joining the table using `concat_delimited`  should enable you to do clustering within the concatenated file. However, in certain scenario, one may need to perform clustering on multiple files. For example, if you sequence the same ID loci using two different library layouts, you need to separate the processing steps. Here, the command `cluster_delimited_sequences` allows you to cluster columns from multiple files at the same time. After clustering, one could use the match function in `process_delimited_sequences` to applying the clustering results to individual delimited sequences files. 

##### Future functions to be added

Under the current strategy, functions are run in a specific order. A general option `priority` may be added in the future to determine the run order.

#### Generation of ID map from processed delimited sequences

*biodatatools command: `generate_IDMap_from_delimited`*  

At times we would like to create an ID map that one could look up a certain ID in a table to get the target value. This method generates an ID map where target value obtained from an ID must be unique (with a user-defined error tolerance).

In the following example, we would like to have the EID and PID to be unique and map to the Element. Here we will have id_column `EID` and `PID`, target_column `Element`, and count_column `Count`. 

| EID   | PID   | Element | Count |
| ----- | ----- | ------- | ----- |
| EID-1 | PID-1 | A1      | 1000  |
| EID-2 | PID-2 | A2      | 78    |
| EID-2 | PID-3 | A2      | 9     |
| EID-3 | PID-4 | A1      | 987   |
| EID-4 | PID-5 | A3      | 70    |
| EID-5 | PID-5 | A4      | 869   |
| EID-6 | PID-6 | A3      | 231   |

For each id column, it must map to all other id columns and target columns uniquely. 

Case 1: 

- `EID-1` could map to only `PID-1` at `PID` column, and map to only `A1` in `Element` column. 
- `PID-1` could map to only `EID-1` at `EID` column, and map to only `A1` in `Element` column. 

In this case, a unique ID pairing `EID-1`, `PID-1` is successful. One could use `EID-1` to get `PID-1` and `A1`, or use `PID-1` to get `EID-1` and `A1`.

Case 2:

- `EID-2` could map to both `PID-2` and `PID-3` at `PID` column, and map to only `A2` in `Element` column. 
- `PID-2` could map to only `EID-2` at `EID` column, and map to only `A2` in `Element` column. 
- `PID-3` could map to only `EID-2` at `EID` column, and map to only `A2` in `Element` column. 

Since `EID-2` maps to two entries at `PID` column, it is rejected to be a good ID. All linked entries including `PID-2` and `PID-3` are also removed. 

The final output:

| EID   | PID   | Element |
| ----- | ----- | ------- |
| EID-1 | PID-1 | A1      |
| EID-3 | PID-4 | A1      |
| EID-6 | PID-6 | A3      |

*biodatatools command: `join_IDMap`*  

Sometimes IDMaps are generated from multiple sequencing library layouts. For example, one IDMap captures PID and EID, and the other IDMap captures PID and Element. In such case, one may need to join multiple IDMaps as one using the shared IDs to get a combined IDMap for downstream analysis. 

### PRO-cap analysis

An analysis pipeline for PRO-cap analysis is available in rmsp-library. 

In the post-alignment step, the command `process_PROcap_bam_to_bigwig` could be used to convert the alignment bam file to bigwig files. The command will output the 5' end of the RNA (For PRO-cap, it indicates the TSS position) on plus (`prefix_5pl.bw`) and minus strand (`prefix_5mn.bw`).  Similarly, the command will output the 3' end of the RNA (For PRO-seq, it indicates the RNA polymerase position) on plus (`prefix_3pl.bw`) and minus strand (`prefix_3mn.bw`).  

The command `process_PROcap_bam_to_TSS_RNA_len` provides another view on the data, where it stores a collection of distances originated from the TSS on plus (`prefix_dpl.bed.bgz`) and minus strand (`prefix_dmn.bed.bgz`). An additional command `merge_PROcap_TSS_RNA_len` could be useful when merging multiple TSS_RNA_len files  (e.g. merging replicates). The command `summarize_PROcap_TSS_RNA_len` produces a table of the RNA lengths based on the TSS_RNA_len files. 

The command `generate_genebody_TSS_ratio_table` helps to generate the ratio of gene body / TSS reads. For PRO-cap where TSS is detected from capped RNA, the gene body / TSS ratio should be much lower than that detected in the control library (uncapped RNA). 

The commands `process_bigwigs_to_count_table` , `process_count_tables_to_correlation_table`   and `plot_count_tables_correlation` helps summarize replicate correlation in a table format or a correlation plot. 

The command `generate_PROcap_stat_table` helps to generate a summary table on the PRO-cap libraries. Here is a description on the json file containing the dictionary with keys and input files when using the command: 

| Keys                       | Input                                                        |
| -------------------------- | ------------------------------------------------------------ |
| Raw read pairs             | The fastqc output of the raw read pairs.                     |
| Trimmed read pairs         | The fastqc output of the trimmed read pairs.                 |
| Uniquely mapped read pairs | The bam statistics file generated using `samtools coverage` on the uniquely mapped bam file, or the bam file itself (where `samtools` is automatically run to generate the statistics). |
| Deduplicated read pairs    | The bam statistics file generated using `samtools coverage` on the deduplicated bam file, or the bam file itself (where `samtools` is automatically run to generate the statistics). |
| Spike-in read pairs        | The bam statistics file generated using `samtools coverage` on the bam file, or the bam file itself (where `samtools` is automatically run to generate the statistics). Only reference name in `-spikein_chrom_sizes` are considered as spike-in read pairs. |
| Sense read pairs           | A bigwig file for reads on the plus / sense strand.          |
| Antisense read pairs       | A bigwig file for reads on the minus / antisense strand.     |
| Median RNA length          | A TSS_RNA_len summary text file generated by biodatatools command  `summarize_PROcap_TSS_RNA_len`. |
| Gene body ratio            | A gene body / TSS ratio table generated by biodatatools command `generate_genebody_TSS_ratio_table` |
| Replicates correlation     | A correlation table generated by biodatatools command `process_count_tables_to_correlation_table` |
| XXX elements               | A element-call bed file generated by peak-calling tools such as PINTS. The prefix could be any of the different types of elements (e.g. Bidirectional, Divergent and Unidirectional). |

### STARR-seq analysis

An analysis pipeline for STARR-seq analysis is available in rmsp-library. 

In STARR-seq, we measure element activity as the power to transcribe DNA to RNA. When interpreting the data, this is reflected by the measured number of copies of RNA (RNA count) divided by number of copies of DNA (DNA count) in the system. For processing specific sequence library layouts to obtain RNA and DNA counts, please see the section *Fastq processing with complex read layout*. 

To combine DNA and RNA counts from multiple files, the command `merge_STARR_element_counts` is used. One could obtain the ratio of log RNA/DNA counts of elements to negative controls as the logFC using the command `generate_STARR_logFC_by_limma`. The command `generate_STARR_activity_call`  is applied to determine the element activity call. 

The biodatatools commands `plot_STARR_ranked_logFCs`,  `plot_STARR_replicates_correlation` and `plot_STARR_orientation_correlation` provide plots for QC purpose. 



### General plotting hints

This section will be expanded in the future.

## Files

This section will be expanded in the future. 

Common file types

- bigwig
- BED related
- GFF3 / GTF
- VCF
- FASTA / FASTQ
- SAM / BAM
- chrom_size

Other file types 

- TSS_RNA_len
- genebody_TSS_ratio_table



## All Commands

The naming convention of command prefixes is described below. 


- check - Check for certain information or file integrity. Usually the output is not parseable
- convert - Convert file into a different format while the stored data should remain the same
- downsample - Downsample data. Input and output data type should be the same
- filter - Create a new file that retains data entries matching the criteria
- generate - Generate new file that usually serves a different purpose than the input data.
- join - Join multiple files storing contents with complementary information (usually same data type) into one file
- merge - Merge multiple files storing additional contents (same data type) into one file
- modify - Create a new file with certain values modified
- plot - Create a plot based on the inputs. 
- process - Process files from one data type into some other data type. 
- summarize - Summarize data statistics

### convert_bedgraph_to_bigwig
*version: 20240501*
Convert bedgraph into bigwig files.
#### Parameters
- **-i**: Input bedgraph file
- **-g**: Chrom size file
- **-o**: Output bigwig file
- **-autosort**: [optional] Perform sorting on bedgraph file before running bedGraphToBigWig. Set to *false* if you are sure that your input files are sorted to reduce running time. [default: True]
- **-filter_chr**: [optional] Remove chromosomes in bedgraph file that are not present in chrom size file [default: False]
- **-nthread**: [optional] Number of threads used in sorting [default: 1]
### process_PROcap_bam_to_bigwig
*version: 20240423*
Convert GROcap/PROcap/GROseq/PROseq bam file to bigwig files (paired-end reads). Returns 4 bigwig files representing 5' and 3' end of the molecules on plus or minus strand. See PRO-cap design for more explanations about rna_strand.
#### Parameters
- **-i**: Input bam file
- **-g**: Chrom size file
- **-o**: Output bigwig file prefix
- **-paired_end**: Specify *true* if paired-end sequencing and *false* for single-end sequencing
- **-rna_strand**: Indicate whether RNA strand is forward or reverse. In paired-end, forward implies that the first bp of read 1 is 5'. reverse implies that the first bp of read 2 is 5'
### process_PROcap_bam_to_TSS_RNA_len
*version: 20240501*
Convert GROcap/PROcap/GROseq/PROseq bam file to bed files Returns 2 bed files with the 4th column as a comma separated list of RNA distances from TSS.
#### Parameters
- **-i**: Input bam file
- **-o**: output bed file prefix. Two files, _dpl.bed.bgz and _dmn.bed.bgz are output
- **-paired_end**: Specify *true* if paired-end sequencing and *false* for single-end sequencing
- **-rna_strand**: Indicate whether RNA strand is forward or reverse. In paired-end, forward implies that the first bp of read 1 is 5'. reverse implies that the first bp of read 2 is 5'
- **-min_rna_len**: [optional] Minimum RNA length to record [default: 0]
- **-max_rna_len**: [optional] Maximum RNA length to record [default: 100000]
- **-g**: [optional] Chrom size file. If provided, only chromosomes in the chrom size file are retained. [default: None]
### merge_PROcap_TSS_RNA_len
*version: 20240430*
Merge PROcap TSS RNA len files.
#### Parameters
- **-i**: Input files
- **-o**: Output file
### summarize_PROcap_TSS_RNA_len
*version: 20240501*
Summarize the PROcap TSS RNA len files into min, median, mean and max of RNA lengths.
#### Parameters
- **-i**: Input files
- **-o**: Output file
### generate_genebody_TSS_ratio_table
*version: 20240501*
Generate gene body TSS ratio table. For capped RNA reads, the 5' end should be much more dominant near the promoter TSS region than the transcript region.	The ratio of gene body reads to TSS reads serves as a quality measure for capped RNA sequencing experiments.
#### Parameters
- **-label**: Sample labels
- **-ibwpl**: Input bigwig file (plus/sense strand on chromosomes)
- **-ibwmn**: Input bigwig file (minus/antisense strand on chromosomes)
- **-iga**: Input gene annotations used in calculating the gene body TSS ratio. One may want to pre-filter the annotations to get a specific set of genes prior to running this command.
- **-o**: Output file
- **-mode**: [optional] Only accept heg or all. In heg mode, only the specified ratio of top highly expressed genes are used to calculate the ratio. In all mode, all genes are used to calculate the ratio. [default: heg]
- **-gb_dc_tss_forward_len**: [optional] Forward len of discarded part around TSS when obtaining the gene body region [default: 500]
- **-gb_dc_tss_reverse_len**: [optional] Reverse len of discarded part around TSS when obtaining the gene body region [default: 0]
- **-gb_dc_tts_forward_len**: [optional] Forward len of discarded part around TTS when obtaining the gene body region [default: 1]
- **-gb_dc_tts_reverse_len**: [optional] Reverse len of discarded part around TTS when obtaining the gene body region [default: 499]
- **-tss_forward_len**: [optional] Forward len of TSS region [default: 500]
- **-tss_reverse_len**: [optional] Reerse len of TSS region [default: 0]
- **-heg_top_ratio**: [optional] In heg mode, the specified ratio of top expressed genes used for calculating gene body TSS ratio [default: 0.1]
- **-heg_tss_forward_len**: [optional] Forward len of TSS region when considering the gene expression [default: 1000]
- **-heg_tss_reverse_len**: [optional] Reverse len of TSS region when considering the gene expression [default: 100]
### process_bed_overlapped_regions
*version: 20240801*
Process and merge bed overlapped regions. Two criteria, min overlap length and min overlap ratio are used to define overlap between two regions.
#### Parameters
- **-i**: Input bed files
- **-o**: Output bed file
- **-stranded**: [optional] If *true*, regions from different strands are never merged. [default: False]
- **-min_overlap_len**: [optional] Minimum overlap length in bp to connect two regions [default: 1]
- **-min_overlap_ratio**: [optional] Minimum overlap ratio (of the smaller region) to connect two regions [default: 0]
- **-mode**: [optional] Strategy to merge overlapped regions. Available mode includes *union* and *best* [default: union]
- **-func**: [optional] Function used in certain mode. In *best* mode, this corresponds to the scoring function for the region [default: None]
### filter_bed
*version: 20240901*
Filter bed entries. 
#### Parameters
- **-i**: Input bed file
- **-o**: Output bed file
- **-bedx**: [optional] Use BEDXReader instead of standard BEDReader with bedx indicating the number of basic field in bed format [default: None]
- **-fieldnames**: [optional] Additional field names for bed [default: None]
- **-filter_func**: [optional] Function to filter bed [default: None]
- **-overlap_regions**: [optional] Regions indicated by bed files. A bed entry is kept only if it overlaps with any listed region. [default: []]
- **-non_overlap_regions**: [optional] Regions indicated by bed files. A bed entry is kept only if it does not overlap with any listed region. [default: []]
- **-stranded**: [optional] Whether strand is considered when defining two regions as overlap [default: False]
- **-min_overlap_len**: [optional] Minimum overlap length in bp to define two regions as overlap [default: 1]
- **-min_overlap_ratio**: [optional] Minimum overlap ratio (of the smaller region) to define two regions as overlap [default: 0]
### modify_fasta_names
*version: 20240515*
Modify fasta entries' names. This method is deprecated and replaced by a more general method `modify_fasta`
#### Parameters
- **-i**: Input fasta file
- **-o**: Output fasta file
- **-func**: Function to modify fasta name. Either a python function or a string to be evaluated as python lambda function. For example, to add a prefix, `lambda x: "PREFIX_" + x`
### modify_fasta
*version: 20240801*
Modify fasta entries
#### Parameters
- **-i**: Input fasta file
- **-o**: Output fasta file
- **-name_func**: [optional] Function to modify fasta name. Either a python function or a string to be evaluated as python lambda function. For example, to add a prefix, `lambda x: "PREFIX_" + x` [default: None]
- **-seq_func**: [optional] Function to modify fasta sequence. Either a python function or a string to be evaluated as python lambda function [default: None]
### filter_fasta
*version: 20240801*
Filter fasta entries
#### Parameters
- **-i**: Input fasta file
- **-o**: Output fasta file
- **-filter_func**: [optional] Function to filter fasta [default: None]
- **-remove_duplicates_mode**: [optional] Remove duplicated entries. Available modes include name, seq, seq_ignorecase, entry, entry_ignorecase [default: None]
### extract_fasta_names
*version: 20240801*
Extract names from a fasta file to a text file
#### Parameters
- **-i**: Input fasta file
- **-o**: Output text file
### generate_chrom_size
*version: 20240501*
Create a chrom size file from fasta
#### Parameters
- **-i**: Input fasta file
- **-o**: Output chrom size file
### modify_bigwig_values
*version: 20240423*
Modify bigwig values according to the func
#### Parameters
- **-i**: Input bigwig file
- **-o**: Output bigwig file
- **-func**: Function to modify bigwig. Either a python function or a string to be evaluated as python lambda function. For example, to convert all positive values into negative values, `lambda x: x * -1`
### filter_bigwig_by_chroms
*version: 20240501*
Filter bigwig entries by chromosomes
#### Parameters
- **-i**: Input bigwig file
- **-o**: Output bigwig file
- **-chroms**: Seleted chromosomes retained in the output
### merge_bigwig
*version: 20240501*
Merge multiple bigwig files into one file. If the bigWig file contains negative data values, threshold must be properly set. An option remove_zero is added to remove entries with zero values.
#### Parameters
- **-i**: Input bigwig files
- **-g**: chrom size file
- **-o**: output bigwig file
- **-threshold**: [optional] Threshold. Set to a very negative value, e.g. -2147483648, if your bigwig contains negative values. [default: None]
- **-adjust**: [optional] Adjust [default: None]
- **-clip**: [optional] Clip [default: None]
- **-max**: [optional] Max [default: False]
- **-remove_zero**: [optional] _ [default: False]
- **-autosort**: [optional] Perform sorting on bedgraph file before running bedGraphToBigWig. Set to *false* if you are sure that your input files are sorted to reduce running time. [default: True]
- **-filter_chr**: [optional] Remove chromosomes in bedgraph file that are not present in chrom.sizes file [default: False]
- **-nthread**: [optional] Number of threads used in sorting [default: 1]
### subsample_bigwig
*version: 20240501*
Subsample multiple bigwig files into target values. For example, if bwpl contains 100 counts and bwmn contains 200 counts, and n = 50, then sum of read counts in output_bwpl and output_mn will be 50 but the ratio of read counts is not kept at 1:2. This function assumes int value in bigwig value. This function supports positive / negative read counts.
#### Parameters
- **-ibws**: Input bigwig files
- **-obws**: Output bigwig files
- **-n**: Target number to subsample
- **-seed**: Random seed used in subsampling
### normalize_bigwig
*version: 20240501*
Normalize bigwig files. 
#### Parameters
- **-ibws**: Input bigwig files
- **-obws**: Output bigwig files
- **-mode**: [optional] Mode to normalize bigwig files. Only rpm is supported now. [default: rpm]
- **-nthread**: [optional] Number of threads used to create normalized bigwig files. [default: -1]
### subsample_bam
*version: 20240501*
Subsample a bam file into exact number of entries. Alignments of n total reads (including unmapped reads) will be retrieved.
#### Parameters
- **-i**: Input bam file
- **-o**: Output bam file
- **-n**: Target number to subsample
- **-seed**: Random seed used in subsampling
- **-nthread**: [optional] Number of threads for compression [default: 1]
### filter_bam_NCIGAR_reads
*version: 20240501*
Remove reads with any alignment that contain N in the CIGAR string. 
#### Parameters
- **-i**: Input bam file
- **-o**: Output bam file
- **-nthread**: [optional] Number of threads used in compression [default: 1]
### process_bigwigs_to_count_table
*version: 20240601*
Process bigwig into count table, either in a specific set of regions, or genomewide bins
#### Parameters
- **-sample_names**: Input sample names
- **-i**: Input bigwig files
- **-o**: Output count table file
- **-region_file**: [optional] A bed file containing regions to calculate bigwig counts [default: None]
- **-bin_size**: [optional] If regions not provided, generate genomewide counts binned in bin_size [default: None]
- **-g**: [optional] chrom size file. If provided, only use the selected chromosomes for genomewide counts [default: None]
### process_count_tables_to_correlation_table
*version: 20240501*
Process count tables into a correlation table. Currently Pearson correlation is used.
#### Parameters
- **-i**: Input files
- **-o**: Output file
- **-filter_func**: [optional] A function that takes in a pair of sample 1 and sample 2 count values to see if this pair should be retained or discarded [default: None]
- **-value_func**: [optional] A function that modifies count values [default: None]
- **-keys**: [optional] Only the selected samples are used to generate the correlation table [default: None]
### generate_union_TSS
*version: 20240501*
Generate a union TSS +x -y bp region for classifying distal / proximal regions.
#### Parameters
- **-i**: Input gff file
- **-o**: Output file
- **-forward_len**: Length to extend in the forward strand. Use 1 if only TSS is chosen. For TSS-500bp to TSS+250bp, the region is 750bp long and forward_len should be set to 250.
- **-reverse_len**: Length to extend in the reverse strand. For TSS-500bp to TSS+250bp, the region is 750bp long and reverse_len should be set to 500.
- **-filter_func**: [optional] Function to filter the transcripts [default: None]
### generate_union_transcripts
*version: 20240501*
Deprecated - replaced with a more general method generate_geneannotations_union_features. Generate union transcripts regions. 
#### Parameters
- **-i**: Input gff file
- **-o**: Output file
- **-filter_func**: [optional] Function to filter the transcripts [default: None]
### generate_geneannotations_union_features
*version: 20240901*
Generate union feature regions.
#### Parameters
- **-i**: Input genome annotation file
- **-o**: Output genome annotation file
- **-feature**: Feature to be selected to generate the union regions
- **-filter_func**: [optional] Function to filter the feature [default: None]
### filter_geneannotations
*version: 20240501*
Filter genome annotations
#### Parameters
- **-i**: Input genome annotation file
- **-o**: Output genome annotation file
- **-filter_func**: [optional] Function to filter genome annotations [default: None]
- **-remove_overlapping_genes**: [optional] Remove overlapping genes [default: False]
- **-overlapping_genes_extension**: [optional] Expand the genes before finding overlapping genes for removal [default: 0]
### check_sequencing_files_md5
*version: 20240501*
Check sequencing files organized in a particular layout.
Your input i should be the raw_data directory as specified below

The directory has a layout as:

```
raw_data/
|___ LibraryName1/
|_______ MD5.txt
|_______ L1_1.fq.gz
|_______ L1_2.fq.gz
|___ LibraryName2/
|_______ MD5.txt
|_______ L2_1.fq.gz
|_______ L2_2.fq.gz
```

#### Parameters
- **-i**: Input folder
### generate_PROcap_stat_table
*version: 20240623*

Generate a statistics table for PRO-cap data. The method accepts a list of entries as input. Each entry is a dictionary, where keys could be one of the following and values are the corresponding files:

- `Raw read pairs`: Accepts a zip file generated by fastqc
- `Trimmed read pairs`: Accepts a zip file generated by fastqc
- `Uniquely mapped read pairs`: Accepts a bam stat file generated by `samtools coverage` 
- `Deduplicated read pairs`: Accepts a bam stat file generated by `samtools coverage`
- `Spike-in read pairs`: Accepts a bam stat file generated by `samtools coverage`. `spikein_chrom_sizes` must be provided
- `Sense read pairs`: Accepts a bigwig file (usually ended with pl.bw)
- `Antisense read pairs`: Accepts a bigwig file (usually ended with mn.bw)
- `Median RNA length`: Accepts a table file generated by `biodatatools summarize_PROcap_TSS_RNA_len`
- `Gene body ratio`: Accepts a table file generated by `biodatatools generate_genebody_TSS_ratio_table`
- `Replicates correlation`: Accepts a table file generated by `biodatatools process_count_tables_to_correlation_table`
- `XXXX elements`: The field could be any string that ends with `elements`. Any element-call file in BED format is accepted. 

If `proximal_regions` is provided, statistics will be reported for both distal and proximal elements. If `transcripts_regions` is also provided, statistics will be reported for distal intragenic, distal intergenic and proximal elements. 

#### Parameters
- **-i**: Input json file
- **-o**: Output file
- **-proximal_regions**: [optional] A BED file that indicates proximal regions [default: None]
- **-transcripts_regions**: [optional] A BED file that indicates all transcripts regions [default: None]
- **-spikein_chrom_sizes**: [optional] chrom size file for spike-in chromosomes. Required only if `Spike-in read pairs` is reported [default: None]
- **-nthread**: [optional] Number of threads [default: 1]
### check_RNAseq_strand_specificity
*version: 20231030*

Checks for RNA-seq design - whether it is a strand specific RNA-seq or not
If you know the library design, you can use this method to validate. 

Outputs --fr-stranded and --rf-stranded abundances. If the percentages are close to 50% it is unlikely strand specific.	

#### Parameters
- **-index_file**: kallisto index file
- **-f1**: Read1 fastq file
- **-f2**: Read2 fastq file
- **-nthread**: [optional] Number of threads [default: 1]
### process_sequencing_reads_to_delimited_sequences
*version: 20240624*

Process sequencing reads (FASTA/FASTQ) into delimited sequences. The method enables a flexible layout set up for easy extraction of sub-sequences.

#### Parameters
- **-o**: Output delimited file
- **-f1**: Input sequence file (Read 1)
- **-layout1**: Layout (json format) corresponding to f1
- **-f2**: [optional] Input sequence file (Read 2). Required for paired-end sequencing. [default: None]
- **-layout2**: [optional] Layout (json format) corresponding to f2. Required for paired-end sequencing. [default: None]
- **-max_edit_distance**: [optional] Maximum edit distance when performing constant sequence matching [default: 1]
- **-min_last_anchor_match**: [optional] The minimum matching length required for the last segment [default: 1]
- **-keep_unmatch**: [optional] If True, __UNMATCH__ is indicated in the columns. If False, the reads are not retained.  [default: False]
- **-reverse_complements**: [optional] The columns you wish to reverse complement in the output [default: []]
- **-column_names**: [optional] Column names in the output. If not provided, columns will be auto numbered [default: []]
- **-nthread**: [optional] Number of threads [default: 1]
- **-reads_per_thread**: [optional] Number of reads a thread should handle at a time. [default: 1000000]
### process_delimited_sequences
*version: 20241020*
Process delimited sequences into useful information. 
#### Parameters
- **-i**: Input delimited sequence file
- **-o**: Output delimited sequence file
- **-filter**: [optional] Remove certain rows (entries) that do not match the criteria [default: []]
- **-filter_func**: [optional] Filter function used in filter [default: []]
- **-rename**: [optional] Rename columns [default: None]
- **-trim**: [optional] Trim target sequence by removing any identified query sequence and beyond. Example: `-trim 'column=Element;trimseq=ACGGT;direction=1'` [default: []]
- **-refs**: [optional] References [default: None]
- **-match**: [optional] Align sequence to the reference and retrieve the identity of it [default: []]
- **-align**: [optional] Align sequence to the reference and retrieve the alignment position [default: []]
- **-map**: [optional] Map the column values according to the reference map [default: []]
- **-cluster**: [optional] Cluster the sequences [default: []]
- **-quantify**: [optional] Use the values from all non-quantify columns as unique keys to group sequences from the quantify columns.  [default: []]
- **-quantify_option**: [optional] Options for -quantify [default: None]
- **-merge**: [optional] Merge values from the merge column grouped by non-merge columns as unique keys [default: []]
- **-merge_option**: [optional] Options for -merge [default: ]
- **-order**: [optional] Order of the output columns [default: []]
- **-nthread**: [optional] Number of threads [default: 1]
### cluster_delimited_sequences
*version: 20241023*
Cluster from multiple delimited files
#### Parameters
- **-i**: Input delimited files
- **-output_prefix**: Output prefix
- **-column**: Corresponding column name to use for clustering in each delimited file
- **-filter_func**: [optional] Pre-filtering for the clustering [default: None]
- **-mode**: [optional] Clustering mode [default: connected]
- **-max_edit_distance**: [optional] Max edit distance in clustering [default: 1]
- **-nthread**: [optional] Number of threads for clustering [default: 1]
### concat_delimited
*version: 20240715*
Concatenate multiple delimited files into one. All input files should have the same headers
#### Parameters
- **-i**: Input delimited files
- **-o**: Output delimited file
### generate_IDMap_from_delimited
*version: 20241024*
Generate an IDMap from the delimited file.
#### Parameters
- **-i**: Input delimited file
- **-o**: Output ID Map file
- **-id_column**: ID columns
- **-count_column**: Count column
- **-target_column**: [optional] Target columns [default: []]
- **-skip_targets**: [optional] A list of target entries that should be removed from the ID or target columns [default: ['__UNMATCH__', '__AMBIG__']]
- **-min_perid_dominant_count**: [optional] Minimum count for each ID [default: 10]
- **-max_perid_target_no**: [optional] Maximum targets per ID [default: -1]
- **-min_perid_dominant_count_ratio**: [optional] Minimum dominant count ratio [default: 0.8]
- **-min_first_and_second_dominant_fold_difference**: [optional] Minimum count ratio between the first and second dominant targets [default: 2]
### join_IDMap
*version: 20241024*
Join multiple ID Maps into one ID Map. 
#### Parameters
- **-i**: Input ID Map files
- **-o**: Output ID Map file
- **-id_column**: ID columns
- **-target_column**: [optional] Target columns [default: []]
### annotate_bed_classes
*version: 20240925*
Annotate multiple bed files by names. 
#### Parameters
- **-i**: Input annotated bed files
- **-o**: Output annotated bed file
- **-clsname**: Class names corresponding to the input annotated bed files.
- **-column**: [optional] The column to insert the new annotation [default: None]
### annotate_bed_overlaps
*version: 20240925*
Annotate bed file by overlaps. 
#### Parameters
- **-i**: Input annotated bed file
- **-r**: Input reference file
- **-o**: Output annotated bed file
- **-pcls**: Name for overlapped entries
- **-ncls**: Name for non-overlapped entries
- **-column**: [optional] The column to insert the new annotation [default: None]
### annotate_bed_directionality_index
*version: 20240925*
Annotate bed file with directionality index
#### Parameters
- **-i**: Input annotated bed file
- **-ipl**: Input plus-strand bigwig file
- **-imn**: Input minus-strand bigwig file
- **-o**: Output annotated bed file
- **-column**: [optional] The column to insert the new annotation [default: None]
### summarize_bed_annotation_counts
*version: 20240925*
Summarize annotated bed files into a table
#### Parameters
- **-i**: Input annotated bed files
- **-name**: Sample names of the inputs
- **-o**: Output table file
- **-func**: [optional] A function to create a unique group. By default the forth to last columns are all used to create the unique group.  [default: None]
### modify_bed_annotation
*version: 20240925*
Modify a bed annotation file
#### Parameters
- **-i**: Input bed annotation files
- **-o**: Output bed annotation file
- **-func**: A function to modify each entry
### plot_count_tables_correlation
*version: 20240901*
Plot two-way correlation between samples in the count table
#### Parameters
- **-i**: Input count table file
- **-o**: Output plot file
- **-filter_func**: [optional] Filtering function applied to each pair of values between two samples. [default: None]
- **-value_func**: [optional] Value function applied to the count table before plotting. Applied after filter_func. [default: None]
- **-keys**: [optional] Selected keys to plot correlation [default: []]
- **-labels**: [optional] A dictionary to map label in count table to names used in plot [default: None]
- **-plot_kw**: [optional] _ [default: {}]
- **-fig_change_kw**: [optional] Figure changes kw [default: {}]
- **-fig_save_kw**: [optional] Figure save kw [default: {}]
### merge_STARR_element_counts
*version: 20240801*
Merge multiple STARR element counts into a table. Usually element counts from different replicates in the same experiments are merged
#### Parameters
- **-idna**: List of DNA element counts files
- **-irna**: List of RNA element counts files
- **-o**: Output file
- **-missing_value**: [optional] Strategy to deal with missing value in certain element counts file. Currently only 'zero' is supported, where missing values are assumed to have zero counts. [default: zero]
- **-filter_func**: [optional] A function to filter unwanted entries [default: None]
- **-element_column**: [optional] The names of input columns as the element key. If multiple input colums are provided, they will be joined using column_sep [default: ['Element']]
- **-count_column**: [optional] The name of the count column [default: Count]
- **-column_sep**: [optional] The delimiter used to join multiple column names [default: .]
### generate_STARR_logFC_by_limma
*version: 20240801*
Generate logFCs using a limma-based method. 
#### Parameters
- **-i**: Input element counts file
- **-o**: Output activity call file
- **-n**: Negative control file
- **-f**: [optional] A sample-group table file. If not provided, this is auto determine based on the column names in the element count file [default: None]
### generate_STARR_activity_call
*version: 20240801*
Generate STARR activity call. The activity of an element in one orientation could be called as PositiveActivity, NegativeActivity or Inactive. When combining both orientations, an additional activity Ambig will be assigned if the activity from the two orientations are different. Elements with missing data will be assigned NA activity
#### Parameters
- **-i**: Input logFC file
- **-n**: Negative control file
- **-o**: Output activity call file
- **-fwd_suffix**: [optional] Suffix for element in forward orientation [default: .fwd]
- **-rev_suffix**: [optional] Suffix for element in reverse orientation [default: .rev]
### plot_STARR_ranked_logFCs
*version: 20240901*
Create a ranked plot for STARR logFCs
#### Parameters
- **-i**: Input logFC files
- **-name**: Names corresponding to the inputs
- **-o**: Output plot file
- **-group**: [optional] A dictionary containing group name as key and list of group elements as values [default: {}]
- **-default_group_name**: [optional] If an element does not appear in any group, it will be assigned to the default group [default: Elements]
- **-plot_kw**: [optional] Plot arguments [default: {}]
- **-plot_kw_dict**: [optional] Group-specific plot arguments [default: {}]
- **-line_kw**: [optional] Line arguments [default: {}]
- **-fig_change_kw**: [optional] Figure change arguments [default: {}]
- **-fig_save_kw**: [optional] Figure save arguments [default: {}]
### plot_STARR_replicates_correlation
*version: 20241001*
Create replicates correlation plot for STARR logFCs
#### Parameters
- **-i**: Input STARR logFC file
- **-o**: Output plot file
- **-group**: [optional] A dictionary containing replicate name as key and list of DNA, RNA key as values [default: None]
- **-plot_kw**: [optional] Plot arguments [default: {}]
- **-fig_change_kw**: [optional] Figure change arguments [default: {}]
- **-fig_save_kw**: [optional] Figure save arguments [default: {}]
### plot_STARR_orientation_correlation
*version: 20241001*
Create orientation correlation plot for STARR
#### Parameters
- **-i**: Input STARR activity file
- **-o**: Output plot file
- **-plot_kw**: [optional] Plot arguments [default: {}]
- **-fig_change_kw**: [optional] Figure change arguments [default: {}]
- **-fig_save_kw**: [optional] Figure save arguments [default: {}]
### plot_sequence_library_layouts
*version: 20241022*
Create sequence library layout plot
#### Parameters
- **-i**: A dictionary or json that indicates the input files
- **-o**: Output plot file
- **-plot_kw**: [optional] Plot arguments [default: {}]
- **-compose_kw**: [optional] Figure panel compose arguments [default: {}]
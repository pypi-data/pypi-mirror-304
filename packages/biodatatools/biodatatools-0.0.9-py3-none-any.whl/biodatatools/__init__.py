import sys
import simplevc
simplevc.register(sys.modules[__name__], "0.0.9")

from commonhelper import convert_to_bool


def check_binaries_validity(*binary_names): # Change to decorator in the future
	import shutil
	missing_binary_names = [binary_name for binary_name in binary_names if shutil.which(binary_name) is None]
	if len(missing_binary_names) > 0:
		raise Exception("The following binaries are not found: " + ",".join(binary_names))
	
def bash_command(cmd):
	import subprocess
	p = subprocess.run(cmd, shell=True, executable='/bin/bash')
	if p.returncode != 0:
		raise Exception("Bash command fails: " + cmd)
	
#  
# Common file conversions
#  
@vt(
	description="Convert bedgraph into bigwig files", 
	helps=dict(
		i="Input bedgraph file", g="chrom size file", o="output bigwig file",
		autosort="Perform sorting on bedgraph file before running bedGraphToBigWig",
		filter_chr="Remove chromosomes in bedgraph file that are not present in chrom.sizes file", 
		nthread="Number of threads used in sorting")
)
@vc
def _convert_bedgraph_to_bigwig_20240423(i:str, g:str, o:str, autosort:convert_to_bool=False, filter_chr:convert_to_bool=False, nthread:int=1):
	'''
	Convert bedgraph into bigwig files. Auto sort and filter bedgraphs prior to calling bedGraphToBigWig
	:param i: Input bedgraph file
	:param g: chrom.size file
	:param o: Output bw file
	:param autosort: Perform sorting on bedgraph file before running bedGraphToBigWig
	:param filter_chr: Remove chromosomes in bedgraph file that are not present in chrom.sizes file
	'''
	import os
	import tempfile
	from biodata.delimited import DelimitedReader, DelimitedWriter
	check_binaries_validity("zcat", "sort", "bedGraphToBigWig")
	tmpfiles = []
	if filter_chr:
		inputfile = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
		tmpfiles.append(inputfile)
		with DelimitedReader(g) as dr:
			chromosomes = set([d[0] for d in dr])
		with DelimitedReader(i) as dr, DelimitedWriter(inputfile) as dw:
			for d in dr:
				if d[0] in chromosomes:
					dw.write(d)
		i = inputfile
	
	if autosort:
		inputfile = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
		tmpfiles.append(inputfile)
		if nthread > 1:
			added_param = f"--parallel={nthread} "
		else:
			added_param = ""
		if i.endswith(".gz"):
			bash_command(f"zcat {i} | sort -k1,1 -k2,2n {added_param}> {inputfile}")
		else:
			bash_command(f"sort -k1,1 -k2,2n {added_param}{i} > {inputfile}")
		i = inputfile
		
	bash_command(f"bedGraphToBigWig {i} {g} {o}")
	for tmpfile in tmpfiles:
		os.unlink(tmpfile)
@vt(
	description="Convert bedgraph into bigwig files.", helps=dict(
		i="Input bedgraph file", g="Chrom size file", o="Output bigwig file",
		autosort="Perform sorting on bedgraph file before running bedGraphToBigWig. Set to *false* if you are sure that your input files are sorted to reduce running time.",
		filter_chr="Remove chromosomes in bedgraph file that are not present in chrom size file", 
		nthread="Number of threads used in sorting")
)
@vc
def _convert_bedgraph_to_bigwig_20240501(i:str, g:str, o:str, autosort:convert_to_bool=True, filter_chr:convert_to_bool=False, nthread:int=1):
	import os
	import tempfile
	from biodata.delimited import DelimitedReader, DelimitedWriter
	
	check_binaries_validity("zcat", "sort", "bedGraphToBigWig")
	tmpfiles = []
	if filter_chr:
		inputfile = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
		tmpfiles.append(inputfile)
		with DelimitedReader(g) as dr:
			chromosomes = set([d[0] for d in dr])
		with DelimitedReader(i) as dr, DelimitedWriter(inputfile) as dw:
			for d in dr:
				if d[0] in chromosomes:
					dw.write(d)
		i = inputfile
	
	if autosort:
		inputfile = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
		tmpfiles.append(inputfile)
		if nthread > 1:
			added_param = f"--parallel={nthread} "
		else:
			added_param = ""
		if i.endswith(".gz"):
			bash_command(f"zcat {i} | sort -k1,1 -k2,2n {added_param}> {inputfile}")
		else:
			bash_command(f"sort -k1,1 -k2,2n {added_param}{i} > {inputfile}")
		i = inputfile
		
	bash_command(f"bedGraphToBigWig {i} {g} {o}")
	for tmpfile in tmpfiles:
		os.unlink(tmpfile)


# 
# PRO-cap/seq specific tools
#

@vt(description="Convert GROcap/PROcap/GROseq/PROseq bam file to bigwig files (paired-end reads). Returns 4 bigwig files representing 5' and 3' end of the molecules on plus or minus strand. See PRO-cap design for more explanations about rna_strand.", 
	helps=dict(i="Input bam file", g="Chrom size file", o="Output bigwig file prefix",
			paired_end="Specify *true* if paired-end sequencing and *false* for single-end sequencing",
			rna_strand="Indicate whether RNA strand is forward or reverse. In paired-end, forward implies that the first bp of read 1 is 5'. reverse implies that the first bp of read 2 is 5'"
			)
		)
@vc
def _process_PROcap_bam_to_bigwig_20240423(i:str, g:str, o:str, paired_end : convert_to_bool, rna_strand : str):
	import os
	import tempfile
	from mphelper import ProcessWrapPool
	
	check_binaries_validity("samtools", "bedtools", "zcat", "sort", "bedGraphToBigWig")
	
	tmpfiles = [tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name for _ in range(4)]
	bg5_pl, bg5_mn, bg3_pl, bg3_mn = tmpfiles
	thread = 16
	pwpool = ProcessWrapPool(4)
	if paired_end:
		tmpfiles_bam = [tempfile.NamedTemporaryFile(mode='w+', suffix=".bam", delete=False).name for _ in range(2)]
		bam5, bam3 = tmpfiles_bam		
		if rna_strand == "forward":
			bam5_pid = pwpool.run(bash_command, args=[f"samtools view -f 66 --write-index -@ {thread} -o {bam5} {i}"])
			bam3_pid = pwpool.run(bash_command, args=[f"samtools view -f 130 --write-index -@ {thread} -o {bam3} {i}"])
		elif rna_strand == "reverse":
			bam5_pid = pwpool.run(bash_command, args=[f"samtools view -f 130 --write-index -@ {thread} -o {bam5} {i}"])
			bam3_pid = pwpool.run(bash_command, args=[f"samtools view -f 66 --write-index -@ {thread} -o {bam3} {i}"])
		else:
			raise Exception()
		# Be careful of the strand. We assumed F1R2 setup 
		bgpl_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {bam5} -5 -strand + -bg > {bg5_pl}"], dependencies=[bam5_pid])
		bgmn_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {bam5} -5 -strand - -bg | awk {{'printf (\"%s\\t%s\\t%s\\t-%s\\n\", $1, $2, $3, $4)'}} > {bg5_mn}"], dependencies=[bam5_pid])
		bg3pl_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {bam3} -5 -strand - -bg > {bg3_pl}"], dependencies=[bam3_pid])
		bg3mn_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {bam3} -5 -strand + -bg | awk {{'printf (\"%s\\t%s\\t%s\\t-%s\\n\", $1, $2, $3, $4)'}} > {bg3_mn}"], dependencies=[bam3_pid])
	else:
		tmpfiles_bam = [] # No bam files needed
		bgpl_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {i} -5 -strand + -bg > {bg5_pl}"])
		bgmn_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {i} -5 -strand - -bg | awk {{'printf (\"%s\\t%s\\t%s\\t-%s\\n\", $1, $2, $3, $4)'}} > {bg5_mn}"])
		bg3pl_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {i} -3 -strand + -bg > {bg3_pl}"])
		bg3mn_pid = pwpool.run(bash_command, args=[f"bedtools genomecov -ibam {i} -3 -strand - -bg | awk {{'printf (\"%s\\t%s\\t%s\\t-%s\\n\", $1, $2, $3, $4)'}} > {bg3_mn}"])
		
	pwpool.run(_convert_bedgraph_to_bigwig_20240423, args=[bg5_pl, g, o + "_5pl.bw"], kwargs=dict(autosort=True, filter_chr=True), dependencies=[bgpl_pid])
	pwpool.run(_convert_bedgraph_to_bigwig_20240423, args=[bg5_mn, g, o + "_5mn.bw"], kwargs=dict(autosort=True, filter_chr=True), dependencies=[bgmn_pid])
	pwpool.run(_convert_bedgraph_to_bigwig_20240423, args=[bg3_pl, g, o + "_3pl.bw"], kwargs=dict(autosort=True, filter_chr=True), dependencies=[bg3pl_pid])
	pwpool.run(_convert_bedgraph_to_bigwig_20240423, args=[bg3_mn, g, o + "_3mn.bw"], kwargs=dict(autosort=True, filter_chr=True), dependencies=[bg3mn_pid])
	pwpool.get(wait=True)
	pwpool.close()
	for tmpfile in tmpfiles + tmpfiles_bam:
		os.unlink(tmpfile)

@vt(description="Convert GROcap/PROcap/GROseq/PROseq bam file to bed files Returns 2 bed files with the 4th column as a comma separated list of RNA distances from TSS", 
	helps=dict(i="Input bam file", o="output bed file prefix. Two files, _dpl.bed.gz and _dmn.bed.gz are output",
			paired_end="True: paired-end sequencing; False: single-end sequencing",
			rna_strand="Indicate whether RNA strand is forward or reverse. In paired-end, forward represents that first read is 5'.",
			min_rna_len="Minimum RNA length to record",
			max_rna_len="Maximum RNA length to record"
			)
		)
@vc
def _process_PROcap_bam_to_TSS_RNA_len_20240423(i, o, paired_end, rna_strand, min_rna_len=0, max_rna_len=100000): 
	'''
	'''
	import pysam
	from commonhelper import nested_default_dict
	from biodata.baseio import BaseWriter
	from biodata.bed import BEDPE
	
	def _to_position(alignment):
		position = alignment.reference_end if alignment.is_reverse else (alignment.reference_start + 1)
		strand = "-" if alignment.is_reverse else "+"
		return (alignment.reference_name, position, strand)

	if not paired_end:
		raise Exception("Single-end not supported yet.")
	saved_reads = {}
	TSS_counter = nested_default_dict(3, list)
	with pysam.AlignmentFile(i) as samfh: 
		for alignment in samfh:
			if alignment.query_name in saved_reads:
				prev_alignment = saved_reads.pop(alignment.query_name)
				alignment1 = prev_alignment if prev_alignment.is_read1 else alignment
				alignment2 = prev_alignment if prev_alignment.is_read2 else alignment
				p1 = _to_position(alignment1) # read1: Pol
				p2 = _to_position(alignment2) # read2: TSS
				
				b = BEDPE(p1[0], p1[1] - 1, p1[1], p2[0], p2[1] - 1, p2[1], strand1 = p1[2], strand2 = p2[2])
				if (b.chrom1 == b.chrom2
					and (   (b.strand1 == "+" and b.strand2 == "-" and b.start1 <= b.start2 and b.stop1 <= b.stop2 and min_rna_len <= b.stop2 - b.start1 <= max_rna_len)
						 or (b.strand1 == "-" and b.strand2 == "+" and b.start2 <= b.start1 and b.stop2 <= b.stop1 and min_rna_len <= b.stop1 - b.start2 <= max_rna_len))):
					
					
					d = b.stop2 - b.start1 if b.strand1 == "+" else b.stop1 - b.start2
					if rna_strand == "forward":
						strand = b.strand1
						if strand == "+":
							TSS_counter[strand][b.chrom1][b.genomic_pos1.start].append(d)
						else:
							TSS_counter[strand][b.chrom1][b.genomic_pos1.stop].append(d)
					elif rna_strand == "reverse":
						strand = b.strand2
						if strand == "+":
							TSS_counter[strand][b.chrom1][b.genomic_pos2.stop].append(d)
						else:
							TSS_counter[strand][b.chrom1][b.genomic_pos2.start].append(d)
					else:
						raise Exception()

			else:
				saved_reads[alignment.query_name] = alignment
		for output_file, strand in zip([f"{o}_dpl.bed.gz", f"{o}_dmn.bed.gz"], ["+", "-"]):
			with BaseWriter(output_file) as bwd:
				regions = TSS_counter[strand]
				for r in sorted(regions.keys()):
					positions = regions[r]
					for p in sorted(positions.keys()):
						v = sorted(positions[p])
						bwd.write(f"{r}\t{p - 1}\t{p}\t{','.join(list(map(str, v)))}\n")
@vt(description="Convert GROcap/PROcap/GROseq/PROseq bam file to bed files Returns 2 bed files with the 4th column as a comma separated list of RNA distances from TSS.", 
	helps=dict(i="Input bam file", o="output bed file prefix. Two files, _dpl.bed.bgz and _dmn.bed.bgz are output",
			paired_end="Specify *true* if paired-end sequencing and *false* for single-end sequencing",
			rna_strand="Indicate whether RNA strand is forward or reverse. In paired-end, forward implies that the first bp of read 1 is 5'. reverse implies that the first bp of read 2 is 5'",
			min_rna_len="Minimum RNA length to record",
			max_rna_len="Maximum RNA length to record",
			g="Chrom size file. If provided, only chromosomes in the chrom size file are retained."
			)
		)
@vc
def _process_PROcap_bam_to_TSS_RNA_len_20240501(i, o, paired_end, rna_strand, min_rna_len=0, max_rna_len=100000, g:str=None): 
	'''
	'''
	import pysam
	from commonhelper import nested_default_dict
	from biodata.baseio import BaseWriter
	from biodata.bed import BEDPE
	from biodata.delimited import DelimitedReader
	def _to_position(alignment):
		position = alignment.reference_end if alignment.is_reverse else (alignment.reference_start + 1)
		strand = "-" if alignment.is_reverse else "+"
		return (alignment.reference_name, position, strand)

	if not paired_end:
		raise Exception("Single-end not supported yet.")
	if g is not None:
		target_chromosomes = DelimitedReader.read_all(lambda ds: set(d[0] for d in ds), g)
	else:
		target_chromosomes = None
	saved_reads = {}
	TSS_counter = nested_default_dict(3, list)
	with pysam.AlignmentFile(i) as samfh: 
		for alignment in samfh:
			if target_chromosomes is not None and alignment.reference_name not in target_chromosomes:
				continue
			if alignment.query_name in saved_reads:
				prev_alignment = saved_reads.pop(alignment.query_name)
				alignment1 = prev_alignment if prev_alignment.is_read1 else alignment
				alignment2 = prev_alignment if prev_alignment.is_read2 else alignment
				p1 = _to_position(alignment1) # read1: Pol
				p2 = _to_position(alignment2) # read2: TSS
				
				b = BEDPE(p1[0], p1[1] - 1, p1[1], p2[0], p2[1] - 1, p2[1], strand1 = p1[2], strand2 = p2[2])
				if (b.chrom1 == b.chrom2
					and (   (b.strand1 == "+" and b.strand2 == "-" and b.start1 <= b.start2 and b.stop1 <= b.stop2 and min_rna_len <= b.stop2 - b.start1 <= max_rna_len)
						 or (b.strand1 == "-" and b.strand2 == "+" and b.start2 <= b.start1 and b.stop2 <= b.stop1 and min_rna_len <= b.stop1 - b.start2 <= max_rna_len))):
					
					
					d = b.stop2 - b.start1 if b.strand1 == "+" else b.stop1 - b.start2
					if rna_strand == "forward":
						strand = b.strand1
						if strand == "+":
							TSS_counter[strand][b.chrom1][b.genomic_pos1.start].append(d)
						else:
							TSS_counter[strand][b.chrom1][b.genomic_pos1.stop].append(d)
					elif rna_strand == "reverse":
						strand = b.strand2
						if strand == "+":
							TSS_counter[strand][b.chrom1][b.genomic_pos2.stop].append(d)
						else:
							TSS_counter[strand][b.chrom1][b.genomic_pos2.start].append(d)
					else:
						raise Exception()

			else:
				saved_reads[alignment.query_name] = alignment
		for output_file, strand in zip([f"{o}_dpl.bed.bgz", f"{o}_dmn.bed.bgz"], ["+", "-"]):
			with BaseWriter(output_file) as bwd:
				regions = TSS_counter[strand]
				for r in sorted(regions.keys()):
					positions = regions[r]
					for p in sorted(positions.keys()):
						v = sorted(positions[p])
						if strand == "-":
							v = sorted([e * -1 for e in v])
						bwd.write(f"{r}\t{p - 1}\t{p}\t{','.join(list(map(str, v)))}\n")						
@vt(
	description="Merge PROcap TSS RNA len files.",
	helps=dict(
		i="Input files", 
		o="Output file"
	)
)
@vc
def _merge_PROcap_TSS_RNA_len_20240430(i:list[str], o:str):
	from biodata.bed import BEDGraph, BEDGraphReader, BEDGraphWriter
	brs = [BEDGraphReader( f, dataValueType=lambda s: list(map(int, s.split(",")))) for f in i]
	with BEDGraphWriter(o, dataValueFunc=lambda v: ",".join(list(map(str, sorted(v))))) as bw:
		finished = False
		while not finished:
			min_region = None
			for br in brs:
				r = br.peek()
				if r is None:
					continue
				if min_region is None or min_region > r.genomic_pos:
					min_region = r.genomic_pos
			if min_region is not None:
				vs = []
				for br in brs:
					if br.peek() is not None and br.peek().genomic_pos == min_region:
						r = br.read()
						vs.extend(r.dataValue)
				bw.write(BEDGraph(min_region.name, min_region.zstart, min_region.ostop, vs))
			else:
				finished = True

@vt(
	description="Summarize the PROcap TSS RNA len files into min, median, mean and max of RNA lengths.",
	helps=dict(
		i="Input files", 
		o="Output file"
	)
)
@vc
def _summarize_PROcap_TSS_RNA_len_20240501(i:list[str], o:str):
	from biodata.baseio import BaseWriter
	from biodata.bed import BEDXReader
	import numpy as np
	dists = []
	for f in i:
		with BEDXReader(f, ["dist"], [lambda a: list(map(lambda x: abs(int(x)), a.split(",")))]) as br:
			for b in br:
				dists.extend(b.dist)
	with BaseWriter(o) as bw:
		bw.write(f"min\t{np.min(dists)}\n")
		bw.write(f"median\t{np.median(dists)}\n")
		bw.write(f"mean\t{np.mean(dists)}\n")
		bw.write(f"max\t{np.max(dists)}\n")

@vt(
	description="Generate gene body TSS ratio table. For capped RNA reads, the 5' end should be much more dominant near the promoter TSS region than the transcript region.	The ratio of gene body reads to TSS reads serves as a quality measure for capped RNA sequencing experiments.",
	helps=dict(
		label="Sample labels",
		ibwpl="Input bigwig file (plus/sense strand on chromosomes)",
		ibwmn="Input bigwig file (minus/antisense strand on chromosomes)",
		iga="Input gene annotations used in calculating the gene body TSS ratio. One may want to pre-filter the annotations to get a specific set of genes prior to running this command.",
		o="Output file",
		mode="Only accept heg or all. In heg mode, only the specified ratio of top highly expressed genes are used to calculate the ratio. In all mode, all genes are used to calculate the ratio.",
		gb_dc_tss_forward_len="Forward len of discarded part around TSS when obtaining the gene body region",
		gb_dc_tss_reverse_len="Reverse len of discarded part around TSS when obtaining the gene body region",
		gb_dc_tts_forward_len="Forward len of discarded part around TTS when obtaining the gene body region",
		gb_dc_tts_reverse_len="Reverse len of discarded part around TTS when obtaining the gene body region",
		tss_forward_len="Forward len of TSS region",
		tss_reverse_len="Reerse len of TSS region",
		heg_top_ratio="In heg mode, the specified ratio of top expressed genes used for calculating gene body TSS ratio",
		heg_tss_forward_len="Forward len of TSS region when considering the gene expression",
		heg_tss_reverse_len="Reverse len of TSS region when considering the gene expression",
	)
)
@vc
def _generate_genebody_TSS_ratio_table_20240501(
		label:list[str], ibwpl:list[str], ibwmn:list[str],
		iga:str,
		o:str,
		mode:str="heg", 
		gb_dc_tss_forward_len:int=500, gb_dc_tss_reverse_len:int=0, 
		gb_dc_tts_forward_len:int=1, gb_dc_tts_reverse_len:int=499,
		tss_forward_len:int=500, tss_reverse_len:int=0,
		heg_top_ratio:float=0.1,
		heg_tss_forward_len:int=1000, heg_tss_reverse_len:int=100,
		
	):
	import itertools
	from biodata.baseio import get_text_file_extension
	from biodata.bigwig import BigWigIReader
	from biodata.delimited import DelimitedWriter
	from biodata.gff import GFF3Reader, GTFReader
	import genomictools
	from genomictools import GenomicPos
	
	
	from .utils import geneannotation
	if not (len(label) == len(ibwpl) == len(ibwmn)):
		raise Exception()
	reader = GFF3Reader if get_text_file_extension(iga) == "gff3" else GTFReader
	gffs = reader.read_all(lambda gffs: [gff for gff in gffs if gff.feature == "transcript"], iga)

	ibwpl = [BigWigIReader(f) for f in ibwpl]
	ibwmn = [BigWigIReader(f) for f in ibwmn]
	with DelimitedWriter(o) as dw:
		dw.write(["Sample", "Gene body counts", "Gene body length", "TSS counts", "TSS length", "Gene body ratio"])		
		if mode == "all":
			gff_pls = list(filter(lambda gff: gff.strand == "+", gffs))
			gff_mns = list(filter(lambda gff: gff.strand == "-", gffs))
			gb_pl = list(genomictools.substract(
				genomictools.union(gff_pls),
				geneannotation._get_TSS_20240501(gff_pls, gb_dc_tss_forward_len, gb_dc_tss_reverse_len),
				geneannotation._get_TTS_20240501(gff_pls, gb_dc_tts_forward_len, gb_dc_tts_reverse_len), 
			))
			gb_mn = list(genomictools.substract(
				genomictools.union(gff_mns),
				geneannotation._get_TSS_20240501(gff_mns, gb_dc_tss_forward_len, gb_dc_tss_reverse_len),
				geneannotation._get_TTS_20240501(gff_mns, gb_dc_tts_forward_len, gb_dc_tts_reverse_len), 
			))
			tss_pl = list(genomictools.union(geneannotation._get_TSS_20240501(gff_pls, tss_forward_len, tss_reverse_len)))
			tss_mn = list(genomictools.union(geneannotation._get_TSS_20240501(gff_mns, tss_forward_len, tss_reverse_len)))
			
			gb_lengths = sum(map(lambda b: len(b.genomic_pos), itertools.chain(gb_pl, gb_mn)))
			tss_lengths = sum(map(lambda b: len(b.genomic_pos), itertools.chain(tss_pl, tss_mn)))
			for label, bwpl, bwmn in zip(label, ibwpl, ibwmn):
				tss_counts = sum(bwpl.value(r, method="abssum") for r in tss_pl) + sum(bwmn.value(r, method="abssum") for r in tss_mn)
				gb_counts = sum(bwpl.value(r, method="abssum") for r in gb_pl) + sum(bwmn.value(r, method="abssum") for r in gb_mn)
				if tss_lengths == 0 or tss_counts == 0 or gb_lengths == 0:
					dw.write([label, gb_counts, gb_lengths, tss_counts, tss_lengths, float("nan")])
				else:
					dw.write([label, gb_counts, gb_lengths, tss_counts, tss_lengths, (gb_counts / gb_lengths) / ((tss_counts / tss_lengths) + (gb_counts / gb_lengths))])
		elif mode == "heg":
			for label, bwpl, bwmn in zip(label, ibwpl, ibwmn):
				# Only select highly expressed genes
				gene_count_dict = geneannotation._generate_bigwig_values_by_attributes_20240501(
					gffs, "gene_id", bwpl, bwmn,
					region_func = lambda gff: GenomicPos(
						gff.genomic_pos.name, 
						(gff.genomic_pos.start - heg_tss_reverse_len) if gff.strand == "+" else (gff.genomic_pos.stop - (heg_tss_forward_len - 1)), 
						(gff.genomic_pos.start + (heg_tss_forward_len - 1)) if gff.strand == "+" else (gff.genomic_pos.stop + heg_tss_reverse_len)
					),
					value_method = "abssum",
					merge_method = "max"
				)
				selected_gene_ids = set(map(lambda x: x[0], sorted(gene_count_dict.items(), reverse=True, key=lambda x: x[1])[:int(heg_top_ratio * len(gene_count_dict))]))
				filtered_gffs = list(filter(lambda gff: gff.attribute["gene_id"] in selected_gene_ids, gffs))
				
				# Define the gene body and TSS regions
				gff_pls = list(filter(lambda gff: gff.strand == "+", filtered_gffs))
				gff_mns = list(filter(lambda gff: gff.strand == "-", filtered_gffs))
				gb_pl = list(genomictools.substract(
					genomictools.union(gff_pls),
					geneannotation._get_TSS_20240501(gff_pls, gb_dc_tss_forward_len, gb_dc_tss_reverse_len),
					geneannotation._get_TTS_20240501(gff_pls, gb_dc_tts_forward_len, gb_dc_tts_reverse_len), 
				))
				gb_mn = list(genomictools.substract(
					genomictools.union(gff_mns),
					geneannotation._get_TSS_20240501(gff_mns, gb_dc_tss_forward_len, gb_dc_tss_reverse_len),
					geneannotation._get_TTS_20240501(gff_mns, gb_dc_tts_forward_len, gb_dc_tts_reverse_len), 
				))
				tss_pl = list(genomictools.union(geneannotation._get_TSS_20240501(gff_pls, tss_forward_len, tss_reverse_len)))
				tss_mn = list(genomictools.union(geneannotation._get_TSS_20240501(gff_mns, tss_forward_len, tss_reverse_len)))
				
				gb_lengths = sum(map(lambda b: len(b.genomic_pos), itertools.chain(gb_pl, gb_mn)))
				tss_lengths = sum(map(lambda b: len(b.genomic_pos), itertools.chain(tss_pl, tss_mn)))
				
				# Generate counts and output ratio
				tss_counts = sum(bwpl.value(r, method="abssum") for r in tss_pl) + sum(bwmn.value(r, method="abssum") for r in tss_mn)
				gb_counts = sum(bwpl.value(r, method="abssum") for r in gb_pl) + sum(bwmn.value(r, method="abssum") for r in gb_mn)

				if tss_lengths == 0 or tss_counts == 0 or gb_lengths == 0:
					dw.write([label, gb_counts, gb_lengths, tss_counts, tss_lengths, float("nan")])
				else:
					dw.write([label, gb_counts, gb_lengths, tss_counts, tss_lengths, (gb_counts / gb_lengths) / ((tss_counts / tss_lengths) + (gb_counts / gb_lengths))])
			
		else:
			raise Exception("Unknown mode")
		

#
# Others
#
@vt(
	description="Process and merge bed overlapped regions. Two criteria, min overlap length and min overlap ratio are used to define overlap between two regions.",
	helps=dict(
		i="Input bed files",
		o="Output bed file",
		stranded="If *true*, regions from different strands are never merged.",
		min_overlap_len="Minimum overlap length in bp to connect two regions",
		min_overlap_ratio="Minimum overlap ratio (of the smaller region) to connect two regions",		
	)
)
@vc
def _process_bed_overlapped_regions_20240501(i:list[str], o:str, stranded:convert_to_bool=False, min_overlap_len:int=1, min_overlap_ratio:float=0):
	import itertools
	from genomictools import GenomicCollection
	from biodata.bed import BED3, BED3Reader, BED3Writer, BED, BEDReader, BEDWriter
	from .utils import genomic
	if stranded:
		regions = list(itertools.chain.from_iterable([BEDReader.read_all(list, f) for f in i]))
		pl_regions = [r for r in regions if r.strand == "+"]
		mn_regions = [r for r in regions if r.strand == "-"]
		merged_pl_regions = genomic._merge_overlapped_regions_20240501(pl_regions, min_overlap_len=min_overlap_len, min_overlap_ratio=min_overlap_ratio)
		merged_mn_regions = genomic._merge_overlapped_regions_20240501(mn_regions, min_overlap_len=min_overlap_len, min_overlap_ratio=min_overlap_ratio)
		pl_beds = [BED(r.name, r.zstart, r.ostop, strand=r.strand) for r in merged_pl_regions]
		mn_beds = [BED(r.name, r.zstart, r.ostop, strand=r.strand) for r in merged_mn_regions]
		BEDWriter.write_all(GenomicCollection(pl_beds + mn_beds), o)
	else:
		regions = list(itertools.chain.from_iterable([BED3Reader.read_all(list, f) for f in i]))
		merged_regions = genomic._merge_overlapped_regions_20240501(regions, min_overlap_len=min_overlap_len, min_overlap_ratio=min_overlap_ratio)
		beds = [BED3(r.name, r.zstart, r.ostop) for r in merged_regions]
		BED3Writer.write_all(GenomicCollection(beds), o)
		
		
@vt(
	description="Process and merge bed overlapped regions. Two criteria, min overlap length and min overlap ratio are used to define overlap between two regions.",
	helps=dict(
		i="Input bed files",
		o="Output bed file",
		stranded="If *true*, regions from different strands are never merged.",
		min_overlap_len="Minimum overlap length in bp to connect two regions",
		min_overlap_ratio="Minimum overlap ratio (of the smaller region) to connect two regions",
		mode="Strategy to merge overlapped regions. Available mode includes *union* and *best*",
		func="Function used in certain mode. In *best* mode, this corresponds to the scoring function for the region"
	)
)
@vc
def _process_bed_overlapped_regions_20240801(i:list[str], o:str, stranded:convert_to_bool=False, min_overlap_len:int=1, min_overlap_ratio:float=0, mode="union", func=None):
	import itertools
	from genomictools import GenomicCollection
	from biodata.bed import BED3, BED3Reader, BED3Writer, BED, BEDReader, BEDWriter
	from .utils import genomic
	if stranded:
		regions = list(itertools.chain.from_iterable([BEDReader.read_all(list, f) for f in i]))
		pl_regions = [r for r in regions if r.strand == "+"]
		mn_regions = [r for r in regions if r.strand == "-"]
		merged_pl_regions = genomic._merge_overlapped_regions_20240801(pl_regions, min_overlap_len=min_overlap_len, min_overlap_ratio=min_overlap_ratio, mode=mode, func=func)
		merged_mn_regions = genomic._merge_overlapped_regions_20240801(mn_regions, min_overlap_len=min_overlap_len, min_overlap_ratio=min_overlap_ratio, mode=mode, func=func)
		pl_beds = [BED(r.name, r.zstart, r.ostop, strand=r.strand) for r in merged_pl_regions]
		mn_beds = [BED(r.name, r.zstart, r.ostop, strand=r.strand) for r in merged_mn_regions]
		BEDWriter.write_all(GenomicCollection(pl_beds + mn_beds), o)
	else:
		regions = list(itertools.chain.from_iterable([BED3Reader.read_all(list, f) for f in i]))
		merged_regions = genomic._merge_overlapped_regions_20240801(regions, min_overlap_len=min_overlap_len, min_overlap_ratio=min_overlap_ratio, mode=mode, func=func)
		beds = [BED3(r.name, r.zstart, r.ostop) for r in merged_regions]
		BED3Writer.write_all(GenomicCollection(beds), o)
		
@vt(
	description="Filter bed entries. ",
	helps=dict(
		i="Input bed file",
		o="Output bed file",
		filter_func="Function to filter bed",
		overlap_regions="Regions indicated by bed files. A bed entry is kept only if it overlaps with any listed region.",
		non_overlap_regions="Regions indicated by bed files. A bed entry is kept only if it does not overlap with any listed region.",
		min_overlap_len="Minimum overlap length in bp to define two regions as overlap",
		min_overlap_ratio="Minimum overlap ratio (of the smaller region) to define two regions as overlap",				
	)
)
@vc
def _filter_bed_20240709(i:str, o:str, filter_func:str=None, overlap_regions:list[str]=[], non_overlap_regions:list[str]=[], stranded:convert_to_bool=False, min_overlap_len=1, min_overlap_ratio=0):
	from biodata.bed import BEDReader, BEDWriter
	from genomictools import GenomicCollection
	def _overlap(query, regions, stranded, min_overlap_len, min_overlap_ratio):
		r = query.genomic_pos
		hits = regions.find_overlaps(r)
		for hit in hits:
			if stranded and query.stranded_genomic_pos.strand != hit.stranded_genomic_pos.strand:
				continue
			tr = hit.genomic_pos
			overlap_len = min(r.stop, tr.stop) - max(r.start, tr.start) + 1
			if overlap_len >= min_overlap_len and overlap_len / min(len(r), len(tr)) >= min_overlap_ratio:
				return True
		return False

	overlap_regions = [BEDReader.read_all(GenomicCollection, s) for s in overlap_regions]
	non_overlap_regions = [BEDReader.read_all(GenomicCollection, s) for s in non_overlap_regions]
	if filter_func is not None and isinstance(filter_func, str):
		filter_func = eval(filter_func, {}) # While unsafe to use eval, disable access to global variables to make it a little bit safer..
	with BEDReader(i) as br, BEDWriter(o) as bw:
		for bed in br:
			if filter_func is not None and not filter_func(bed):
				continue
			if len(overlap_regions) > 0:
				if all(not _overlap(bed, regions, stranded, min_overlap_len, min_overlap_ratio) for regions in overlap_regions):
					continue
			if len(non_overlap_regions) > 0:
				if any(_overlap(bed, regions, stranded, min_overlap_len, min_overlap_ratio) for regions in non_overlap_regions):
					continue
			bw.write(bed)
			
@vt(
	description="Filter bed entries. ",
	helps=dict(
		i="Input bed file",
		o="Output bed file",
		bedx="Use BEDXReader instead of standard BEDReader with bedx indicating the number of basic field in bed format",
		fieldnames="Additional field names for bed",
		filter_func="Function to filter bed",
		overlap_regions="Regions indicated by bed files. A bed entry is kept only if it overlaps with any listed region.",
		non_overlap_regions="Regions indicated by bed files. A bed entry is kept only if it does not overlap with any listed region.",
		stranded="Whether strand is considered when defining two regions as overlap",
		min_overlap_len="Minimum overlap length in bp to define two regions as overlap",
		min_overlap_ratio="Minimum overlap ratio (of the smaller region) to define two regions as overlap",
	)
)
@vc
def _filter_bed_20240901(
		i:str, o:str, 
		bedx:int=None, fieldnames:list[str]=None, 
		filter_func:str=None, overlap_regions:list[str]=[], non_overlap_regions:list[str]=[], 
		stranded:convert_to_bool=False, min_overlap_len=1, min_overlap_ratio=0):
	from biodata.bed import BEDReader, BEDXReader, BEDWriter, BEDXWriter
	from genomictools import GenomicCollection
	def _overlap(query, regions, stranded, min_overlap_len, min_overlap_ratio):
		r = query.genomic_pos
		hits = regions.find_overlaps(r)
		for hit in hits:
			if stranded and query.stranded_genomic_pos.strand != hit.stranded_genomic_pos.strand:
				continue
			tr = hit.genomic_pos
			overlap_len = min(r.stop, tr.stop) - max(r.start, tr.start) + 1
			if overlap_len >= min_overlap_len and overlap_len / min(len(r), len(tr)) >= min_overlap_ratio:
				return True
		return False

	overlap_regions = [BEDReader.read_all(GenomicCollection, s) for s in overlap_regions]
	non_overlap_regions = [BEDReader.read_all(GenomicCollection, s) for s in non_overlap_regions]
	if filter_func is not None and isinstance(filter_func, str):
		filter_func = eval(filter_func, {}) # While unsafe to use eval, disable access to global variables to make it a little bit safer..
		
	if bedx is not None:
		reader = BEDXReader
		writer = BEDXWriter
		kwargs = {"fieldnames":fieldnames, "x":bedx}
	else:
		reader = BEDReader
		writer = BEDWriter
		kwargs = {}
	with reader(i, **kwargs) as br, writer(o) as bw:
		for bed in br:
			if filter_func is not None and not filter_func(bed):
				continue
			if len(overlap_regions) > 0:
				if all(not _overlap(bed, regions, stranded, min_overlap_len, min_overlap_ratio) for regions in overlap_regions):
					continue
			if len(non_overlap_regions) > 0:
				if any(_overlap(bed, regions, stranded, min_overlap_len, min_overlap_ratio) for regions in non_overlap_regions):
					continue
			bw.write(bed)

@vt(
	description="Modify fasta entries' names. This method is deprecated and replaced by a more general method `modify_fasta`", 
	helps=dict(i="Input fasta file", o="Output fasta file", func="Function to modify fasta name. Either a python function or a string to be evaluated as python lambda function. For example, to add a prefix, `lambda x: \"PREFIX_\" + x`")
)
@vc
def _modify_fasta_names_20240515(i:str, o:str, func:str):
	'''
	Extract all intervals that overlap with the selected regions
	'''
	from biodata.fasta import FASTAReader, FASTAWriter
	if isinstance(func, str):
		func = eval(func, {}) # While unsafe to use eval, disable access to global variables to make it a little bit safer..
	with FASTAReader(i) as fr, FASTAWriter(o) as fw:
		for f in fr:
			f.name = func(f.name)
			fw.write(f)
			
@vt(
	description="Modify fasta entries", 
	helps=dict(
		i="Input fasta file", 
		o="Output fasta file",
		name_func="Function to modify fasta name. Either a python function or a string to be evaluated as python lambda function. For example, to add a prefix, `lambda x: \"PREFIX_\" + x`",
		seq_func="Function to modify fasta sequence. Either a python function or a string to be evaluated as python lambda function"
		)
)
@vc
def _modify_fasta_20240801(i:str, o:str, name_func:str=None, seq_func:str=None):
	from biodata.fasta import FASTAReader, FASTAWriter
	from .utils.sequence import _reverse_complement_20200726
	if name_func is not None:
		if isinstance(name_func, str):
			name_func = eval(name_func, {}) # While unsafe to use eval, disable access to global variables to make it a little bit safer..
	if seq_func is not None:
		if isinstance(seq_func, str):
			if seq_func == "reverse-complement":
				seq_func = _reverse_complement_20200726
			else:
				seq_func = eval(seq_func, {}) # While unsafe to use eval, disable access to global variables to make it a little bit safer..
	
	with FASTAReader(i) as fr, FASTAWriter(o) as fw:
		for f in fr:
			if name_func is not None:
				f.name = name_func(f.name)
			if seq_func is not None:
				f.seq = seq_func(f.seq)
			fw.write(f)
		
@vt(
	description="Filter fasta entries",
	helps=dict(
		i="Input fasta file",
		o="Output fasta file",
		filter_func="Function to filter fasta",
		remove_duplicates_mode="Remove duplicated entries. Available modes include name, seq, seq_ignorecase, entry, entry_ignorecase"
	)
)
@vc
def _filter_fasta_20240801(i:str, o:str, filter_func:str=None, remove_duplicates_mode:str=None):		
	from biodata.fasta import FASTAReader, FASTAWriter
	from genomictools import GenomicCollection
	if filter_func is not None and isinstance(filter_func, str):
		filter_func = eval(filter_func, {}) # While unsafe to use eval, disable access to global variables to make it a little bit safer..
		
	entries = set()
	with FASTAReader(i) as fr, FASTAWriter(o) as fw:
		for f in fr:
			if filter_func is not None and not filter_func(f):
				continue
			if remove_duplicates_mode is not None:
				if remove_duplicates_mode == "name":
					e = f.name 
				elif remove_duplicates_mode == "seq":
					e = f.seq
				elif remove_duplicates_mode == "seq_ignorecase":
					e = f.seq.upper()
				elif remove_duplicates_mode == "entry":
					e = (f.name, f.seq)
				elif remove_duplicates_mode == "entry_ignorecase":
					e = (f.name, f.seq.upper())
				else:
					raise Exception()
				if e in entries:
					continue
				entries.add(e)
			fw.write(f)
			
@vt(
	description="Extract names from a fasta file to a text file",
	helps=dict(
		i="Input fasta file",
		o="Output text file",
	)
)
@vc
def _extract_fasta_names_20240801(i:str, o:str):
	from biodata.delimited import DelimitedWriter
	from biodata.fasta import FASTAReader			
	with FASTAReader(i) as fr, DelimitedWriter(o) as dw:
		for f in fr:
			dw.write([f.name])	
@vt(
	description="Create a chrom size file from fasta", 
	helps=dict(i="Input fasta file", o="Output chrom size file")
)			
@vc
def _generate_chrom_size_20240501(i:str, o:str):
	from biodata.delimited import DelimitedWriter
	from biodata.fasta import FASTAReader
	with FASTAReader(i) as fr, DelimitedWriter(o) as dw:
		for f in fr:
			dw.write([f.name, len(f.seq)])
	
			
@vt(description="Modify bigwig values according to the func", 
	helps=dict(
		i="Input bigwig file",
		o="Output bigwig file", 
		func="Function to modify bigwig. Either a python function or a string to be evaluated as python lambda function. For example, to convert all positive values into negative values, `lambda x: x * -1`")
	)
@vc
def _modify_bigwig_values_20240423(i:str, o:str, func:str):
	'''
	'''
	import pyBigWig
	from commonhelper import safe_inverse_zip

	if isinstance(func, str):
		func = eval(func, {}) # While unsafe to use eval, disable access to global variables to make it a little bit safer..
	input_bw = pyBigWig.open(i)
	def _get_pyBigWig_all_interval_generator(bw):
		for chrom in bw.chroms():
			if bw.intervals(chrom) is not None:
				for interval in bw.intervals(chrom):
					yield (chrom, *interval)
	output_bw = pyBigWig.open(o, "w")
	output_bw.addHeader(list(input_bw.chroms().items()))
	all_intervals = list(_get_pyBigWig_all_interval_generator(input_bw))
	chroms, starts, ends, values = safe_inverse_zip(all_intervals, 4)
	values = list(map(func, values))
	output_bw.addEntries(list(chroms), list(starts), ends=list(ends), values=list(values))
	output_bw.close()
	input_bw.close()

@vt(
	description="Filter bigwig entries by chromosomes",
	helps=dict(
		i="Input bigwig file",
		o="Output bigwig file",
		chroms="Seleted chromosomes retained in the output"
	) 
)
@vc
def _filter_bigwig_by_chroms_20240501(i:str, o:str, chroms:list[str]):
	import pyBigWig
	from commonhelper import safe_inverse_zip

	input_bw = pyBigWig.open(i)
	output_bw = pyBigWig.open(o, "w")
	output_bw.addHeader(list(input_bw.chroms().items()))
	all_intervals = []
	for chrom in input_bw.chroms():
		if chrom in chroms and input_bw.intervals(chrom) is not None:
			for interval in input_bw.intervals(chrom):
				all_intervals.append([chrom, *interval])

	chroms, starts, ends, values = safe_inverse_zip(all_intervals, 4)
	output_bw.addEntries(list(chroms), list(starts), ends=list(ends), values=list(values))
	output_bw.close()
	input_bw.close()
@vt(
	description="Merge multiple bigwig files into one file. If the bigWig file contains negative data values, threshold must be properly set. An option remove_zero is added to remove entries with zero values.",
	helps=dict(
		i="Input bigwig files", g="chrom size file", o="output bigwig file",
		threshold="Threshold. Set to a very negative value, e.g. -2147483648, if your bigwig contains negative values.",
		adjust="Adjust",
		clip="Clip",
		max="Max",
		autosort="Perform sorting on bedgraph file before running bedGraphToBigWig. Set to *false* if you are sure that your input files are sorted to reduce running time.",
		filter_chr="Remove chromosomes in bedgraph file that are not present in chrom.sizes file", 
		nthread="Number of threads used in sorting"
	)
)
@vc
def _merge_bigwig_20240501(i:list[str], g:str, o:str, 
									threshold:float=None, adjust:float=None, clip:float=None, max:convert_to_bool=False, remove_zero:convert_to_bool=False,
									autosort=True, filter_chr=False, nthread=1):
	import os
	import tempfile
	
	check_binaries_validity("bigWigMerge", "sort", "bedGraphToBigWig")
	if len(i) <= 1:
		raise Exception("At least two input bigwig files are required for merging")
	bigWigMerge_cmd = "bigWigMerge"
	if threshold is not None:
		bigWigMerge_cmd += f" -threshold={threshold}"
	if adjust is not None:
		bigWigMerge_cmd += f" -adjust={adjust}"
	if clip is not None:
		bigWigMerge_cmd += f" -clip={clip}"
	if max:
		bigWigMerge_cmd += " -max"
	
	bw_files = " ".join(i)
	
	tmpfile_bgo = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
	if remove_zero:
		tmpfile = tempfile.NamedTemporaryFile(mode='w+', suffix=".bg", delete=False).name
		bash_command(f"{bigWigMerge_cmd} {bw_files} {tmpfile}")
		bash_command("awk '{ if ($4 != 0) print $0 }' " + tmpfile + " > " + tmpfile_bgo)
		os.unlink(tmpfile)
	else:
		bash_command(f"{bigWigMerge_cmd} {bw_files} {tmpfile_bgo}")
	_convert_bedgraph_to_bigwig_20240501(tmpfile_bgo, g, o, autosort, filter_chr, nthread)
	os.unlink(tmpfile_bgo)
	
@vt(
	description="Subsample multiple bigwig files into target values. For example, if bwpl contains 100 counts and bwmn contains 200 counts, and n = 50, then sum of read counts in output_bwpl and output_mn will be 50 but the ratio of read counts is not kept at 1:2. This function assumes int value in bigwig value. This function supports positive / negative read counts.", 
	helps=dict(
		ibws="Input bigwig files",
		obws="Output bigwig files",
		n="Target number to subsample",
		seed="Random seed used in subsampling",
		)
)
@vc	
def _subsample_bigwig_20240501(ibws : list[str], obws : list[str], n : int, seed : int):
	from collections import Counter
	import random
	import pyBigWig
	def intervals_generator(bw):
		for chrom in bw.chroms():
		# This condition avoids problems if a chromosome info is included but the region is not
			if bw.intervals(chrom) is not None:
				for interval in bw.intervals(chrom):
					yield (chrom, *interval)

	random.seed(seed)
	
	ibws = [pyBigWig.open(bw) if isinstance(bw, str) else bw for bw in ibws]
	
	sorted_dicts = {}
	for idx, bw in enumerate(ibws):
		sorted_dicts[idx] = {k:i for i, k in enumerate(bw.chroms().keys())}
		
	all_locs = []
	all_abscounts = []
	all_counts = []
	for idx, bw in enumerate(ibws):
		loc, counts = list(zip(*[((idx, i[0], p + 1, i[3]>=0), i[3]) for i in intervals_generator(bw) for p in range(i[1], i[2])]))
		abscounts = list(map(lambda c: abs(int(c)), counts))
		all_locs.extend(loc)
		all_abscounts.extend(abscounts)
		all_counts.extend(counts)
	
	downsampled_rc = Counter(random.sample(all_locs, counts=all_abscounts, k=n))
	keys = sorted(downsampled_rc.keys(), key=lambda k: (k[0], sorted_dicts[k[0]][k[1]], k[2]))

	chroms = [[] for _ in range(len(ibws))]
	starts = [[] for _ in range(len(ibws))]
	ends = [[] for _ in range(len(ibws))]
	values = [[] for _ in range(len(ibws))]
	for k in keys:
		idx, chrname, p, is_positive = k
		cnt = downsampled_rc[k]
		chroms[idx].append(chrname)
		starts[idx].append(p - 1)
		ends[idx].append(p)
		values[idx].append(cnt * (1.0 if is_positive else -1.0))

	for idx, (ibw, obw_file) in enumerate(zip(ibws, obws)):
		obw = pyBigWig.open(obw_file, "w")
		obw.addHeader(list(ibw.chroms().items()))
		obw.addEntries(chroms[idx], starts[idx], ends[idx], values[idx])
		obw.close()	

@vt(
	description="Normalize bigwig files. ",
	helps=dict(
		ibws="Input bigwig files",
		obws="Output bigwig files",
		mode="Mode to normalize bigwig files. Only rpm is supported now.",
		nthread="Number of threads used to create normalized bigwig files."
	)
)
@vc
def _normalize_bigwig_20240501(ibws:list[str], obws:list[str], mode:str="rpm", nthread:int=-1): 
	import pyBigWig
	from mphelper import ProcessWrapPool, ProcessWrapState
	if len(ibws) != len(obws):
		raise Exception()
	if len(ibws) == 0:
		raise Exception()
	total = 0
	for ibw in ibws:
		with pyBigWig.open(ibw) as bw:
			total += abs(bw.header()["sumData"])
	if nthread == -1:
		nthread = len(ibws)
	pool = ProcessWrapPool(nthread)
	for ibw, obw in zip(ibws, obws):
		if mode == "rpm":
			pool.run(_modify_bigwig_values_20240423, kwargs={"i":ibw, "o":obw, "func":f"lambda i: i/{total}*1000000"})
		else:
			raise Exception()
	pool.get(wait=True)
	pool.close()
	for f in pool.futures.values():
		if f.state != ProcessWrapState.COMPLETE:
			raise Exception()
	
			
@vt(
	description="Subsample a bam file into exact number of entries. Alignments of n total reads (including unmapped reads) will be retrieved.", 
	helps=dict(
		i="Input bam file",
		o="Output bam file",
		n="Target number to subsample",
		seed="Random seed used in subsampling",
		nthread="Number of threads for compression"
	)
)
@vc
def _subsample_bam_20240501(i : str, o : str, n : int, seed : int, nthread : int = 1):
	import random
	import pysam
	
	ibam = pysam.AlignmentFile(i, "rb")
	all_read_names = sorted(set(read.qname for read in ibam.fetch(until_eof=True)))
	ibam.close()
	random.seed(seed)
	random.shuffle(all_read_names)
	if len(all_read_names) < n:
		raise Exception(f"Cannot subsample {n} reads from {len(all_read_names)} total reads.")
	selected = set(all_read_names[:n])
	ibam = pysam.AlignmentFile(i, "rb")
	obam = pysam.AlignmentFile(o, "wb", template=ibam, threads=nthread)
	for read in ibam.fetch(until_eof=True):
		if read.qname in selected:
			obam.write(read)
	obam.close()
	ibam.close()
@vt(
	description="Remove reads with any alignment that contain N in the CIGAR string. ",
	helps=dict(
		i="Input bam file",
		o="Output bam file",
		nthread="Number of threads used in compression"
	)
)
@vc
def _filter_bam_NCIGAR_reads_20240501(i : str, o : str, nthread : int = 1):
	import random
	import pysam
	ibam = pysam.AlignmentFile(i, "rb")
	to_remove = set(read.qname for read in ibam.fetch(until_eof=True) if 'N' in read.cigarstring)
	ibam.close()
	ibam = pysam.AlignmentFile(i, "rb")
	obam = pysam.AlignmentFile(o, "wb", template=ibam, threads=nthread)
	for read in ibam.fetch(until_eof=True):
		if read.qname not in to_remove:
			obam.write(read)
	obam.close()
	ibam.close()


@vt(
	description="Process bigwig into count table, either in a specific set of regions, or genomewide bins", 
	helps=dict(
		sample_names="Input sample names",
		i="Input bigwig files",
		o="Output count table file",
		region_file="A bed file containing regions to calculate bigwig counts",
		bin_size="If regions not provided, generate genomewide counts binned in bin_size",
		g="chrom size file. If provided, only use the selected chromosomes for genomewide counts",
	)
)
@vc
def _process_bigwigs_to_count_table_20240501(
		sample_names:list[str], i:list[str], o:str, 
		region_file:str=None, bin_size:int=None, g:str=None):
	from collections import defaultdict
	from biodata.bed import BED3Reader
	from biodata.bigwig import BigWigIReader
	from biodata.delimited import DelimitedReader, DelimitedWriter
	from genomictools import GenomicCollection
		
	def intervals_generator(bw, chroms=None):
		if chroms is None:
			chroms = bw.chroms()
		for chrom in chroms:
			if bw.intervals(chrom) is not None:
				for interval in bw.intervals(chrom):
					yield (chrom, *interval)
	if len(sample_names) != len(i):
		raise Exception("Number of sample names do not match number of bigwig files")				
	bws = [BigWigIReader(f) for f in i]
	if region_file is not None:
		regions = BED3Reader.read_all(GenomicCollection, region_file)
		with DelimitedWriter(o) as dw:
			dw.write([""] + sample_names)
			for r in regions:
				dw.write([str(r)] + [bw.value(r, "sum") for bw in bws])
	elif bin_size is not None:
		if g is None:
			chroms = None
		else:
			chroms = DelimitedReader.read_all(lambda ds: [d[0] for d in ds], g)
		covs = []
		for bw in bws:
			cov = defaultdict(int)
			for chrom, zstart, ostop, score in intervals_generator(bw.bw, chroms):
				for idx in range(zstart // bin_size, (ostop - 1) // bin_size + 1):
					l = min((idx + 1) * bin_size, ostop) - max(idx * bin_size, zstart)
					cov[chrom, idx] += l * score
			covs.append(cov)
		union_keys = sorted(set.union(*[set(cov.keys()) for cov in covs]))
		with DelimitedWriter(o) as dw:
			dw.write([""] + sample_names)
			for k in union_keys:
				dw.write([f"{k[0]}:{k[1]*bin_size+1}-{(k[1]+1)*bin_size}"] + [cov[k] if k in cov else 0 for cov in covs])
	else:
		raise Exception()		
@vt(
	description="Process bigwig into count table, either in a specific set of regions, or genomewide bins", 
	helps=dict(
		sample_names="Input sample names",
		i="Input bigwig files",
		o="Output count table file",
		region_file="A bed file containing regions to calculate bigwig counts",
		bin_size="If regions not provided, generate genomewide counts binned in bin_size",
		g="chrom size file. If provided, only use the selected chromosomes for genomewide counts",
	)
)
@vc
def _process_bigwigs_to_count_table_20240601(
		sample_names:list[str], i:list[str], o:str, 
		region_file:str=None, bin_size:int=None, g:str=None):
	from collections import defaultdict
	from biodata.bed import BED3Reader
	from biodata.bigwig import BigWigIReader
	from biodata.delimited import DelimitedReader, DelimitedWriter
	from genomictools import GenomicCollection
		
	def intervals_generator(bw, chroms=None):
		if chroms is None:
			chroms = bw.chroms()
		for chrom in chroms:
			if chrom not in bw.chroms():
				continue
			if bw.intervals(chrom) is not None:
				for interval in bw.intervals(chrom):
					yield (chrom, *interval)
	if len(sample_names) != len(i):
		raise Exception("Number of sample names do not match number of bigwig files")				
	bws = [BigWigIReader(f) for f in i]
	if region_file is not None:
		regions = BED3Reader.read_all(GenomicCollection, region_file)
		with DelimitedWriter(o) as dw:
			dw.write([""] + sample_names)
			for r in regions:
				dw.write([str(r.genomic_pos)] + [bw.value(r, "sum") for bw in bws])
	elif bin_size is not None:
		if g is None:
			chroms = None
		else:
			chroms = DelimitedReader.read_all(lambda ds: [d[0] for d in ds], g)
		covs = []
		for bw in bws:
			cov = defaultdict(int)
			for chrom, zstart, ostop, score in intervals_generator(bw.bw, chroms):
				for idx in range(zstart // bin_size, (ostop - 1) // bin_size + 1):
					l = min((idx + 1) * bin_size, ostop) - max(idx * bin_size, zstart)
					cov[chrom, idx] += l * score
			covs.append(cov)
		union_keys = sorted(set.union(*[set(cov.keys()) for cov in covs]))
		with DelimitedWriter(o) as dw:
			dw.write([""] + sample_names)
			for k in union_keys:
				dw.write([f"{k[0]}:{k[1]*bin_size+1}-{(k[1]+1)*bin_size}"] + [cov[k] if k in cov else 0 for cov in covs])
	else:
		raise Exception()		
@vt(
	description="Process count tables into a correlation table. Currently Pearson correlation is used.",
	helps=dict(
		i="Input files",
		o="Output file",
		filter_func="A function that takes in a pair of sample 1 and sample 2 count values to see if this pair should be retained or discarded",
		value_func="A function that modifies count values",
		keys="Only the selected samples are used to generate the correlation table"
	)
)
@vc
def _process_count_tables_to_correlation_table_20240501(i:list[str], o:str, filter_func=None, value_func=None, keys=None):
	import itertools
	from commonhelper import safe_inverse_zip
	from biodata.delimited import DelimitedReader, DelimitedWriter
	import math
	import numpy as np
	import scipy.stats
	tables = None
	for f in i:
		with DelimitedReader(f) as dr:
			header = dr.read()[1:]
			if keys is None:
				keys = header
			tmp_tables = safe_inverse_zip([list(map(float, d[1:])) for d in dr], len(keys))
			indice = [header.index(k) for k in keys]
			tmp_tables = [tmp_tables[idx] for idx in indice]
			if tables is None:
				tables = [list(t) for t in tmp_tables]
			else:
				for idx in range(len(keys)):
					tables[idx].extend(tmp_tables[idx])
	
	if filter_func is not None:
		filter_func = eval(filter_func, {})
	if value_func is not None:
		value_func = eval(value_func, {"math":math})
	with DelimitedWriter(o) as dw:
		dw.write(["Sample-1", "Sample-2", "Correlation"])
		for s1, s2 in itertools.combinations(range(len(keys)), 2):
			s1_values = []
			s2_values = []
			for a, b in zip(tables[s1], tables[s2]):
				if filter_func is None or filter_func(a, b):
					s1_values.append(a if value_func is None else value_func(a))
					s2_values.append(b if value_func is None else value_func(b))
			dw.write([keys[s1], keys[s2], scipy.stats.pearsonr(s1_values, s2_values)[0]])
			
			
#
# Gene annotation related tools
#
@vt(
	description="Generate a union TSS +x -y bp region for classifying distal / proximal regions.",
	helps=dict(
		i="Input gff file",
		o="Output file",
		forward_len="Length to extend in the forward strand. Use 1 if only TSS is chosen. For TSS-500bp to TSS+250bp, the region is 750bp long and forward_len should be set to 250.",
		reverse_len="Length to extend in the reverse strand. For TSS-500bp to TSS+250bp, the region is 750bp long and reverse_len should be set to 500.",
		filter_func="Function to filter the transcripts"
		)
)
@vc	
def _generate_union_TSS_20240501(
		i:str, o:str, forward_len:int, reverse_len:int, filter_func:str=None):
	from biodata.baseio import get_text_file_extension
	from biodata.bed import BED3Writer
	from biodata.gff import GFF3Reader, GTFReader
	import genomictools
	from genomictools import GenomicCollection
	from .utils import geneannotation
	
	if get_text_file_extension(i) == "gff3":
		gr = GFF3Reader(i)
	else:
		gr = GTFReader(i)
	if isinstance(filter_func, str):
		filter_func = eval(filter_func, {})
	regions = GenomicCollection(genomictools.union(geneannotation._get_TSS_20240501(gr, forward_len, reverse_len, filter_func=filter_func)))
	gr.close()	
	BED3Writer.write_all(regions, o)
	
@vt(
	description="Deprecated - replaced with a more general method generate_geneannotations_union_features. Generate union transcripts regions. ",
	helps=dict(
		i="Input gff file",
		o="Output file",
		filter_func="Function to filter the transcripts"
		)
	)
@vc	
def _generate_union_transcripts_20240501(
		i:str, o:str, filter_func:str=None):
	from biodata.baseio import get_text_file_extension
	from biodata.bed import BED3Writer
	from biodata.gff import GFF3Reader, GTFReader
	import genomictools
	from genomictools import GenomicCollection
	from .utils import geneannotation
	if get_text_file_extension(i) == "gff3":
		gr = GFF3Reader(i)
	else:
		gr = GTFReader(i)
	if isinstance(filter_func, str):
		filter_func = eval(filter_func, {})
	regions = GenomicCollection(genomictools.union(geneannotation._get_transcripts_20240501(gr, filter_func=filter_func)))
	gr.close()	
	BED3Writer.write_all(regions, o)
@vt(
	description="Generate union feature regions.",
	helps=dict(
		i="Input genome annotation file",
		o="Output genome annotation file",
		feature="Feature to be selected to generate the union regions",
		filter_func="Function to filter the feature"
	)
)
@vc
def _generate_geneannotations_union_features_20240901(
		i:str, o:str, feature:str, filter_func:str=None):
	from biodata.baseio import get_text_file_extension
	from biodata.bed import BED3Writer
	from biodata.gff import GFF3Reader, GTFReader
	import genomictools
	from genomictools import GenomicCollection
	from .utils import geneannotation
	if get_text_file_extension(i) == "gff3":
		gr = GFF3Reader(i)
	else:
		gr = GTFReader(i)
	if isinstance(filter_func, str):
		filter_func = eval(filter_func, {})
	regions = GenomicCollection(genomictools.union(geneannotation._get_features_20240901(gr, feature, filter_func=filter_func)))
	gr.close()	
	BED3Writer.write_all(regions, o)

@vt(
	description="Filter genome annotations",
	helps=dict(
		i="Input genome annotation file",
		o="Output genome annotation file",
		filter_func="Function to filter genome annotations",
		remove_overlapping_genes="Remove overlapping genes",
		overlapping_genes_extension="Expand the genes before finding overlapping genes for removal"
	)
)
@vc
def _filter_geneannotations_20240501(
		i:str, o:str, 
		filter_func:str=None,
		remove_overlapping_genes:convert_to_bool=False,
		overlapping_genes_extension:int=0
	):
	from biodata.baseio import get_text_file_extension
	from biodata.bed import BED3Writer
	from biodata.gff import GFF3Reader, GTFReader, GFF3Writer, GTFWriter
	from .utils import geneannotation
	
	if get_text_file_extension(i) == "gff3":
		gr = GFF3Reader(i)
	else:
		gr = GTFReader(i)
	if get_text_file_extension(o) == "gff3":
		gw = GFF3Writer(o)
	else:
		gw = GTFWriter(o)
	if isinstance(filter_func, str):
		filter_func = eval(filter_func, {})
	if remove_overlapping_genes:
		gffs = list(gr)
		gffs = geneannotation._filter_out_overlapping_genes_20240501(gffs, overlapping_genes_extension)
	else: 
		gffs = gr
	for gff in gffs:
		if filter_func is None or filter_func(gff):
			gw.write(gff)
	gr.close()
	gw.close()
	
@vt(
	description="""Check sequencing files organized in a particular layout.
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
""",
	helps=dict(
		i="Input folder"
	)
)
@vc
def _check_sequencing_files_md5_20240501(i):
	import os
	import glob
	import subprocess
	from biodata.baseio import BaseReader
	
	check_binaries_validity("md5sum")
	
	print(f"Checking {i}")
	nd = 0
	n = 0
	m = 0
	for d in glob.glob(f"{i}/**/"):
		if not os.path.exists(f"{d}MD5.txt"):
			continue
		nd += 1
		with BaseReader(f"{d}MD5.txt") as br:
			for b in br:
				md5, fname = b.split()
				try:
					n += 1
					if not os.path.exists(f"{d}{fname}"):
						print(f"Warning! File does not exist: {d}{fname}")
						continue
					cal_md5 = subprocess.check_output(f"md5sum {d}{fname}", shell=True).decode().split()[0]
					if cal_md5 != md5:
						print(f"Warning! Data in {d}{fname} has error.")
						continue
					m += 1
				except:
					print(f"Warning! Error when running md5sum in {d}{fname}")
	print(f"MD5 check is done in {nd} directories.")
	print(f"Correct files: {m}/{n}")
	
	
	
@vt(
	description='''
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
''',
	helps=dict(
		i="Input json file",
		o="Output file",
		proximal_regions="A BED file that indicates proximal regions",
		transcripts_regions="A BED file that indicates all transcripts regions",
		spikein_chrom_sizes="chrom size file for spike-in chromosomes. Required only if `Spike-in read pairs` is reported",
		nthread="Number of threads"
	)
)
@vc	
def _generate_PROcap_stat_table_20240601(
		i:str,
		o:str,
		proximal_regions:str=None,
		transcripts_regions:str=None, 
		spikein_chrom_sizes:str=None,
		nthread:int=1, 
		
	):
	
	import itertools
	import pandas as pd
	import numpy as np
	import pyBigWig

	from commonhelper import safe_inverse_zip, sort_multiple_ordered_lists
	from mphelper import ProcessWrapPool
	from biodata.bed import BED3Reader
	from biodata.delimited import DelimitedReader, DelimitedWriter
	from genomictools import GenomicCollection
	from .utils.common import _json_load_20240601
	def _extract_non_overlaps_generator(query_regions, ref_regions):
		for r in query_regions:
			if not ref_regions.overlaps(r):
				yield r

	def _fastqc_simple_stat_dict(files):
		import io
		import os
		import zipfile
		from biodata.baseio import BaseReader
		stats = {}
		for f in files:
			with zipfile.ZipFile(f) as z:
				name = os.path.basename(os.path.splitext(f)[0])
				fastqc_data_file = f"{name}/fastqc_data.txt"
				if fastqc_data_file not in z.namelist():
					search_results = [i for i in z.namelist() if i.endswith("fastqc_data.txt")]
					if len(search_results) != 1:
						raise Exception("Cannot find unqiue fastqc_data.txt")
					fastqc_data_file = search_results[0]

				with BaseReader(io.TextIOWrapper(z.open(fastqc_data_file))) as br:
					for s in br:
						if s.startswith("Total Sequences"):
							total_seqs = int(s.split("\t")[1])
				stats[name] = total_seqs
		return stats
	def _get_bam_reads(f, *chrsets):
		import subprocess
		import io
		import os
		from biodata.delimited import DelimitedReader
		if len(chrsets) == 0:
			print("Warning! You should provide some chromosomes, or use '*' for all")
		if not os.path.exists(f):
			raise Exception("File not found.")
		if f.endswith(".bam"):
			s = subprocess.getoutput(f"samtools coverage {f}")
			i = io.StringIO(s)
		else:
			i = f
		with DelimitedReader(i, header=True, skip_header_comment_symbol="#") as dr:
			sums = [0 for _ in range(len(chrsets))]
			for d in dr:
				for e, chrs in enumerate(chrsets):
					if chrs == "*" or d['rname'] in chrs:
						sums[e] += int(d['numreads'])
		return sums
	def fastqc_get_raw_reads(vs):	
		return sum(_fastqc_simple_stat_dict(vs).values())
	def bam_get_reads(vs, *chrsets):
		return sum([int(sum(_get_bam_reads(v, *chrsets))) for v in vs])
	def bam_get_read_pairs(vs, *chrsets):
		return sum([int(sum(_get_bam_reads(v, *chrsets))) // 2 for v in vs])
	def bw_get_reads(vs):
		total = 0
		for v in vs:
			with pyBigWig.open(v) as f:
				total += abs(f.header()['sumData'])
		return total
	def median_read_len(v):
		from biodata.delimited import DelimitedReader
		with DelimitedReader(v) as dr:
			rnalen_dict = {d[0]:d[1] for d in dr}
		return rnalen_dict["median"]
	def gb_ratio(v):
		from biodata.delimited import DelimitedReader
		with DelimitedReader(v,header=True) as dr:
			f = dr.read()["Gene body ratio"]
			return float(f)
	def replicates_correlation(v):
		from biodata.delimited import DelimitedReader
		with DelimitedReader(v,header=True) as dr:
			return ";".join([f'{float(d["Correlation"]):.3f}' for d in dr])

	
	def element_get_stat(k, v, proximal_regions, transcripts_regions):
		# Output: List 
		# No proximal region supplied:
		# One number: total
		# Proximal region supplied:
		# Three numbers: total, proximal, distal
		# Proximal region + transcript region supplied:
		# Four numbers: total, proximal, distal intragenic, distal intergenic
		peaks = BED3Reader.read_all(GenomicCollection, v)
		output_stat_list = []
		
		n_peak = len(peaks)
		output_stat_list.append(n_peak)
		
		if proximal_regions is not None:
			distal_peaks = list(_extract_non_overlaps_generator(peaks, proximal_regions))
			n_peak_proximal = n_peak - len(distal_peaks)
			output_stat_list.append(n_peak_proximal)
			
			n_peak_distal = len(distal_peaks)
			if transcripts_regions is not None:
				n_peak_distal_intragenic = len(list(_extract_non_overlaps_generator(distal_peaks, transcripts_regions)))
				n_peak_distal_intergenic = n_peak_distal - n_peak_distal_intragenic
				output_stat_list.append(n_peak_distal_intragenic)
				output_stat_list.append(n_peak_distal_intergenic)
			else:
				output_stat_list.append(n_peak_distal)
		return output_stat_list
	
	if isinstance(i, str):
		data = _json_load_20240601(i)
	else:
		data = i
	if proximal_regions is not None:
		proximal_regions = BED3Reader.read_all(GenomicCollection, proximal_regions)
	if transcripts_regions is not None:
		transcripts_regions = BED3Reader.read_all(GenomicCollection, transcripts_regions)
	if spikein_chrom_sizes is not None:
		spikein_chroms = DelimitedReader.read_all(lambda ds: [d[0] for d in ds], spikein_chrom_sizes)
	
	pool = ProcessWrapPool(nthread)
	final_results = {}
	for keyname, fr in enumerate(data):
		results = {}
		for k, v in fr.items():
			if k == "Raw read pairs":
				if isinstance(v, str):
					v = [v]
				results[k] = pool.run(fastqc_get_raw_reads, args=[v])
			elif k == "Trimmed read pairs":
				if isinstance(v, str):
					v = [v]
				results[k] = pool.run(fastqc_get_raw_reads, args=[v])
			elif k == "Uniquely mapped read pairs":
				if isinstance(v, str):
					v = [v]
				results[k] = pool.run(bam_get_read_pairs, args=[v, "*"])
			elif k == "Deduplicated read pairs":
				if isinstance(v, str):
					v = [v]
				results[k] = pool.run(bam_get_read_pairs, args=[v, "*"])
			elif k == "Spike-in read pairs":
				if isinstance(v, str):
					v = [v]
				results[k] = pool.run(bam_get_read_pairs, args=[v, spikein_chroms])
			elif k == "Sense read pairs":
				if isinstance(v, str):
					v = [v]
				results[k] = pool.run(bw_get_reads, args=[v])
			elif k == "Antisense read pairs":
				if isinstance(v, str):
					v = [v]
				results[k] = pool.run(bw_get_reads, args=[v])
			elif k == "Median RNA length":
				results[k] = pool.run(median_read_len, args=[v])
			elif k == "Gene body ratio":
				results[k] = pool.run(gb_ratio, args=[v])
			elif k == "Replicates correlation":
				results[k] = pool.run(replicates_correlation, args=[v])
			elif k.endswith("elements"):
				# The suffix should be either Bidirectional Elements; Divergent Elements; Unidirectional Elements
				results[k] = pool.run(element_get_stat, args=[k, v, proximal_regions, transcripts_regions])
			else:
				results[k] = pool.run(str, args=[v])
		final_results[keyname] = results
	keys = sort_multiple_ordered_lists([list(results.keys()) for results in final_results.values()])
	# Fix the keys for elements
	fixed_keys = []
	mapped_fixed_keys = {}
	for k in keys:
		if k.endswith("elements"):
			fixed_keys.append(k)
			if proximal_regions is not None:
				fixed = []
				fixed.append(k + " - Proximal")
				if transcripts_regions is not None:
					fixed.append(k + " - Distal Intragenic")
					fixed.append(k + " - Distal Intergenic")
				else:
					fixed.append(k + " - Distal")
				
				mapped_fixed_keys[k] = fixed
				fixed_keys.extend(fixed)
			else:
				mapped_fixed_keys[k] = []
		else:
			fixed_keys.append(k)
	
	pool_results = pool.get(wait=True)
	pool.close()
	extracted_results = []
	for results in final_results.values():
		extracted_result = []
		for k in keys:
			if k in results:
				return_value = pool_results[results[k]]
				if k in mapped_fixed_keys:
					for rv in return_value:
						extracted_result.append(rv)
				else:
					extracted_result.append(return_value)
			elif k in mapped_fixed_keys:
				extracted_result.extend([None] * len(mapped_fixed_keys[k]))
			else:
				extracted_result.append(None)
		extracted_results.append(extracted_result)
	
	with DelimitedWriter(o) as dw:
		dw.write(fixed_keys)
		for row in extracted_results:
			dw.write(row)
	
@vt(
	description='''
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
''',
	helps=dict(
		i="Input json file",
		o="Output file",
		proximal_regions="A BED file that indicates proximal regions",
		transcripts_regions="A BED file that indicates all transcripts regions",
		spikein_chrom_sizes="chrom size file for spike-in chromosomes. Required only if `Spike-in read pairs` is reported",
		nthread="Number of threads"
	)
)
@vc	
def _generate_PROcap_stat_table_20240623(
		i:str,
		o:str,
		proximal_regions:str=None,
		transcripts_regions:str=None, 
		spikein_chrom_sizes:str=None,
		nthread:int=1, 
		
	):
	import itertools
	import pandas as pd
	import numpy as np
	import pyBigWig

	from commonhelper import safe_inverse_zip, sort_multiple_ordered_lists
	from mphelper import ProcessWrapPool
	from biodata.bed import BED3Reader
	from biodata.delimited import DelimitedReader, DelimitedWriter
	from genomictools import GenomicCollection
	from .utils.common import _json_load_20240601
	def _extract_non_overlaps_generator(query_regions, ref_regions):
		for r in query_regions:
			if not ref_regions.overlaps(r):
				yield r
	def _fastqc_simple_stat_dict(files):
		import io
		import os
		import zipfile
		from biodata.baseio import BaseReader
		stats = {}
		for f in files:
			with zipfile.ZipFile(f) as z:
				name = os.path.basename(os.path.splitext(f)[0])
				fastqc_data_file = f"{name}/fastqc_data.txt"
				if fastqc_data_file not in z.namelist():
					search_results = [i for i in z.namelist() if i.endswith("fastqc_data.txt")]
					if len(search_results) != 1:
						raise Exception("Cannot find unqiue fastqc_data.txt")
					fastqc_data_file = search_results[0]

				with BaseReader(io.TextIOWrapper(z.open(fastqc_data_file))) as br:
					for s in br:
						if s.startswith("Total Sequences"):
							total_seqs = int(s.split("\t")[1])
				stats[name] = total_seqs
		return stats
	def _get_bam_reads(f, *chrsets):
		import subprocess
		import io
		import os
		from biodata.delimited import DelimitedReader
		if len(chrsets) == 0:
			print("Warning! You should provide some chromosomes, or use '*' for all")
		if not os.path.exists(f):
			raise Exception("File not found.")
		if f.endswith(".bam"):
			s = subprocess.getoutput(f"samtools coverage {f}")
			i = io.StringIO(s)
		else:
			i = f
		with DelimitedReader(i, header=True, skip_header_comment_symbol="#") as dr:
			sums = [0 for _ in range(len(chrsets))]
			for d in dr:
				for e, chrs in enumerate(chrsets):
					if chrs == "*" or d['rname'] in chrs:
						sums[e] += int(d['numreads'])
		return sums
	def fastqc_get_raw_reads(vs):	
		return sum(_fastqc_simple_stat_dict(vs).values())
	def bam_get_reads(vs, *chrsets):
		return sum([int(sum(_get_bam_reads(v, *chrsets))) for v in vs])
	def bam_get_read_pairs(vs, *chrsets):
		return sum([int(sum(_get_bam_reads(v, *chrsets))) // 2 for v in vs])
	def bw_get_reads(vs):
		total = 0
		for v in vs:
			with pyBigWig.open(v) as f:
				total += abs(f.header()['sumData'])
		return total
	def median_read_len(v):
		from biodata.delimited import DelimitedReader
		with DelimitedReader(v) as dr:
			rnalen_dict = {d[0]:d[1] for d in dr}
		return rnalen_dict["median"]
	def gb_ratio(v):
		from biodata.delimited import DelimitedReader
		with DelimitedReader(v,header=True) as dr:
			f = dr.read()["Gene body ratio"]
			return float(f)
	def replicates_correlation(v):
		from biodata.delimited import DelimitedReader
		with DelimitedReader(v,header=True) as dr:
			return ";".join([f'{float(d["Correlation"]):.3f}' for d in dr])

	
	def element_get_stat(k, v, proximal_regions, transcripts_regions):
		# Output: List 
		# No proximal region supplied:
		# One number: total
		# Proximal region supplied:
		# Three numbers: total, proximal, distal
		# Proximal region + transcript region supplied:
		# Four numbers: total, proximal, distal intragenic, distal intergenic
		peaks = BED3Reader.read_all(GenomicCollection, v)
		output_stat_list = []
		
		n_peak = len(peaks)
		output_stat_list.append(n_peak)
		
		if proximal_regions is not None:
			distal_peaks = list(_extract_non_overlaps_generator(peaks, proximal_regions))
			n_peak_proximal = n_peak - len(distal_peaks)
			output_stat_list.append(n_peak_proximal)
			
			n_peak_distal = len(distal_peaks)
			if transcripts_regions is not None:
				n_peak_distal_intragenic = len(list(_extract_non_overlaps_generator(distal_peaks, transcripts_regions)))
				n_peak_distal_intergenic = n_peak_distal - n_peak_distal_intragenic
				output_stat_list.append(n_peak_distal_intragenic)
				output_stat_list.append(n_peak_distal_intergenic)
			else:
				output_stat_list.append(n_peak_distal)
		return output_stat_list
	
	if isinstance(i, str):
		data = _json_load_20240601(i)
	else:
		data = i
		
	if proximal_regions is not None:
		proximal_regions = BED3Reader.read_all(GenomicCollection, proximal_regions)
	if transcripts_regions is not None:
		transcripts_regions = BED3Reader.read_all(GenomicCollection, transcripts_regions)
	if spikein_chrom_sizes is not None:
		spikein_chroms = DelimitedReader.read_all(lambda ds: [d[0] for d in ds], spikein_chrom_sizes)
		
	final_results = {}
	with ProcessWrapPool(nthread) as pool:
	
		for keyname, fr in enumerate(data):
			results = {}
			for k, v in fr.items():
				if k == "Raw read pairs":
					if isinstance(v, str):
						v = [v]
					results[k] = pool.run(fastqc_get_raw_reads, args=[v])
				elif k == "Trimmed read pairs":
					if isinstance(v, str):
						v = [v]
					results[k] = pool.run(fastqc_get_raw_reads, args=[v])
				elif k == "Uniquely mapped read pairs":
					if isinstance(v, str):
						v = [v]
					results[k] = pool.run(bam_get_read_pairs, args=[v, "*"])
				elif k == "Deduplicated read pairs":
					if isinstance(v, str):
						v = [v]
					results[k] = pool.run(bam_get_read_pairs, args=[v, "*"])
				elif k == "Spike-in read pairs":
					if isinstance(v, str):
						v = [v]
					results[k] = pool.run(bam_get_read_pairs, args=[v, spikein_chroms])
				elif k == "Sense read pairs":
					if isinstance(v, str):
						v = [v]
					results[k] = pool.run(bw_get_reads, args=[v])
				elif k == "Antisense read pairs":
					if isinstance(v, str):
						v = [v]
					results[k] = pool.run(bw_get_reads, args=[v])
				elif k == "Median RNA length":
					results[k] = pool.run(median_read_len, args=[v])
				elif k == "Gene body ratio":
					results[k] = pool.run(gb_ratio, args=[v])
				elif k == "Replicates correlation":
					results[k] = pool.run(replicates_correlation, args=[v])
				elif k.endswith("elements"):
					# The suffix should be either Bidirectional Elements; Divergent Elements; Unidirectional Elements
					results[k] = pool.run(element_get_stat, args=[k, v, proximal_regions, transcripts_regions])
				else:
					results[k] = pool.run(str, args=[v])
			final_results[keyname] = results
		keys = sort_multiple_ordered_lists([list(results.keys()) for results in final_results.values()])
		# Fix the keys for elements
		fixed_keys = []
		mapped_fixed_keys = {}
		for k in keys:
			if k.endswith("elements"):
				fixed_keys.append(k)
				if proximal_regions is not None:
					fixed = []
					fixed.append(k + " - Proximal")
					if transcripts_regions is not None:
						fixed.append(k + " - Distal Intragenic")
						fixed.append(k + " - Distal Intergenic")
					else:
						fixed.append(k + " - Distal")
					
					mapped_fixed_keys[k] = fixed
					fixed_keys.extend(fixed)
				else:
					mapped_fixed_keys[k] = []
			else:
				fixed_keys.append(k)
		pool_results = pool.get(wait=True)
	
	if not pool.check_successful_completion():
		raise Exception("Pool fails.")
	
	extracted_results = []
	for results in final_results.values():
		extracted_result = []
		for k in keys:
			if k in results:
				return_value = pool_results[results[k]]
				if k in mapped_fixed_keys:
					for rv in return_value:
						extracted_result.append(rv)
				else:
					extracted_result.append(return_value)
			elif k in mapped_fixed_keys:
				extracted_result.extend([None] * len(mapped_fixed_keys[k]))
			else:
				extracted_result.append(None)
		extracted_results.append(extracted_result)
	
	with DelimitedWriter(o) as dw:
		dw.write(fixed_keys)
		for row in extracted_results:
			dw.write(row)
			
@vt(
	description='''
Checks for RNA-seq design - whether it is a strand specific RNA-seq or not
If you know the library design, you can use this method to validate. 

Outputs --fr-stranded and --rf-stranded abundances. If the percentages are close to 50% it is unlikely strand specific.	
''',
	helps=dict(
		index_file="kallisto index file",
		f1="Read1 fastq file",
		f2="Read2 fastq file",
		nthread="Number of threads"
		
	)
	
)
@vc			
def _check_RNAseq_strand_specificity_20231030(index_file:str, f1:str, f2:str, nthread=1):
	import tempfile
	from mphelper import ProcessWrapPool
	from biodata.delimited import DelimitedReader
	check_binaries_validity("kallisto")

	temp_dir_fr = tempfile.TemporaryDirectory()
	temp_dir_rf = tempfile.TemporaryDirectory()
	pool = ProcessWrapPool(2)
	pool.run(
		bash_command,
		args=[f"kallisto quant --fr-stranded -t {nthread} -i {index_file} -o {temp_dir_fr.name} {f1} {f2}"],
	)
	pool.run(
		bash_command,
		args=[f"kallisto quant --rf-stranded -t {nthread} -i {index_file} -o {temp_dir_rf.name} {f1} {f2}"],
	)
	pool.get(wait=True)
	func = lambda dr: sum(d["est_counts"] for d in dr)
	fr_est_counts = DelimitedReader.read_all(func, f"{temp_dir_fr.name}/abundance.tsv", header=True, funcs={"est_counts":float})
	rf_est_counts = DelimitedReader.read_all(func, f"{temp_dir_rf.name}/abundance.tsv", header=True, funcs={"est_counts":float})
	print(f"--fr-stranded: {fr_est_counts} ({fr_est_counts/(fr_est_counts+rf_est_counts)*100:.2f}%)")
	print(f"--rf-stranded: {rf_est_counts} ({rf_est_counts/(fr_est_counts+rf_est_counts)*100:.2f}%)")
	temp_dir_fr.cleanup()
	temp_dir_rf.cleanup()
				
				
				
@vt(
	description='''
Process sequencing reads (FASTA/FASTQ) into delimited sequences. The method enables a flexible layout set up for easy extraction of sub-sequences.
''',
	helps=dict(
		o="Output delimited file",
		f1="Input sequence file (Read 1)",
		layout1="Layout (json format) corresponding to f1",
		f2="Input sequence file (Read 2). Required for paired-end sequencing.",
		layout2="Layout (json format) corresponding to f2. Required for paired-end sequencing.",
		max_edit_distance="Maximum edit distance when performing constant sequence matching",
		min_last_anchor_match="The minimum matching length required for the last segment",
		keep_unmatch="If True, __UNMATCH__ is indicated in the columns. If False, the reads are not retained. ",
		reverse_complements="The columns you wish to reverse complement in the output",
		column_names="Column names in the output. If not provided, columns will be auto numbered",
		nthread="Number of threads",
		reads_per_thread="Number of reads a thread should handle at a time."
		
	)
)
@vc
def _process_sequencing_reads_to_delimited_sequences_20240624(
		o:str, 
		f1:str, layout1:str,
		f2:str=None, layout2:str=None, 
		max_edit_distance:int=1, 
		min_last_anchor_match:int=1, 
		keep_unmatch:convert_to_bool=False,
		reverse_complements:list[str]=[],
		column_names:list[str]=[],
		nthread:int=1,
		reads_per_thread:int=1000000
	):
	import json
	from biodata.delimited import DelimitedWriter
	from biodata.fasta import FASTQReader
	from .utils.sequence import _process_sequencing_reads_20240624, _reverse_complement_20200726
	fr1 = FASTQReader(f1)
	fr2 = FASTQReader(f2) if f2 is not None else None
	def seq_generator(reader):
		for r in reader:
			yield r.seq
	if isinstance(layout1, str):
		layout1 = json.loads(layout1)
	if layout2 is not None and isinstance(layout2, str):
		layout2 = json.loads(layout2)
	ncols = sum(not isinstance(l, str) for l in layout1) + (0 if layout2 is None else sum(not isinstance(l, str) for l in layout2))
	if len(column_names) == 0:
		column_names = [f"Col-{i}" for i in range(ncols)]
	if len(column_names) != ncols:
		raise Exception("Mismatch of number of columns names and actual number of columns")
	rc_indice = [column_names.index(col) for col in reverse_complements]
	with DelimitedWriter(o) as dw:
		dw.write(column_names)
		
		results = _process_sequencing_reads_20240624(
			seq_generator(fr1), layout1, seq_generator(fr2) if fr2 is not None else None, layout2,
			max_edit_distance, min_last_anchor_match, keep_unmatch, 
			nthread, reads_per_thread
		)
		for r in results:
			if len(rc_indice) > 0:
				r = [_reverse_complement_20200726(content) if idx in rc_indice else content for idx, content in enumerate(r)]
			dw.write(r)
	fr1.close()
	if fr2 is not None:
		fr2.close()
	
@vt(
	description="Process delimited sequences into useful information. ",
	helps=dict(
		i="Input delimited sequence file",
		o="Output delimited sequence file",
		filter="Remove certain rows (entries) that do not match the criteria",
		filter_func="Filter function used in filter",
		rename="Rename columns",
		trim="Trim target sequence by removing any identified query sequence and beyond. Example: `-trim 'column=Element;trimseq=ACGGT;direction=1'`",
		refs="References",
		match="Align sequence to the reference and retrieve the identity of it",  
		align="Align sequence to the reference and retrieve the alignment position",
		map="Map the column values according to the reference map",
		cluster="Cluster the sequences",
		quantify="Use the values from all non-quantify columns as unique keys to group sequences from the quantify columns. ",
		quantify_option="Options for -quantify",
		merge="Merge values from the merge column grouped by non-merge columns as unique keys",
		merge_option="Options for -merge",
		order="Order of the output columns",
		nthread="Number of threads"
	)
)	
@vc
def _process_delimited_sequences_20240710(
		i:str,
		o:str,
		filter:list[str]=[],
		filter_func:list[str]=[],
		rename:str=None,
		trim:list[str]=[],
		refs:str=None,
		match:list[str]=[],  
		align:list[str]=[],
		map:list[str]=[],
		cluster:list[str]=[],
		quantify:list[str]=[],
		quantify_option:str=None,
		merge:list[str]=[],
		merge_option:str="",
		order:list[str]=[],
		nthread:int=1
	):
	import csv 
	import itertools
	from mphelper import ProcessWrapPool
	from commonhelper import distribute_items_evenly, safe_inverse_zip
	from biodata.baseio import get_text_file_rootname, get_text_file_extension
	from biodata.delimited import DelimitedReader, DelimitedWriter
	from biodata.fasta import FASTA, FASTAReader, FASTAWriter
	from .utils.sequence import _read_seq_dict_20211020, _reverse_complement_seq_dict_20211004, _get_match_candidates_20240702, _cluster_sequences_20240710, _get_align_candidates_20240702, _trim_by_template_20240702
	from collections import defaultdict, namedtuple, Counter
	def _quote_split(s, delimiter):
		return next(csv.reader([s],delimiter=delimiter))
	def _process_str(s, required, defaults, funcs):
		entries = dict(defaults)
		d = dict([_quote_split(e, "=") for e in _quote_split(s, ";")])
		if not all(k in d for k in required):
			missing = [k for k in required if k not in d]
			raise Exception("The following options are required: " + ",".join(missing))  
		for k, v in d.items():
			if k in funcs:
				v = funcs[k](v)
			entries[k] = v
		return entries
	def _read_columns_dict(f):
		with DelimitedReader(f) as dr:
			keys = dr.read()
			values = safe_inverse_zip(list(dr), len(keys))
			return dict(zip(keys, values))			
		return d
	
	# Parameters checking and conversion
	if len(filter) > 0:
		if len(filter_func) == 0:
			raise Exception("No filter func is provided")
		if len(filter_func) > 1 and len(filter_func) != len(filter):
			raise Exception("Mismatch number of filter funcs and filter columns")
		if len(filter) > 1 and len(filter_func) == 1:
			filter_func = [filter_func[0] for _ in range(len(filter))]
		filter_func = [eval(func, {}) for func in filter_func]
	if len(match) > 0 or len(align) > 0 or len(map) > 0:
		if refs is None:
			raise Exception("refs must be provided to match or align sequences")
	if len(match) == 0 and len(align) == 0 and len(map) == 0:
		if refs is not None:
			raise Exception("refs is provided but no columns are selected to match or align to references.")

	# Reading ref seqs
	if isinstance(refs, str):
		refs = _process_str(
			refs,
			required=[],
			defaults={},
			funcs={}
		)
		refs = {k:_read_seq_dict_20211020(v, "upper") if get_text_file_extension(v) in ["fa", "fasta"] else _read_columns_dict(v) for k, v in refs.items()}
		
	

	# Parse string from functions
	if rename is None:
		rename = {}
	else:
		rename = _process_str(
			rename,
			required=[],
			defaults={},
			funcs={},
		)
	trim = [_process_str(
		t, 
		required = ["column", "trimseq", "direction"],
		defaults = {"max_edit_distance":1, "min_match_len":6},
		funcs = {"direction":int, "max_edit_distance":int, "min_match_len":int},
	) for t in trim]
	match = [_process_str(
		m, 
		required = ["column", "direction", "strand"],
		defaults = {"group":None, "ref":None, "end_seq":None, "random_start":False, "max_edit_distance":1, "min_match_len":6, "qpenalty":True},
		funcs = {"direction":int, "strand":int, "random_start":convert_to_bool, "max_edit_distance":int, "min_match_len":int, "qpenalty":convert_to_bool},
	) for m in match]
	for m in match:
		if m["group"] is None: 
			m["group"] = m["column"]
		if m["ref"] is None:
			if len(refs) > 1:
				raise Exception("Cannot auto deduce ref seqs")
		
			m["ref"] = list(refs.keys())[0]
			
	align = [_process_str(
		a, 
		required = ["column"],
		defaults = {"group":None, "ref":None, "strand":0, "end_seq":None, "max_edit_distance":1, "min_match_len":16, "qpenalty":True},
		funcs = {"direction":int, "strand":int, "max_edit_distance":int, "min_match_len":int, "qpenalty":convert_to_bool},
	) for a in align]
	for a in align:
		if a["group"] is None: 
			a["group"] = a["column"]
		if a["ref"] is None:
			if len(refs) > 1:
				raise Exception("Cannot auto deduce ref seqs")
			a["ref"] = list(refs.keys())[0]
	map = [_process_str(
		m, 
		required = ["column", "key", "value"],
		defaults = {"name":None, "ref":None, "sep":".", "keep":False},
		funcs={"value":lambda s: s.split(","), "keep":convert_to_bool}
	) for m in map]
	for m in map:
		if m["name"] is None:
			if m["keep"]:
				raise Exception("You must provide a new column name if you keep the old column")
			m["name"] = m["column"]
		if m["ref"] is None:
			if len(refs) > 1:
				raise Exception("Cannot auto deduce reference map")
		
			m["ref"] = list(refs.keys())[0]
	cluster = [_process_str(
		c,
		required = ["column"],
		defaults = {"mode":"connected", "max_edit_distance":1},
		funcs = {"max_edit_distance":int},
	) for c in cluster]
	if len(quantify) > 0: 
		quantify_option = _process_str(
			quantify_option,
			required=[],
			defaults = {"name":None, "mode":"connected", "max_edit_distance":1, "skip_invalid":False},
			funcs = {"max_edit_distance":int, "skip_invalid":convert_to_bool}
		)
		if quantify_option["name"] is None:
			quantify_option["name"] = quantify[0]
	if len(merge) > 0: 
		merge_option = _process_str(
			merge_option,
			required=[],
			defaults = {"skip_invalid":False},
			funcs = {"skip_invalid":convert_to_bool}
		)
	
	# Further checking
	if any(m["strand"] not in [1, -1] for m in match):
		raise Exception("Strand must either be 1 or -1")
	match_cols = set(m["column"] for m in match)
	match_groups = defaultdict(list)
	for m in match:
		match_groups[m["group"]].append(m)
	align_cols = set(m["column"] for m in align)
	align_groups = defaultdict(list)
	for m in align:
		align_groups[m["group"]].append(m)
	discarded_map_cols = set(m["column"] for m in map if not m["keep"])
	map_names = [m["name"] for m in map]
	
	# Input
	with DelimitedReader(i, header=True) as dr:
		header = dr.header_keys
		columns = {k:[] for k in header}
		for d in dr:
			if len(filter) > 0:
				if any(not func(d[col]) for col, func in zip(filter, filter_func)):
					continue
			for k in header:
				columns[k].append(d[k])
	# Rename all columns
	if len(rename) > 0:
		new_columns = {}
		for k in columns.keys():
			if k in rename:
				n = rename[k]
			else:
				n = k
			new_columns[n] = columns[k]
		columns = new_columns
	# Update the order of columns for output if it is not specified
	if len(order) == 0:
		order = []
		for col in columns.keys():
			if col in (list(match_cols) + list(align_cols) + list(discarded_map_cols) + quantify):
				continue
			order.append(col)
		for k in match_groups.keys():
			order.append(k)
		for k in align_groups.keys():
			order.append(k)
		for k in map_names:
			order.append(k)
		if len(quantify) > 0:
			order.append(quantify_option["name"])
			
	# Trimming
	for t in trim:
		columns[t["column"]] = _trim_by_template_20240702(t["trimseq"], columns[t["column"]], t["direction"], t["max_edit_distance"], t["min_match_len"], nthread=nthread)
	# Match
	for g, ms in match_groups.items():
		all_match_results = [] 
		for m in ms:
			all_match_results.append(_get_match_candidates_20240702(refs[m["ref"]], columns[m["column"]], m["strand"], m["direction"], m["end_seq"], m["random_start"], m["max_edit_distance"], m["min_match_len"], m["qpenalty"], nthread))
		match_results = []
		for rs in zip(*all_match_results):
			r = set.intersection(*rs)
			if len(r) == 0:
				match_results.append("__UNMATCH__")
			elif len(r) > 1:
				match_results.append("__AMBIG__")
			else:
				match_results.append(next(iter(r)))
		columns[g] = match_results
	# Align
	for g, aligns in align_groups.items():
		all_align_results = []
		for a in aligns:
			all_align_results.append(_get_align_candidates_20240702(refs[a["ref"]], columns[a["column"]], strand=a["strand"], end_seq=a["end_seq"], max_edit_distance=a["max_edit_distance"], min_match_len=a["min_match_len"], qpenalty=a["qpenalty"], nthread=nthread))
		align_results = []
		for ts in zip(*all_align_results):
			t = set.intersection(*ts)
			if len(t) == 0:
				align_results.append("__UNMATCH__")
			elif len(t) > 1:
				align_results.append("__AMBIG__")
			else:
				align_results.append(":".join([str(i) for i in next(iter(t))]))
		columns[g] = align_results
	# Map
	for m in map:
		ref = refs[m["ref"]]
		v = [m["sep"].join(h) for h in zip(*[ref[t] for t in m["value"]])]
		rdict = dict(safe_inverse_zip([ref[m["key"]], v], len(v)))
		columns[m["name"]] = [rdict[i] if i in rdict else "__UNMATCH__" for i in columns[m["column"]]]
	# Cluster
	if len(cluster) > 0:
		for c in cluster:
			output_prefix = get_text_file_rootname(o)
			cl_out = output_prefix + "_cluster-" + c["column"] + ".tsv.gz"
			r_cl_out = output_prefix + "_cluster-" + c["column"] + ".fa.gz"
			cluster_results = _cluster_sequences_20240710(columns[c["column"]], max_edit_distance=c["max_edit_distance"], mode=c["mode"], nthread=nthread)
			DelimitedWriter.write_all(cluster_results.items(), cl_out)
			cters = defaultdict(Counter)
			for s in columns[c["column"]]:
				cters[cluster_results[s]][s] += 1
				
			reps = [FASTA(str(g), min(cter.items(), key=lambda i: (-1 * i[1], i[0]))[0]) for g, cter in cters.items()]
			FASTAWriter.write_all(reps, r_cl_out)
			columns[c["column"]] = [cluster_results[s] for s in columns[c["column"]]]
	# Quantify
	if len(quantify) > 0:
		# Retrieve columns
		kcols = [col for col in order if col != quantify_option["name"]]
		dls = []
		for q in quantify:
			dl = defaultdict(list)
			for i in range(len(columns[order[0]])):
				k = tuple([columns[col][i] for col in kcols])
				if quantify_option["skip_invalid"]:
					if any(t in ["__AMBIG__", "__UNMATCH__"] for t in k):
						continue
				dl[k].append(columns[q][i])
			dls.append(dl)
		def _quantify_wrapper(dls, keys, max_edit_distance, mode):
			results = []
			for k in keys:
				qcluster_results_list = []
				for dl in dls:
					temp_results = _cluster_sequences_20240710(dl[k], max_edit_distance=max_edit_distance, mode=mode, nthread=1)
					qcluster_results_list.append([temp_results[s] for s in dl[k]])
				results.append(len(set(zip(*qcluster_results_list))))
			return results
		keys = list(dls[0].keys())
		qresults = []
		if nthread > 1:
			pwpool = ProcessWrapPool(nthread)
			results_list_pids = []
			for (start, end) in distribute_items_evenly(len(keys), nthread):
				results_list_pids.append(pwpool.run(_quantify_wrapper, args=[dls, keys[start:end], quantify_option["max_edit_distance"], quantify_option["mode"]]))
			final_results = pwpool.get(wait=True).values()
			pwpool.close()
			if not pwpool.check_successful_completion():
				raise Exception("Pool fails.")
			qresults = list(itertools.chain.from_iterable(final_results))
		else:
			for k in keys:
				qcluster_results_list = []
				for dl in dls:
					temp_results = _cluster_sequences_20240710(dl[k], max_edit_distance=quantify_option["max_edit_distance"], mode=quantify_option["mode"], nthread=1)
					qcluster_results_list.append([temp_results[s] for s in dl[k]])
				qresult = len(set(zip(*qcluster_results_list)))
				qresults.append(qresult)
		new_columns = {col:[k[idx] for k in keys] for idx, col in enumerate(kcols)}
		new_columns[quantify_option["name"]] = qresults
		columns = new_columns
	# Merge
	if len(merge) > 0:
		kcols = [col for col in order if col not in merge]
		dls = {m:defaultdict(list) for m in merge}
		for i in range(len(columns[order[0]])):
			k = tuple([columns[col][i] for col in kcols])
			if merge_option["skip_invalid"]:
				if any(t in ["__AMBIG__", "__UNMATCH__"] for t in k):
					continue
			for m in merge:
				dls[m][k].append(columns[m][i])
		
		keys = list(dls[merge[0]].keys())
		new_columns = {col:[k[idx] for k in keys] for idx, col in enumerate(kcols)}
		for m in merge:	
			import builtins
			new_columns[m] = [sum(list(builtins.map(int, dls[m][k]))) for k in keys]	
		columns = new_columns
	
	# Output
	with DelimitedWriter(o) as dw:
		dw.write(order)
		for i in range(len(columns[order[0]])):
			dw.write([columns[col][i] for col in order])
				
@vt(
	description="Process delimited sequences into useful information. ",
	helps=dict(
		i="Input delimited sequence file",
		o="Output delimited sequence file",
		filter="Remove certain rows (entries) that do not match the criteria",
		filter_func="Filter function used in filter",
		rename="Rename columns",
		trim="Trim target sequence by removing any identified query sequence and beyond. Example: `-trim 'column=Element;trimseq=ACGGT;direction=1'`",
		refs="References",
		match="Align sequence to the reference and retrieve the identity of it",  
		align="Align sequence to the reference and retrieve the alignment position",
		map="Map the column values according to the reference map",
		cluster="Cluster the sequences",
		quantify="Use the values from all non-quantify columns as unique keys to group sequences from the quantify columns. ",
		quantify_option="Options for -quantify",
		merge="Merge values from the merge column grouped by non-merge columns as unique keys",
		merge_option="Options for -merge",
		order="Order of the output columns",
		nthread="Number of threads"
	)
)	
@vc
def _process_delimited_sequences_20241020(
		i:str,
		o:str,
		filter:list[str]=[],
		filter_func:list[str]=[],
		rename:str=None,
		trim:list[str]=[],
		refs:str=None,
		match:list[str]=[],  
		align:list[str]=[],
		map:list[str]=[],
		cluster:list[str]=[],
		quantify:list[str]=[],
		quantify_option:str=None,
		merge:list[str]=[],
		merge_option:str="",
		order:list[str]=[],
		nthread:int=1
	):
	import csv 
	import itertools
	from mphelper import ProcessWrapPool
	from commonhelper import distribute_items_evenly, safe_inverse_zip
	from biodata.baseio import get_text_file_rootname, get_text_file_extension
	from biodata.delimited import DelimitedReader, DelimitedWriter
	from biodata.fasta import FASTA, FASTAReader, FASTAWriter
	from .utils.sequence import _read_seq_dict_20211020, _reverse_complement_seq_dict_20211004, _get_match_candidates_20240702, _cluster_sequences_20240710, _get_align_candidates_20240702, _trim_by_template_20240702
	from collections import defaultdict, namedtuple, Counter
	def _quote_split(s, delimiter):
		return next(csv.reader([s],delimiter=delimiter))
	def _process_str(s, required, defaults, funcs):
		entries = dict(defaults)
		d = dict([_quote_split(e, "=") for e in _quote_split(s, ";")])
		if not all(k in d for k in required):
			missing = [k for k in required if k not in d]
			raise Exception("The following options are required: " + ",".join(missing))  
		for k, v in d.items():
			if k in funcs:
				v = funcs[k](v)
			entries[k] = v
		return entries
	def _read_columns_dict(f):
		with DelimitedReader(f) as dr:
			keys = dr.read()
			values = safe_inverse_zip(list(dr), len(keys))
			return dict(zip(keys, values))			
		return d
	
	# Parameters checking and conversion
	if len(filter) > 0:
		if len(filter_func) == 0:
			raise Exception("No filter func is provided")
		if len(filter_func) > 1 and len(filter_func) != len(filter):
			raise Exception("Mismatch number of filter funcs and filter columns")
		if len(filter) > 1 and len(filter_func) == 1:
			filter_func = [filter_func[0] for _ in range(len(filter))]
		filter_func = [eval(func, {}) for func in filter_func]
	if len(match) > 0 or len(align) > 0 or len(map) > 0:
		if refs is None:
			raise Exception("refs must be provided to match or align sequences")
	if len(match) == 0 and len(align) == 0 and len(map) == 0:
		if refs is not None:
			raise Exception("refs is provided but no columns are selected to match or align to references.")

	# Reading ref seqs
	if isinstance(refs, str):
		refs = _process_str(
			refs,
			required=[],
			defaults={},
			funcs={}
		)
		refs = {k:_read_seq_dict_20211020(v, "upper") if get_text_file_extension(v) in ["fa", "fasta"] else _read_columns_dict(v) for k, v in refs.items()}
		
	

	# Parse string from functions
	if rename is None:
		rename = {}
	else:
		rename = _process_str(
			rename,
			required=[],
			defaults={},
			funcs={},
		)
	trim = [_process_str(
		t, 
		required = ["column", "trimseq", "direction"],
		defaults = {"max_edit_distance":1, "min_match_len":6},
		funcs = {"direction":int, "max_edit_distance":int, "min_match_len":int},
	) for t in trim]
	match = [_process_str(
		m, 
		required = ["column", "direction", "strand"],
		defaults = {"group":None, "ref":None, "end_seq":None, "random_start":False, "max_edit_distance":1, "min_match_len":6, "qpenalty":True, "multi":False},
		funcs = {"direction":int, "strand":int, "random_start":convert_to_bool, "max_edit_distance":int, "min_match_len":int, "qpenalty":convert_to_bool, "multi":convert_to_bool},
	) for m in match]
	for m in match:
		if m["group"] is None: 
			m["group"] = m["column"]
		if m["ref"] is None:
			if len(refs) > 1:
				raise Exception("Cannot auto deduce ref seqs")
		
			m["ref"] = list(refs.keys())[0]
			
	align = [_process_str(
		a, 
		required = ["column"],
		defaults = {"group":None, "ref":None, "strand":0, "end_seq":None, "max_edit_distance":1, "min_match_len":16, "qpenalty":True, "multi":False},
		funcs = {"direction":int, "strand":int, "max_edit_distance":int, "min_match_len":int, "qpenalty":convert_to_bool, "multi":convert_to_bool},
	) for a in align]
	for a in align:
		if a["group"] is None: 
			a["group"] = a["column"]
		if a["ref"] is None:
			if len(refs) > 1:
				raise Exception("Cannot auto deduce ref seqs")
			a["ref"] = list(refs.keys())[0]
	map = [_process_str(
		m, 
		required = ["column", "key", "value"],
		defaults = {"name":None, "ref":None, "sep":".", "keep":False},
		funcs={"value":lambda s: s.split(","), "keep":convert_to_bool}
	) for m in map]
	for m in map:
		if m["name"] is None:
			if m["keep"]:
				raise Exception("You must provide a new column name if you keep the old column")
			m["name"] = m["column"]
		if m["ref"] is None:
			if len(refs) > 1:
				raise Exception("Cannot auto deduce reference map")
		
			m["ref"] = list(refs.keys())[0]
	cluster = [_process_str(
		c,
		required = ["column"],
		defaults = {"mode":"connected", "max_edit_distance":1},
		funcs = {"max_edit_distance":int},
	) for c in cluster]
	if len(quantify) > 0: 
		quantify_option = _process_str(
			quantify_option,
			required=[],
			defaults = {"name":None, "mode":"connected", "max_edit_distance":1, "skip_invalid":False},
			funcs = {"max_edit_distance":int, "skip_invalid":convert_to_bool}
		)
		if quantify_option["name"] is None:
			quantify_option["name"] = quantify[0]
	if len(merge) > 0: 
		merge_option = _process_str(
			merge_option,
			required=[],
			defaults = {"skip_invalid":False},
			funcs = {"skip_invalid":convert_to_bool}
		)
	
	# Further checking
	if any(m["strand"] not in [1, -1] for m in match):
		raise Exception("Strand must either be 1 or -1")
	match_cols = set(m["column"] for m in match)
	match_groups = defaultdict(list)
	for m in match:
		match_groups[m["group"]].append(m)
	align_cols = set(m["column"] for m in align)
	align_groups = defaultdict(list)
	for m in align:
		align_groups[m["group"]].append(m)
	discarded_map_cols = set(m["column"] for m in map if not m["keep"])
	map_names = [m["name"] for m in map]
	
	# Input
	with DelimitedReader(i, header=True) as dr:
		header = dr.header_keys
		columns = {k:[] for k in header}
		for d in dr:
			if len(filter) > 0:
				if any(not func(d[col]) for col, func in zip(filter, filter_func)):
					continue
			for k in header:
				columns[k].append(d[k])
	# Rename all columns
	if len(rename) > 0:
		new_columns = {}
		for k in columns.keys():
			if k in rename:
				n = rename[k]
			else:
				n = k
			new_columns[n] = columns[k]
		columns = new_columns
	# Update the order of columns for output if it is not specified
	if len(order) == 0:
		order = []
		for col in columns.keys():
			if col in (list(match_cols) + list(align_cols) + list(discarded_map_cols) + quantify):
				continue
			order.append(col)
		for k in match_groups.keys():
			order.append(k)
		for k in align_groups.keys():
			order.append(k)
		for k in map_names:
			order.append(k)
		if len(quantify) > 0:
			order.append(quantify_option["name"])
			
	# Trimming
	for t in trim:
		columns[t["column"]] = _trim_by_template_20240702(t["trimseq"], columns[t["column"]], t["direction"], t["max_edit_distance"], t["min_match_len"], nthread=nthread)
	# Match
	retained_match_results = {}
	for g, ms in match_groups.items():
		all_match_results = [] 
		for m in ms:
			all_match_results.append(_get_match_candidates_20240702(refs[m["ref"]], columns[m["column"]], m["strand"], m["direction"], m["end_seq"], m["random_start"], m["max_edit_distance"], m["min_match_len"], m["qpenalty"], nthread))
		
		if g in align_groups:
			# Only generate a temporary intersection results, and store it in a temporary place.
			temp_results = []
			for rs in zip(*all_match_results):
				temp_results.append(set.intersection(*rs))
			retained_match_results[g] = temp_results
		else:
			multi = any(m["multi"] for m in ms)
			match_results = []
			for rs in zip(*all_match_results):
				r = set.intersection(*rs)
				if len(r) == 0:
					match_results.append("__UNMATCH__")
				elif len(r) > 1:
					if multi:
						match_results.append(";".join(sorted(r)))
					else:
						match_results.append("__AMBIG__")
				else:
					match_results.append(next(iter(r)))
			columns[g] = match_results
	# Align
	for g, aligns in align_groups.items():
		all_align_results = []
		for a in aligns:
			all_align_results.append(_get_align_candidates_20240702(refs[a["ref"]], columns[a["column"]], strand=a["strand"], end_seq=a["end_seq"], max_edit_distance=a["max_edit_distance"], min_match_len=a["min_match_len"], qpenalty=a["qpenalty"], nthread=nthread))
		retained_match_result = retained_match_results[g] if g in retained_match_results else None
		multi = any(a["multi"] for a in aligns) or (any(m["multi"] for m in match_groups[g]) if g in match_groups else False)
		align_results = []
		for idx, ts in enumerate(zip(*all_align_results)):
			t = set.intersection(*ts)
			if retained_match_result is not None:
				t = set(i for i in t if i[0] in retained_match_result[idx])
			if len(t) == 0:
				align_results.append("__UNMATCH__")
			elif len(t) > 1:
				if multi:
					align_results.append(";".join([":".join([str(i) for i in tmp]) for tmp in t]))
				else:
					align_results.append("__AMBIG__")
			else:
				align_results.append(":".join([str(i) for i in next(iter(t))]))
		columns[g] = align_results
	# Map
	for m in map:
		ref = refs[m["ref"]]
		v = [m["sep"].join(h) for h in zip(*[ref[t] for t in m["value"]])]
		rdict = dict(safe_inverse_zip([ref[m["key"]], v], len(v)))
		columns[m["name"]] = [rdict[i] if i in rdict else "__UNMATCH__" for i in columns[m["column"]]]
	# Cluster
	if len(cluster) > 0:
		for c in cluster:
			output_prefix = get_text_file_rootname(o)
			cl_out = output_prefix + "_cluster-" + c["column"] + ".tsv.gz"
			r_cl_out = output_prefix + "_cluster-" + c["column"] + ".fa.gz"
			cluster_results = _cluster_sequences_20240710(columns[c["column"]], max_edit_distance=c["max_edit_distance"], mode=c["mode"], nthread=nthread)
			DelimitedWriter.write_all(cluster_results.items(), cl_out)
			cters = defaultdict(Counter)
			for s in columns[c["column"]]:
				cters[cluster_results[s]][s] += 1
				
			reps = [FASTA(str(g), min(cter.items(), key=lambda i: (-1 * i[1], i[0]))[0]) for g, cter in cters.items()]
			FASTAWriter.write_all(reps, r_cl_out)
			columns[c["column"]] = [cluster_results[s] for s in columns[c["column"]]]
	# Quantify
	if len(quantify) > 0:
		# Retrieve columns
		kcols = [col for col in order if col != quantify_option["name"]]
		dls = []
		for q in quantify:
			dl = defaultdict(list)
			for i in range(len(columns[order[0]])):
				k = tuple([columns[col][i] for col in kcols])
				if quantify_option["skip_invalid"]:
					if any(t in ["__AMBIG__", "__UNMATCH__"] for t in k):
						continue
				dl[k].append(columns[q][i])
			dls.append(dl)
		def _quantify_wrapper(dls, keys, max_edit_distance, mode):
			results = []
			for k in keys:
				qcluster_results_list = []
				for dl in dls:
					temp_results = _cluster_sequences_20240710(dl[k], max_edit_distance=max_edit_distance, mode=mode, nthread=1)
					qcluster_results_list.append([temp_results[s] for s in dl[k]])
				results.append(len(set(zip(*qcluster_results_list))))
			return results
		keys = list(dls[0].keys())
		qresults = []
		if nthread > 1:
			pwpool = ProcessWrapPool(nthread)
			results_list_pids = []
			for (start, end) in distribute_items_evenly(len(keys), nthread):
				results_list_pids.append(pwpool.run(_quantify_wrapper, args=[dls, keys[start:end], quantify_option["max_edit_distance"], quantify_option["mode"]]))
			final_results = pwpool.get(wait=True).values()
			pwpool.close()
			if not pwpool.check_successful_completion():
				raise Exception("Pool fails.")
			qresults = list(itertools.chain.from_iterable(final_results))
		else:
			for k in keys:
				qcluster_results_list = []
				for dl in dls:
					temp_results = _cluster_sequences_20240710(dl[k], max_edit_distance=quantify_option["max_edit_distance"], mode=quantify_option["mode"], nthread=1)
					qcluster_results_list.append([temp_results[s] for s in dl[k]])
				qresult = len(set(zip(*qcluster_results_list)))
				qresults.append(qresult)
		new_columns = {col:[k[idx] for k in keys] for idx, col in enumerate(kcols)}
		new_columns[quantify_option["name"]] = qresults
		columns = new_columns
	# Merge
	if len(merge) > 0:
		kcols = [col for col in order if col not in merge]
		dls = {m:defaultdict(list) for m in merge}
		for i in range(len(columns[order[0]])):
			k = tuple([columns[col][i] for col in kcols])
			if merge_option["skip_invalid"]:
				if any(t in ["__AMBIG__", "__UNMATCH__"] for t in k):
					continue
			for m in merge:
				dls[m][k].append(columns[m][i])
		
		keys = list(dls[merge[0]].keys())
		new_columns = {col:[k[idx] for k in keys] for idx, col in enumerate(kcols)}
		for m in merge:	
			import builtins
			new_columns[m] = [sum(list(builtins.map(int, dls[m][k]))) for k in keys]	
		columns = new_columns
	
	# Output
	with DelimitedWriter(o) as dw:
		dw.write(order)
		for i in range(len(columns[order[0]])):
			dw.write([columns[col][i] for col in order])
@vt(
	description="Cluster from multiple delimited files",
	helps=dict(
		i="Input delimited files",
		output_prefix="Output prefix",
		column="Corresponding column name to use for clustering in each delimited file",
		filter_func="Pre-filtering for the clustering",
		mode="Clustering mode",
		max_edit_distance="Max edit distance in clustering",
		nthread="Number of threads for clustering"
	)
)
@vc
def _cluster_delimited_sequences_20241023(
		i:list[str],
		output_prefix:str,
		column:list[str],
		filter_func:str=None, 
		mode:str="connected",
		max_edit_distance:int=1,
		nthread:int=1
	):
	from biodata.delimited import DelimitedReader, DelimitedWriter
	from biodata.fasta import FASTA, FASTAWriter
	from .utils.sequence import _cluster_sequences_20240710
	from collections import defaultdict, Counter
	
	cl_out = output_prefix + ".tsv.gz"
	r_cl_out = output_prefix + ".fa.gz"
	if len(column) != len(i):
		if len(column) != 1:
			raise Exception("Could not determine column in input files")
		column = [column[0]] * len(i)
	if filter_func is not None:
		filter_func = eval(filter_func, {})

	seqs = []
	for f, col in zip(i, column):
		seqs.extend(DelimitedReader.read_all(lambda dr: [d[col] for d in dr], f, header=True))
	if filter_func is not None:		
		seqs = list(filter(filter_func, seqs))
	cluster_results = _cluster_sequences_20240710(seqs, max_edit_distance=max_edit_distance, mode=mode, nthread=nthread)
	DelimitedWriter.write_all(cluster_results.items(), cl_out)
	cters = defaultdict(Counter)
	for s in seqs:
		cters[cluster_results[s]][s] += 1
		
	reps = [FASTA(str(g), min(cter.items(), key=lambda i: (-1 * i[1], i[0]))[0]) for g, cter in cters.items()]
	FASTAWriter.write_all(reps, r_cl_out)
	
			
@vt(
	description="Concatenate multiple delimited files into one. All input files should have the same headers",
	helps=dict(
		i="Input delimited files",
		o="Output delimited file" 
	)
)
@vc
def _concat_delimited_20240715(
		i:list[str], 
		o:str
	):
	from biodata.delimited import DelimitedReader, DelimitedWriter
	drs = [DelimitedReader(f, header=True) for f in i]
	hks = [dr.header_keys for dr in drs]
	if any(hks[0] != hks[x] for x in range(1, len(hks))):
		raise Exception("Mismatch headers in delimited files")
	header_key = hks[0]
	with DelimitedWriter(o) as dw:
		dw.write(header_key)
		for dr in drs:
			for d in dr:
				dw.write([d[k] for k in header_key])
	for dr in drs:
		dr.close()

@vt(
	description="Generate an IDMap from the delimited file"
)
@vc
def _generate_IDMap_from_delimited_20240617( 
	i:str, 
	o:str, 
	id_column:str,
	target_column:str,
	count_column:str,
	skip_targets:list[str]= ["__UNMATCH__", "__AMBIG__"],
	min_perid_dominant_count:int=10, 
	max_perid_target_no:int=-1, 
	min_perid_dominant_count_ratio:float=0.9, 
	min_first_and_second_dominant_fold_difference:float=2):
	import operator
	from collections import defaultdict
	from biodata.delimited import DelimitedReader, DelimitedWriter
	
	ndd = defaultdict(dict)
	with DelimitedReader(i, header=True) as dr:
		for d in dr:
			ndd[d[id_column]][d[target_column]] = int(d[count_column])
	cid_element_map = dict()
	for cid in ndd:
		if max_perid_target_no != -1 and len(ndd[cid]) > max_perid_target_no:
			continue
		dominant_element = max(ndd[cid].items(), key=operator.itemgetter(1))[0]
		dominant_umis = ndd[cid][dominant_element]
		if dominant_umis < min_perid_dominant_count:
			continue
		total_umis = sum(ndd[cid].values())
		if dominant_umis / total_umis < min_perid_dominant_count_ratio:
			continue
		if (len(ndd[cid]) > 1 
			and dominant_umis / sorted(ndd[cid].values())[-2] < min_first_and_second_dominant_fold_difference):
			continue
		cid_element_map[cid] = dominant_element
		
	with DelimitedWriter(o) as dw:
		for cid, element in cid_element_map.items():
			if element in skip_targets:
				continue
			dw.write([cid, element])
@vt(
	description="Generate an IDMap from the delimited file.",
	helps=dict(
		i="Input delimited file",
		o="Output ID Map file",
		id_column="ID columns",
		target_column="Target columns",
		count_column="Count column",
		skip_targets="A list of target entries that should be removed from the ID or target columns",
		min_perid_dominant_count="Minimum count for each ID",
		max_perid_target_no="Maximum targets per ID",
		min_perid_dominant_count_ratio="Minimum dominant count ratio",
		min_first_and_second_dominant_fold_difference="Minimum count ratio between the first and second dominant targets"
	)
)
@vc
def _generate_IDMap_from_delimited_20240801( 
	i:str, 
	o:str, 
	id_column:list[str],
	target_column:list[str],
	count_column:str,
	skip_targets:list[str] = ["__UNMATCH__", "__AMBIG__"],
	min_perid_dominant_count:int=10, 
	max_perid_target_no:int=-1, 
	min_perid_dominant_count_ratio:float=0.8, 
	min_first_and_second_dominant_fold_difference:float=2):
	import operator
	from collections import defaultdict
	from biodata.delimited import DelimitedReader, DelimitedWriter
	
	def get_dominant_target_map(ndd):
		cid_element_map = dict()
		for cid in ndd:
			if max_perid_target_no != -1 and len(ndd[cid]) > max_perid_target_no:
				continue
			dominant_element = max(ndd[cid].items(), key=operator.itemgetter(1))[0]
			dominant_umis = ndd[cid][dominant_element]
			if dominant_umis < min_perid_dominant_count:
				continue
			total_umis = sum(ndd[cid].values())
			if dominant_umis / total_umis < min_perid_dominant_count_ratio:
				continue
			if (len(ndd[cid]) > 1 
				and dominant_umis / sorted(ndd[cid].values())[-2] < min_first_and_second_dominant_fold_difference):
				continue
			if cid in skip_targets or dominant_element in skip_targets:
				continue 
			cid_element_map[cid] = dominant_element
		return cid_element_map
	
	xd = {} 
	for ic_b in id_column:
		for ic_t in id_column + target_column:
			if ic_b != ic_t:
				xd[ic_b, ic_t] = defaultdict(lambda: defaultdict(int))
			
	with DelimitedReader(i, header=True, funcs={count_column:int}) as dr:
		for d in dr:
			for ic_b in id_column:
				for ic_t in id_column + target_column:
					if ic_b != ic_t:
						xd[ic_b, ic_t][d[ic_b]][d[ic_t]] += d[count_column] 
	dd = {}
	for ic_b in id_column:
		for ic_t in id_column:
			if ic_b != ic_t:
				dd[ic_b, ic_t] = get_dominant_target_map(xd[ic_b, ic_t])
	for ic in id_column:
		for tc in target_column:
			dd[ic, tc] = get_dominant_target_map(xd[ic, tc])
	kbase = id_column[0]
	tkeys = set.intersection(*[set(dd[ic_b, ic_t].keys()) for ic_b, ic_t in dd.keys() if ic_b == kbase])	
	ktarget = id_column[1] if len(id_column) > 1 else target_column[0]
	with DelimitedWriter(o) as dw:
		dw.write(id_column + target_column)
		for k in dd[kbase, ktarget]:
			if k not in tkeys:
				continue
			dominant_keys = {kbase:k}
			dominant_keys.update({ic_t:dd[kbase, ic_t][k] for ic_t in id_column[1:]})
			dominant_keys.update({tc:dd[kbase, tc][k] for tc in target_column})
			used = True
			for ic_b in id_column:
				for ic_t in id_column + target_column:
					if ic_b != ic_t:
						if not(dominant_keys[ic_b] in dd[ic_b, ic_t] and dd[ic_b, ic_t][dominant_keys[ic_b]] == dominant_keys[ic_t]):
							used = False
							break
				if not used:
					break
			if not used:
				continue
			dw.write(list(dominant_keys.values()))
@vt(
	description="Generate an IDMap from the delimited file.",
	helps=dict(
		i="Input delimited file",
		o="Output ID Map file",
		id_column="ID columns",
		count_column="Count column",
		target_column="Target columns",
		skip_targets="A list of target entries that should be removed from the ID or target columns",
		min_perid_dominant_count="Minimum count for each ID",
		max_perid_target_no="Maximum targets per ID",
		min_perid_dominant_count_ratio="Minimum dominant count ratio",
		min_first_and_second_dominant_fold_difference="Minimum count ratio between the first and second dominant targets"
	)
)
@vc
def _generate_IDMap_from_delimited_20241024( 
	i:str, 
	o:str, 
	id_column:list[str],
	count_column:str,
	target_column:list[str]=[],
	skip_targets:list[str] = ["__UNMATCH__", "__AMBIG__"],
	min_perid_dominant_count:int=10, 
	max_perid_target_no:int=-1, 
	min_perid_dominant_count_ratio:float=0.8, 
	min_first_and_second_dominant_fold_difference:float=2):
	import operator
	from collections import defaultdict
	from biodata.delimited import DelimitedReader, DelimitedWriter
	
	def get_dominant_target_map(ndd):
		cid_element_map = dict()
		for cid in ndd:
			if max_perid_target_no != -1 and len(ndd[cid]) > max_perid_target_no:
				continue
			dominant_element = max(ndd[cid].items(), key=operator.itemgetter(1))[0]
			dominant_umis = ndd[cid][dominant_element]
			if dominant_umis < min_perid_dominant_count:
				continue
			total_umis = sum(ndd[cid].values())
			if dominant_umis / total_umis < min_perid_dominant_count_ratio:
				continue
			if (len(ndd[cid]) > 1 
				and dominant_umis / sorted(ndd[cid].values())[-2] < min_first_and_second_dominant_fold_difference):
				continue
			if cid in skip_targets or dominant_element in skip_targets:
				continue 
			cid_element_map[cid] = dominant_element
		return cid_element_map
	
	xd = {} 
	for ic_b in id_column:
		for ic_t in id_column + target_column:
			if ic_b != ic_t:
				xd[ic_b, ic_t] = defaultdict(lambda: defaultdict(int))
			
	with DelimitedReader(i, header=True, funcs={count_column:int}) as dr:
		for d in dr:
			for ic_b in id_column:
				for ic_t in id_column + target_column:
					if ic_b != ic_t:
						xd[ic_b, ic_t][d[ic_b]][d[ic_t]] += d[count_column] 
	dd = {}
	for ic_b in id_column:
		for ic_t in id_column:
			if ic_b != ic_t:
				dd[ic_b, ic_t] = get_dominant_target_map(xd[ic_b, ic_t])
	for ic in id_column:
		for tc in target_column:
			dd[ic, tc] = get_dominant_target_map(xd[ic, tc])
	kbase = id_column[0]
	tkeys = set.intersection(*[set(dd[ic_b, ic_t].keys()) for ic_b, ic_t in dd.keys() if ic_b == kbase])	
	ktarget = id_column[1] if len(id_column) > 1 else target_column[0]
	with DelimitedWriter(o) as dw:
		dw.write(id_column + target_column)
		for k in dd[kbase, ktarget]:
			if k not in tkeys:
				continue
			dominant_keys = {kbase:k}
			dominant_keys.update({ic_t:dd[kbase, ic_t][k] for ic_t in id_column[1:]})
			dominant_keys.update({tc:dd[kbase, tc][k] for tc in target_column})
			used = True
			for ic_b in id_column:
				for ic_t in id_column + target_column:
					if ic_b != ic_t:
						if not(dominant_keys[ic_b] in dd[ic_b, ic_t] and dd[ic_b, ic_t][dominant_keys[ic_b]] == dominant_keys[ic_t]):
							used = False
							break
				if not used:
					break
			if not used:
				continue
			dw.write(list(dominant_keys.values()))
						
@vt(
	description="Join multiple ID Maps into one ID Map. ",
	helps=dict(
		i="Input ID Map files",
		o="Output ID Map file",
		id_column="ID columns",
		target_column="Target columns",
	)
)
@vc
def _join_IDMap_20241024(i:list[str], o:str, id_column:list[str], target_column:list[str]=[]):
	from biodata.delimited import DelimitedReader, DelimitedWriter
	maps = []
	for f in i:
		with DelimitedReader(f, header=True) as dr:
			maps.append([dr.header_keys, list(dr)])
			
	base_ic = id_column[0]
	# Initialize the entries but taking the first id column
	all_keys = set(k for header_keys, m in maps for k in header_keys)
	missing_cols = [col for col in id_column + target_column if col not in all_keys]
	if len(missing_cols) > 0:
		raise Exception("The following id_columns or target_columns are not present in any IDMap: " + ",".join(missing_cols))
	
	for header_keys, m in maps:
		if base_ic in header_keys:
			entries = [{base_ic:r[base_ic]} for r in m]
			break
	connected_ics = {base_ic}
	used_ics = set()
	while len(used_ics) != len(id_column):
		# Get the next connected id column to use 
		next_ic = None
		for ic_b in id_column:
			if ic_b in used_ics:
				continue
			if ic_b not in connected_ics:
				continue
			next_ic = ic_b
			break
		if next_ic is None:
			raise Exception("Cannot connect the IDs")
		ic_b = next_ic
		used_ics.add(ic_b)
		
		# Intersection of all presence of the keys in all ID maps
		for header_keys, m in maps:
			if ic_b not in header_keys:
				continue
			s = set(r[ic_b] for r in m)
			entries = [e for e in entries if e[ic_b] in s]
		
		# Look for new connected columns. If the connection is already present, remove entries that do not match
		for ic_t in id_column + target_column:
			if ic_b != ic_t:
				for header_keys, m in maps:
					if not(ic_b in header_keys and ic_t in header_keys):
						continue
					connected_ics.add(ic_t)
					d = {r[ic_b]:r[ic_t] for r in m}
					new_entries = []
					for e in entries:
						if e[ic_b] in d:
							if ic_t in e:
								if e[ic_t] != d[e[ic_b]]:
									continue
							else:
								e[ic_t] = d[e[ic_b]]
							new_entries.append(e)
					entries = new_entries
	with DelimitedWriter(o) as dw:
		dw.write(id_column + target_column)
		for e in entries:
			dw.write([e[ic] for ic in id_column + target_column])
			

@vt(
	description="Annotate multiple bed files by names. ",
	helps=dict(
		i="Input annotated bed files",
		o="Output annotated bed file",
		clsname="Class names corresponding to the input annotated bed files.",
		column="The column to insert the new annotation"
	)
)
@vc
def _annotate_bed_classes_20240925(
	i:list[str],
	o:str,
	clsname:list[str],
	column:int=None
):
	from biodata.delimited import DelimitedReader, DelimitedWriter
	if len(i) != len(clsname):
		raise Exception("Mismatched length of input files and names")
	with DelimitedWriter(o) as dw:
		for f, n in zip(i, clsname):
			with DelimitedReader(f) as dr:
				for d in dr:
					if column is None:
						dw.write(d + [n])
					else:
						dw.write(d[:column] + [n] + d[column:])
@vt(
	description="Annotate bed file by overlaps. ",
	helps=dict(
		i="Input annotated bed file",
		r="Input reference file",
		o="Output annotated bed file",
		pcls="Name for overlapped entries",
		ncls="Name for non-overlapped entries",
		column="The column to insert the new annotation"
	)
)
@vc
def _annotate_bed_overlaps_20240925(
	i:str,
	r:str,
	o:str,
	pcls:str,
	ncls:str,
	column:int=None
):
	from genomictools import GenomicCollection
	from biodata.bed import BED3, BED3Reader
	from biodata.delimited import DelimitedReader, DelimitedWriter
	refs = BED3Reader.read_all(GenomicCollection, r)
	with DelimitedReader(i) as dr, DelimitedWriter(o) as dw:
		for d in dr:
			r = BED3(d[0], int(d[1]), int(d[2]))
			n = pcls if refs.overlaps(r) else ncls
			if column is None:
				dw.write(d + [n])
			else:
				dw.write(d[:column] + [n] + d[column:])
@vt(
	description="Annotate bed file with directionality index",
	helps=dict(
		i="Input annotated bed file",
		ipl="Input plus-strand bigwig file",
		imn="Input minus-strand bigwig file",
		o="Output annotated bed file",
		column="The column to insert the new annotation"
	)
)
@vc
def _annotate_bed_directionality_index_20240925(
	i:str,
	ipl:str,
	imn:str,
	o:str,
	column:int=None
):
	from biodata.bed import BED3
	from biodata.bigwig import BigWigIReader
	from biodata.delimited import DelimitedReader, DelimitedWriter
	with BigWigIReader(ipl) as bwpl, BigWigIReader(imn) as bwmn, DelimitedReader(i) as dr, DelimitedWriter(o) as dw:
		for d in dr:
			r = BED3(d[0], int(d[1]), int(d[2]))
			plcount = bwpl.value(r, method="abssum")
			mncount = bwmn.value(r, method="abssum")
			n = (plcount - mncount) / (plcount+mncount)
			if column is None:
				dw.write(d + [n])
			else:
				dw.write(d[:column] + [n] + d[column:])
@vt(
	description="Summarize annotated bed files into a table",
	helps=dict(
		i="Input annotated bed files",
		name="Sample names of the inputs",
		o="Output table file",
		func="A function to create a unique group. By default the forth to last columns are all used to create the unique group. "
	)
)
@vc
def _summarize_bed_annotation_counts_20240925(
	i:list[str],
	name:list[str],
	o:str,
	func:str=None,
):
	import itertools
	from collections import Counter
	from biodata.delimited import DelimitedReader, DelimitedWriter
	if func is None:
		func = lambda d: "-".join(d[4:])
	else:
		func = eval(func, {})
	cters = {}
	for f, n in zip(i, name):
		with DelimitedReader(f) as dr:
			cters[n] = Counter([func(d) for d in dr])
	keys = sorted(set(itertools.chain.from_iterable([cter.keys() for s, cter in cters.items()])))
	with DelimitedWriter(o) as dw:
		dw.write(["Group"] + name)
		for k in keys:
			dw.write([k] + [cters[n][k] for n in name])
			
@vt(
	description="Modify a bed annotation file",
	helps=dict(
		i="Input bed annotation files",
		o="Output bed annotation file",
		func="A function to modify each entry"
	)	
)
@vc
def _modify_bed_annotation_20240925(
	i:str,
	o:str,
	func:str
):	
	from biodata.delimited import DelimitedReader, DelimitedWriter
	func = eval(func, {})
	with DelimitedReader(i) as dr, DelimitedWriter(o) as dw:
		for d in dr:
			dw.write(func(d))

@vt(
	description="Plot two-way correlation between samples in the count table",
	helps=dict(
		i="Input count table file", 
		o="Output plot file",
		filter_func="Filtering function applied to each pair of values between two samples.",
		value_func="Value function applied to the count table before plotting. Applied after filter_func.",
		keys="Selected keys to plot correlation",
		labels="A dictionary to map label in count table to names used in plot",
		scatter_kw="Scatter kw",
		fig_change_kw="Figure changes kw",
		fig_save_kw="Figure save kw"
	)
)
@vc
def _plot_count_tables_correlation_20240901(
	i:list[str], 
	o:str, 
	filter_func:str=None, 
	value_func:str=None, 
	keys:list[str]=[],
	labels:str=None,
	plot_kw={},
	fig_change_kw={},
	fig_save_kw:str={}
):
	from .utils.common import _read_json_like_struct_20240601
	
	import itertools
	import math
	import numpy as np
	
	from commonhelper import safe_inverse_zip
	from biodata.delimited import DelimitedReader, DelimitedWriter
	from biodataplot.common import _plot_two_way_correlation_20240901
	from biodataplot.utils import _plt_change_figure_properties_20240501

	tables = None
	for f in i:
		with DelimitedReader(f) as dr:
			header = dr.read()[1:]
			if keys is None or len(keys) == 0:
				keys = header
			tmp_tables = safe_inverse_zip([list(map(float, d[1:])) for d in dr], len(keys))
			indice = [header.index(k) for k in keys]
			tmp_tables = {keys[idx]:tmp_tables[idx] for idx in indice}
			if tables is None:
				tables = {k:list(t) for k, t in tmp_tables.items()}
			else:
				for k in keys:
					tables[k].extend(tmp_tables[k])
	
	if filter_func is not None:
		filter_func = eval(filter_func, {})
	if value_func is not None:
		value_func = eval(value_func, {"math":math})
	labels = _read_json_like_struct_20240601(labels)
	fig_change_kw = _read_json_like_struct_20240601(fig_change_kw)
	fig_save_kw = _read_json_like_struct_20240601(fig_save_kw)
	
	fig = _plot_two_way_correlation_20240901(
		tables, xkeys=keys[:-1], ykeys=keys[1:], 
		**{"scatter_kw":{"s":1, "alpha":0.5, "color":"#636363"}, **plot_kw}, 
		value_func=value_func, filter_func=filter_func, labels=labels)
	
	_plt_change_figure_properties_20240501(
		fig, 
		fig_supxlabel="Count",
		fig_supylabel="Count",
		fig_supxlabel_prop={"fontsize":16},
		fig_supylabel_prop={"fontsize":16},
		xlabel_prop={"fontsize":14},
		ylabel_prop={"fontsize":14},
	)
	
	if len(fig_change_kw) > 0:
		_plt_change_figure_properties_20240501(
			fig, **fig_change_kw
		)
	fig.tight_layout()
	fig.savefig(o, **{"dpi":300, "bbox_inches":"tight", **fig_save_kw})
	return fig

@vt(
	description="Merge multiple STARR element counts into a table. Usually element counts from different replicates in the same experiments are merged",
	helps=dict(
		idna="List of DNA element counts files",
		irna="List of RNA element counts files",
		o="Output file",
		missing_value="Strategy to deal with missing value in certain element counts file. Currently only 'zero' is supported, where missing values are assumed to have zero counts.",
		filter_func="A function to filter unwanted entries",
		element_column="The names of input columns as the element key. If multiple input colums are provided, they will be joined using column_sep",
		column_sep="The delimiter used to join multiple column names",
		count_column="The name of the count column",
	)
)
@vc
def _merge_STARR_element_counts_20240801(
		idna:list[str], irna:list[str], o:str,
		missing_value:str="zero", 
		filter_func=None, element_column:list[str]=["Element"], count_column:str="Count", column_sep="."):
	from biodata.delimited import DelimitedReader, DelimitedWriter
	if missing_value == "zero":
		missing_value = 0
	else:
		raise Exception("Unsupported missing value")
		
	if filter_func is None:
		filter_func = lambda d: True
	elif isinstance(filter_func, str):
		filter_func = eval(filter_func, {})
	ds = []
	for i in idna + irna:
		ds.append(DelimitedReader.read_all(lambda dr: {column_sep.join(d[t] for t in element_column):d[count_column] for d in dr if filter_func(d)}, i, header=True))
	union_keys = sorted(set.union(*[set(ec.keys()) for ec in ds]))
	with DelimitedWriter(o) as dw:
		dw.write(["Element"] + [f"DNA{i+1}" for i in range(len(idna))] + [f"RNA{i+1}" for i in range(len(irna))])
		for k in union_keys:
			dw.write([k] + [ec[k] if k in ec else missing_value for ec in ds])
			
	
@vt(
	description="Generate logFCs using a limma-based method. ",
	helps=dict(
		i="Input element counts file",
		n="Negative control file",
		o="Output activity call file",
		f="A sample-group table file. If not provided, this is auto determine based on the column names in the element count file"
	)
)
@vc
def _generate_STARR_logFC_by_limma_20240801(i:str, o:str, n:str, f:str=None):

	rscript_template = '''
library(edgeR)
library(dplyr)
input_count_file <- commandArgs(trailingOnly = TRUE)[1]
sample_info_file <- commandArgs(trailingOnly = TRUE)[2]
input_neg_ctrl_file <- commandArgs(trailingOnly = TRUE)[3]
output_file <- commandArgs(trailingOnly = TRUE)[4]
neg_ctrls <- readLines(input_neg_ctrl_file)
counts = read.delim(input_count_file, row.names=1)
counts <- counts[complete.cases(counts),]
d0 <- DGEList(counts)
dneg <- d0[which(rownames(d0) %in% neg_ctrls), ]
dneg <- calcNormFactors(dneg, logratioTrim=0, sumTrim=0)
d0$samples <- dneg$samples
cutoff <- 10
todrop <- which(apply(cpm(d0), 1, max) < cutoff)
if (length(todrop) != 0) d <- d0[-todrop,] else d <- d0
sample_info = read.table(sample_info_file, sep="\t", header=T)
group=as.factor((sample_info[sample_info["Sample"] == colnames(d0), ]$Group))

mm <- model.matrix(~0 + group)
y <- voom(d, mm) #, plot = T
fit <- lmFit(y, mm)
contr <- makeContrasts(groupRNA - groupDNA, levels = colnames(coef(fit)))
tmp <- contrasts.fit(fit, contr)
tmp <- eBayes(tmp)
top.table <- topTable(tmp, sort.by = "logFC", n = Inf)
top.table <- top.table[order(top.table$logFC, decreasing = TRUE),]
m <- merge(cpm(d0),top.table,by="row.names",all.x=TRUE)
colnames(m)[1] <- "Element"
if (endsWith(output_file, ".gz")) {
	gz1 <- gzfile(output_file, "w")
	write.table(m, gz1, row.names=FALSE, quote=FALSE, sep="\t")
	close(gz1)
} else {
	write.table(m,output_file, row.names=FALSE, quote=FALSE, sep="\t")
}
'''
	from biodata.baseio import BaseWriter
	from biodata.delimited import DelimitedReader, DelimitedWriter
	import tempfile
	import os
	check_binaries_validity("Rscript")
	tmpfiles = []
	if f is None:
		s = tempfile.NamedTemporaryFile(mode='w+', suffix=".txt", delete=False).name
		tmpfiles.append(s)
		with DelimitedReader(i, header=True) as dr, DelimitedWriter(s) as dw:
			dw.write(["Sample", "Group"])
			for k in dr.header_keys[1:]:
				if k.startswith("DNA"):
					dw.write([k, "DNA"])
				elif k.startswith("RNA"):
					dw.write([k, "RNA"])
				else:
					raise Exception()
		f = s
	s = tempfile.NamedTemporaryFile(mode='w+', suffix=".R", delete=False).name
	tmpfiles.append(s)
	BaseWriter.write_all([rscript_template], s)
	bash_command(
		"Rscript {s} {i} {f} {n} {o}".format(
		s=s,
		i=i,
		f=f,
		n=n,
		o=o,
	)
	)
	for s in tmpfiles:
		os.unlink(s)
		
@vt(
	description="Generate STARR activity call. The activity of an element in one orientation could be called as PositiveActivity, NegativeActivity or Inactive. When combining both orientations, an additional activity Ambig will be assigned if the activity from the two orientations are different. Elements with missing data will be assigned NA activity",
	helps=dict(
		i="Input logFC file",
		n="Negative control file",
		o="Output activity call file",
		fwd_suffix="Suffix for element in forward orientation",
		rev_suffix="Suffix for element in reverse orientation",
	)
)
@vc
def _generate_STARR_activity_call_20240801(i, n, o, fwd_suffix=".fwd", rev_suffix=".rev"):
	from biodata.baseio import BaseReader
	from biodata.delimited import DelimitedReader, DelimitedWriter
	import numpy as np
	from collections import defaultdict
	
	
	float_func = lambda d: "NA" if d == "NA" else float(d)
	combined_func = lambda f, r: "NA" if f == "NA" or r == "NA" else (f if f == r else "Ambig")
	logFC_combined_func = lambda f, r: "NA" if f == "NA" or r == "NA" else ((f + r) / 2)

	tbl = DelimitedReader.read_all(lambda dr: {d["Element"]:d for d in dr}, i, header=True, funcs={"logFC":float_func, "adj.P.Val":float_func})
	neg_ctrl_elements = BaseReader.read_all(set, n)
	neg_logFCs = [tbl[e]["logFC"] for e in neg_ctrl_elements if e in tbl and tbl[e]["logFC"] != "NA"]
	mean_neg_ctrl = np.mean(neg_logFCs)
	std_neg_ctrl = np.std(neg_logFCs)
	logFC_cutoff = 1.96 * std_neg_ctrl+mean_neg_ctrl
	b = defaultdict(lambda: defaultdict(lambda: "NA"))
	logFCs = defaultdict(lambda: defaultdict(lambda: "NA"))
	for d in tbl.values():
		if d["logFC"] == "NA" or d["adj.P.Val"] == "NA":
			status = "NA"
		else:
			zscore = (d["logFC"] - mean_neg_ctrl) / std_neg_ctrl
			if zscore >= logFC_cutoff and d["adj.P.Val"] < 0.05:
				status = "PositiveActivity"
			elif zscore <= -1*logFC_cutoff and d["adj.P.Val"] < 0.05:
				status = "NegativeActivity"
			else:
				status = "Inactive"
				
		if d["Element"].endswith(fwd_suffix):
			b[d["Element"][:-len(fwd_suffix)]]["Forward"] = status
			logFCs[d["Element"][:-len(fwd_suffix)]]["Forward"] = d["logFC"]
		elif d["Element"].endswith(rev_suffix):
			b[d["Element"][:-len(rev_suffix)]]["Reverse"] = status
			logFCs[d["Element"][:-len(rev_suffix)]]["Reverse"] = d["logFC"]
		else:
			raise Exception()	
	with DelimitedWriter(o) as dw:
		dw.write(["Element", "Forward-logFC", "Reverse-logFC", "logFC", "Forward-Call", "Reverse-Call", "Call"])
		for element in b:
			dw.write([element, 
				logFCs[element]["Forward"], logFCs[element]["Reverse"], logFC_combined_func(logFCs[element]["Forward"], logFCs[element]["Reverse"]),
				b[element]["Forward"], b[element]["Reverse"], combined_func(b[element]["Forward"], b[element]["Reverse"])])

@vt(
	description="Create a ranked plot for STARR logFCs",
	helps=dict(
		i="Input logFC files",
		name="Names corresponding to the inputs",
		o="Output plot file",
		group="A dictionary containing group name as key and list of group elements as values",
		default_group_name="If an element does not appear in any group, it will be assigned to the default group",
		plot_kw="Plot arguments",
		plot_kw_dict="Group-specific plot arguments",
		line_kw="Line arguments",
		fig_change_kw="Figure change arguments",
		fig_save_kw="Figure save arguments",
	)
)			
@vc
def _plot_STARR_ranked_logFCs_20240901(
	i:list[str], name:list[str], o:str, 
	group:str={}, default_group_name:str="Elements", 
	plot_kw:str={}, plot_kw_dict:str={}, 
	line_kw:str={},
	fig_change_kw:str={}, fig_save_kw:str={}
):
	import matplotlib.pyplot as plt
	from biodata.delimited import DelimitedReader
	from biodataplot.common import _plot_ranked_values_20240601
	from biodataplot.utils import _plt_change_figure_properties_20240501
	from .utils.common import _read_json_like_struct_20240601
	def _rev_dict(d):
		new_dict = {}
		for k, vs in d.items():
			for v in vs:
				if v in new_dict:
					raise Exception("Duplicated values to be used in dict")
				new_dict[v] = k
		return new_dict
	float_func = lambda d: "NA" if d == "NA" else float(d)
	group = _read_json_like_struct_20240601(group)
	plot_kw = _read_json_like_struct_20240601(plot_kw)
	plot_kw_dict = _read_json_like_struct_20240601(plot_kw_dict)
	line_kw = _read_json_like_struct_20240601(line_kw)
	fig_change_kw = _read_json_like_struct_20240601(fig_change_kw)
	fig_save_kw = _read_json_like_struct_20240601(fig_save_kw)
	calls = {}
	for f, n in zip(i, name):
		calls[n] = DelimitedReader.read_all(lambda dr: {d["Element"]:d for d in dr if d["logFC"] != "NA"}, f, header=True, funcs={"logFC":float_func, "Forward-logFC":float_func, "Reverse-logFC":float_func})
	shared_keys = set.intersection(*[set(c.keys()) for c in calls.values()])
	
	rev_group = _rev_dict(group)
	fig, axs = plt.subplots(1, len(i), sharey=True)
	
	for (n, c), ax in zip(calls.items(), axs.reshape(-1)):
		data = {k:[] for k in group}
		if default_group_name is not None:
			data[default_group_name] = []
		for k in shared_keys:
			data[rev_group[k] if k in rev_group else default_group_name].append(c[k]["logFC"])
		
		ax.axhline(**{"y":0, "ls":"--", "c":"grey", **line_kw})
		
		_plot_ranked_values_20240601(data, ax=ax, plot_kw=plot_kw, plot_kw_dict=plot_kw_dict)
		ax.set_title(n)
	axs[-1].legend(loc="upper left", bbox_to_anchor=[1,1])
	fig.supylabel("logFC")
	fig.supxlabel("Rank")
	_plt_change_figure_properties_20240501(
		fig, 
		fig_supxlabel_prop={"fontsize":16},
		fig_supylabel_prop={"fontsize":16},
		xlabel_prop={"fontsize":14},
		ylabel_prop={"fontsize":14},
		title_prop={"fontsize":18},
		legend_text_prop={"fontsize":14}
	)
	
	if len(fig_change_kw) > 0:
		_plt_change_figure_properties_20240501(
			fig, **fig_change_kw
		)
	fig.savefig(o, **{"dpi":300, "bbox_inches":"tight", **fig_save_kw})
	return fig
@vt(
	description="Create replicates correlation plot for STARR logFCs",
	helps=dict(
		i="Input STARR logFC file",
		o="Output plot file",
		group="A dictionary containing replicate name as key and list of DNA, RNA key as values",
		plot_kw="Plot arguments",
		fig_change_kw="Figure change arguments",
		fig_save_kw="Figure save arguments",
	)
)			
@vc
def _plot_STARR_replicates_correlation_20241001(
		i:str, o:str, group:str=None, 
		plot_kw:str={}, fig_change_kw:str={}, fig_save_kw:str={}
	):
	from biodata.delimited import DelimitedReader
	from biodataplot.common import _plot_two_way_correlation_20240901
	from biodataplot.utils import _plt_change_figure_properties_20240501
	from .utils.common import _read_json_like_struct_20240601
	import numpy as np
	import re
	float_func = lambda d: float("nan") if d == "NA" else float(d)
	group = _read_json_like_struct_20240601(group)
	plot_kw = _read_json_like_struct_20240601(plot_kw)
	fig_change_kw = _read_json_like_struct_20240601(fig_change_kw)
	fig_save_kw = _read_json_like_struct_20240601(fig_save_kw)
	
	with DelimitedReader(i, header=True) as dr:
		dna_keys = {}
		rna_keys = {}
		if group is None:
			for k in dr.header_keys:
				m = re.match("^DNA([0-9]+)$", k)
				if m is not None:
					dna_keys[int(m.group(1))] = k
				m = re.match("^RNA([0-9]+)$", k)
				if m is not None:
					rna_keys[int(m.group(1))] = k
			group = {f"Replicate {k}":[dna_keys[k], rna_keys[k]] for k in sorted(set.intersection(set(dna_keys), set(rna_keys)))}
		data = {g:{} for g in group}
		for d in dr:
			for g, (dnak, rnak) in group.items():
				if float_func(d[dnak]) >= 10:
					data[g][d["Element"]] = np.log2((float_func(d[rnak])+1) / float_func(d[dnak]))
		
	fig = _plot_two_way_correlation_20240901(
		data,
		xkeys=list(data.keys())[:-1],
		ykeys=list(data.keys())[1:],
		**{"scatter_kw":{"s":1, "color":"#636363"}, "skip_same_keys":True, **plot_kw}
	)
	_plt_change_figure_properties_20240501(
		fig, 
		fig_supxlabel="$log_{2}$ RNA/DNA ratio",
		fig_supxlabel_prop={"fontsize":16},
		fig_supylabel="$log_{2}$ RNA/DNA ratio",
		fig_supylabel_prop={"fontsize":16},
		xlabel_prop={"fontsize":14},
		ylabel_prop={"fontsize":14}
	)
	if len(fig_change_kw) > 0:
		_plt_change_figure_properties_20240501(
			fig, **fig_change_kw
		)
	fig.tight_layout()
	fig.savefig(o, **{"dpi":300, "bbox_inches":"tight", **fig_save_kw})
	return fig	
@vt(
	description="Create orientation correlation plot for STARR",
	helps=dict(
		i="Input STARR activity file",
		o="Output plot file",
		plot_kw="Plot arguments",
		fig_change_kw="Figure change arguments",
		fig_save_kw="Figure save arguments",
	)
)			
@vc
def _plot_STARR_orientation_correlation_20241001(
		i:str, o:str, 
		plot_kw:str={}, fig_change_kw:str={}, fig_save_kw:str={}):
	import math
	import re
	from biodata.delimited import DelimitedReader
	from biodataplot.common import _plot_two_way_correlation_20240901
	from biodataplot.utils import _plt_change_figure_properties_20240501
	from .utils.common import _read_json_like_struct_20240601

	float_func = lambda d: float("nan") if d == "NA" else float(d)
	plot_kw = _read_json_like_struct_20240601(plot_kw)
	fig_change_kw = _read_json_like_struct_20240601(fig_change_kw)
	fig_save_kw = _read_json_like_struct_20240601(fig_save_kw)

	data = {k:[] for k in ["Forward-logFC", "Reverse-logFC"]}
	with DelimitedReader(i, header=True,funcs={"Forward-logFC":float_func, "Reverse-logFC":float_func}) as dr:
		for d in dr:
			if math.isnan(d["Forward-logFC"]) or math.isnan(d["Reverse-logFC"]):
				continue
			data["Forward-logFC"].append(d["Forward-logFC"])
			data["Reverse-logFC"].append(d["Reverse-logFC"])
			
	fig = _plot_two_way_correlation_20240901(
		data,
		xkeys=["Forward-logFC"],
		ykeys=["Reverse-logFC"],
		**{"scatter_kw":{"s":1, "color":"#636363"}, **plot_kw}
	)
	_plt_change_figure_properties_20240501(
		fig, 
		xlabel_prop={"fontsize":14},
		ylabel_prop={"fontsize":14}
	)
	if len(fig_change_kw) > 0:
		_plt_change_figure_properties_20240501(
			fig, **fig_change_kw
		)
	
	fig.savefig(o, **{"dpi":300, "bbox_inches":"tight", **fig_save_kw})

@vt(
	description="Create sequence library layout plot",
	helps=dict(
		i="A dictionary or json that indicates the input files",
		o="Output plot file",
		plot_kw="Plot arguments",
		compose_kw="Figure panel compose arguments",
	)
	
)
@vc
def _plot_sequence_library_layouts_20241022(i:str, o:str, plot_kw:str={}, compose_kw={}):
	import matplotlib.pyplot as plt
	from .utils.common import _read_json_like_struct_20240601	
	from biodataplot.sequence import _plot_fastq_layout_20230105
	from biodataplot.utils import _compose_SVG_panel_20241022
	data = _read_json_like_struct_20240601(i)
	plot_kw = _read_json_like_struct_20240601(plot_kw)
	compose_kw = _read_json_like_struct_20240601(compose_kw)
	cols = max(len(v) for v in data.values())
	data = {k : v + [None] * (cols - len(v)) for k, v in data.items()}
	figs = [None if f is None else _plot_fastq_layout_20230105(f, title=k + f"_R{idx+1}", **plot_kw) for k, v in data.items() for idx, f in enumerate(v)]
	plt.close('all')
	return _compose_SVG_panel_20241022(figs, output=o, **{"w":2000, "cols":cols, **compose_kw})
if __name__ == "__main__":
	main()



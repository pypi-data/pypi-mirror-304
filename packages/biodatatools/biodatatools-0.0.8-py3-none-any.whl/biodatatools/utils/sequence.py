# All sequences are represented in either str, FASTA or FASTQ

import sys
import simplevc
simplevc.register(sys.modules[__name__])

import itertools
from mphelper import ProcessWrapPool
from commonhelper import cluster_by_linkages
from biodata.fasta import FASTQ, FASTA
from collections import defaultdict
from commonhelper import distribute_items_evenly


_REVERSE_COMPLEMENT_MAP = {
"A":"T",
"G":"C",
"C":"G",
"T":"A",
"Y":"R",
"R":"Y",
"W":"W",
"S":"S",
"K":"M",
"M":"K",
"D":"H",
"V":"B",
"H":"D",
"B":"V",
"X":"X",
"N":"N",
"a":"t",
"g":"c",
"c":"g",
"t":"a",
"y":"r",
"r":"y",
"w":"w",
"s":"s",
"k":"m",
"m":"k",
"d":"h",
"v":"b",
"h":"d",
"b":"v",
"x":"x",
"n":"n",
"-":"-"
}
@vc
def _reverse_complement_20200726(s):
	'''
	Performs reverse complement on the sequence
	
	:param s: Input sequence
	:type s: str
	:return: The reverse complement of the sequence
	:rtype: str
	
	:Example:

	.. code-block:: python
		
		reverse_complement("ATC")
		# 'GAT'
		
		reverse_complement("atNG")
		# 'CNat'
	
	
	'''
	return "".join([_REVERSE_COMPLEMENT_MAP[c] for c in s][::-1])

@vc
def _read_seq_dict_20211020(i, case_conversion=None):
	from biodata.fasta import FASTAReader
	with FASTAReader(i) as fr:
		if case_conversion is None:
			return {f.name:f.seq for f in fr}
		elif isinstance(case_conversion, str):
			if case_conversion == "upper":
				return {f.name:f.seq.upper() for f in fr}
			elif case_conversion == "lower":
				return {f.name:f.seq.lower() for f in fr}
			else:
				raise Exception()
		else:
			return {f.name:case_conversion(f.seq) for f in fr}
@vc
def _reverse_complement_seq_dict_20211004(seq_dict):
	return {n:_reverse_complement_20200726(seq) for n, seq in seq_dict.items()}

@vc
def _get_edit_distance_20230120(
		ref, 
		query, 
		max_edit_distance=None, 
		direction=1, 
		rindex=None, 
		qindex=None, 
		rpenalty=False, 
		qpenalty=False, 
		allow_indel=True, 
		ambig_dict=None
	):
	'''
	Consider a query and ref, find the edit distance between them
	'''
	def match(r, q):
		if ambig_dict is None:
			return r == q
		else:
			if r in ambig_dict: r = ambig_dict[r]
			if q in ambig_dict: q = ambig_dict[q]
			return not set(r).isdisjoint(q)
	if qindex is None: qindex = (0 if direction == 1 else (len(query) - 1));
	if rindex is None: rindex = (0 if direction == 1 else (len(ref) - 1));
	if max_edit_distance is None: max_edit_distance = max(len(ref), len(query));
	if rindex > len(ref) or qindex > len(query):
		print(ref, query, rindex, qindex, len(ref), len(query))
		raise Exception()
	while 0 <= qindex < len(query) and 0 <= rindex < len(ref):
		if match(ref[rindex], query[qindex]):
			rindex += direction
			qindex += direction
		else:
			if max_edit_distance > 0:
				if allow_indel:
					results = (_get_edit_distance_20230120(ref, query, max_edit_distance - 1, direction, rindex + direction, qindex + direction, rpenalty, qpenalty, allow_indel),
							   _get_edit_distance_20230120(ref, query, max_edit_distance - 1, direction, rindex,             qindex + direction, rpenalty, qpenalty, allow_indel),
							   _get_edit_distance_20230120(ref, query, max_edit_distance - 1, direction, rindex + direction, qindex            , rpenalty, qpenalty, allow_indel))
				else:
					results = [_get_edit_distance_20230120(ref, query, max_edit_distance - 1, direction, rindex + direction, qindex + direction, rpenalty, qpenalty, allow_indel)]
				return min(results) + 1
			else:
				return 1
	penalty = 0
	if rpenalty: penalty += (len(ref)   - rindex) if direction == 1 else (rindex - -1);
	if qpenalty: penalty += (len(query) - qindex) if direction == 1 else (qindex - -1);
	return penalty

@vc
def _process_sequencing_read_20240624(read, layout, max_edit_distance=1, min_last_anchor_match=1):
	'''
	Process a read that has a layout:
	NNN...NN ANCHORSEQ1 NNN...NN ANCHORSEQ2 NNN...NN ...
	
	Output a list of non-anchor sequences (NNN...NNs).
	
	If an achorseq is at the last block, we do not require a full-length anchorseq to be mapped. 
	If the layout has NNN...NN with no fixed length as the last segment, mark the length as -1. 
	
	:param layout: A list of objects that describes the read layout. For NNN...NNs, either an int or a list of int is accepted. For anchor sequence, a string is accepted.
	
	'''
	def compile_temp_ints(temp_ints):
		left_splits = []
		right_splits = []
		final_ints = None 
		if any(l == -1 for l in temp_ints):
			final_ints = -1
			idx = temp_ints.index(-1)
			for i in range(0, idx):
				l = temp_ints[i]
				if isinstance(l, int):
					left_splits.append(l)
				elif len(l) == 1:
					left_splits.append(l[0])
				else:
					raise Exception()
			for i in range(idx+1, len(temp_ints)):
				l = temp_ints[i]
				if isinstance(l, int):
					right_splits.append(l)
				elif len(l) == 1:
					right_splits.append(l[0])
				else:
					raise Exception()
		else:
			idx = None
			for i, l in enumerate(temp_ints):
				if not isinstance(l, int) and len(l) > 1:
					idx = i 
					break
			if idx is not None:
				for i in range(0, idx):
					l = temp_ints[i]
					if isinstance(l, int):
						left_splits.append(l)
					elif len(l) == 1:
						left_splits.append(l[0])
					else:
						raise Exception()
				for i in range(idx+1, len(temp_ints)):
					l = temp_ints[i]
					if isinstance(l, int):
						right_splits.append(l)
					elif len(l) == 1:
						right_splits.append(l[0])
					else:
						raise Exception()
				s = sum(left_splits) + sum(right_splits)
				final_ints = [r + s for r in temp_ints[idx]]
			else:
				for l in temp_ints:
					if isinstance(l, int):
						left_splits.append(l)
					elif len(l) == 1:
						left_splits.append(l[0])
					else:
						raise Exception()
				final_ints = [sum(left_splits)]
				right_splits = None
		return final_ints, left_splits, right_splits
	def split_seqs(s, left_splits, right_splits):
		left_seqs = []
		right_seqs = []
		for l in left_splits:
			left_seqs.append(s[:l])
			s = s[l:]
		if right_splits is None:
			return left_seqs
		else:
			for l in right_splits[::-1]:
				right_seqs.append(s[l:])
				s = s[:l]
			return left_seqs + [s] + right_seqs[::-1]
	if isinstance(read, str):
		name = None
		seq = read
		quality = None
	elif isinstance(read, FASTQ):
		name = read.name
		seq = read.seq
		quality = read.quality
	elif isinstance(read, FASTA):
		name = read.name
		seq = read.seq
		quality = None
	else:
		raise Exception("Unknown type")
	layout_idx = 0
	start_index = 0
	output_seqs = []
	output_qualities = []
	
	compiled_splits = {}
	compiled_layout = []
	temp_ints = []
	for l in layout:
		if isinstance(l, str):
			if len(temp_ints) > 0:
				final_ints, left_splits, right_splits = compile_temp_ints(temp_ints)
				compiled_layout.append(final_ints)
				compiled_splits[len(compiled_layout) - 1] = (left_splits, right_splits)
				temp_ints = []
			compiled_layout.append(l)
		else:
			temp_ints.append(l)
	if len(temp_ints) > 0:
		final_ints, left_splits, right_splits = compile_temp_ints(temp_ints)
		compiled_layout.append(final_ints)
		compiled_splits[len(compiled_layout) - 1] = (left_splits, right_splits)
	layout = compiled_layout
	while len(layout) > layout_idx:
		l = layout[layout_idx]
		layout_idx += 1
		if not isinstance(l, str): # If this is an int instance
			left_splits, right_splits = compiled_splits[layout_idx - 1]
			if layout_idx == len(layout): # If this is the last instance
				if l == -1:
					# The last NNNs can have any lengths
					output_seqs.extend(split_seqs(seq[start_index:], left_splits, right_splits))
					if quality is not None:
						output_qualities.extend(split_seqs(quality[start_index:], left_splits, right_splits))
				else:
					if isinstance(l, int):
						l = [l]
					if len(l) != 1:
						raise Exception()
					if len(seq) - start_index < l[0]:
						return None
					output_seqs.extend(split_seqs(seq[start_index:start_index + l[0]], left_splits, right_splits))
# 					if len(seq) - start_index not in l:
# 						return None
# 					output_seqs.extend(split_seqs(seq[start_index:], left_splits, right_splits))
					if quality is not None:
						output_qualities.extend(split_seqs(quality[start_index:start_index + l[0]], left_splits, right_splits))
			else:
				if isinstance(l, int): # Wrap, if user provides an int, wrap it into a list
					if l == -1:
						l = list(range(len(seq) - start_index))
					else:
						l = [l]
				rindice = [i + start_index for i in l]
				
				l = layout[layout_idx]
				layout_idx += 1
				if not isinstance(l, str):
					raise Exception()
				anchorseq = l
				is_last_anchorseq = layout_idx == len(layout)
					
				if is_last_anchorseq:
					# If it is the last anchor seq, then allow seq matching only partial anchorseq
					rindice = [ri for ri in rindice if len(seq) - ri >= min_last_anchor_match]
					rstart_mismatch_dict = {n:_get_edit_distance_20230120(seq, anchorseq, max_edit_distance, 1, rindex=n, qpenalty=False, rpenalty=False, allow_indel=False) for n in rindice}
# 					rstart_mismatch_dict = {n:_get_edit_distance_20230120(seq, anchorseq, max_edit_distance, 1, rindex=n, qpenalty=False, rpenalty=True, allow_indel=False) for n in rindice}
				else:
					rstart_mismatch_dict = {n:_get_edit_distance_20230120(seq, anchorseq, max_edit_distance, 1, rindex=n, qpenalty=True, rpenalty=False, allow_indel=False) for n in rindice if n < len(seq)}
				if len(rstart_mismatch_dict) == 0:
					return None
				best_backbone_start = min(rstart_mismatch_dict.keys(), key=lambda i: rstart_mismatch_dict[i])
				if rstart_mismatch_dict[best_backbone_start] > max_edit_distance:
					return None
				output_seqs.extend(split_seqs(seq[start_index:best_backbone_start], left_splits, right_splits))
				if quality is not None:
					output_qualities.extend(split_seqs(quality[start_index:best_backbone_start], left_splits, right_splits))
				start_index = best_backbone_start + len(anchorseq)
		else:
			# A string to represent anchor seq
			rindice = [start_index]
			anchorseq = l
			is_last_anchorseq = layout_idx == len(layout)
			if is_last_anchorseq:
				# If it is the last anchor seq, then allow seq matching only partial anchorseq
				rindice = [ri for ri in rindice if len(seq) - ri >= min_last_anchor_match]
				rstart_mismatch_dict = {n:_get_edit_distance_20230120(seq, anchorseq, max_edit_distance, 1, rindex=n, qpenalty=False, rpenalty=True, allow_indel=False) for n in rindice} 
			else:
				rstart_mismatch_dict = {n:_get_edit_distance_20230120(seq, anchorseq, max_edit_distance, 1, rindex=n, qpenalty=True, rpenalty=False, allow_indel=False) for n in rindice}
			if len(rstart_mismatch_dict) == 0:
				return None
			best_backbone_start = min(rstart_mismatch_dict.keys(), key=lambda i: rstart_mismatch_dict[i])
			if rstart_mismatch_dict[best_backbone_start] > max_edit_distance:
				return None
			start_index = best_backbone_start + len(anchorseq)
			
	if name is None:
		return output_seqs
	elif quality is None:
		return [FASTA(name, s) for s in output_seqs]
	else:
		return [FASTQ(name, s, q) for s, q in zip(output_seqs, output_qualities)]
	
	
def _process_sequencing_reads_20240624(
		f1, layout1,
		f2=None, layout2=None, 
		max_edit_distance=1, 
		min_last_anchor_match=1, 
		keep_unmatch=False,
		nthread=1,
		reads_per_thread=1000000
	):
	
	def _dummy_wrapper_single(reads, layout, max_edit_distance, keep_unmatch):
		ncols = len(layout) - sum(isinstance(layout_item, str) for layout_item in layout)
		results = []
		for read in reads:
			result = _process_sequencing_read_20240624(read, layout, max_edit_distance, min_last_anchor_match=min_last_anchor_match)
			if result is not None:
				results.append(result)
			elif keep_unmatch:
				results.append(["_UNMATCH_" for _ in range(ncols)])
		return results
	def _dummy_wrapper_pairs(read_pairs, layout1, layout2, max_edit_distance, keep_unmatch):
		ncols = len(layout1) + len(layout2) - sum(isinstance(layout_item, str) for layout_item in itertools.chain(layout1, layout2))
		results = []
		
		for read1, read2 in read_pairs:
			result1 = _process_sequencing_read_20240624(read1, layout1, max_edit_distance, min_last_anchor_match=min_last_anchor_match)
			result2 = _process_sequencing_read_20240624(read2, layout2, max_edit_distance, min_last_anchor_match=min_last_anchor_match)
			if result1 is not None and result2 is not None:
				results.append(result1 + result2)
			elif keep_unmatch:
				results.append(["_UNMATCH_" for _ in range(ncols)])
		return results
	
	if f2 is None and layout2 is not None:
		raise Exception("You should not provide layout2 if you do not provide second reads")
	with ProcessWrapPool(nthread) as pwpool:
		x = 0
		if f2 is not None:
			read_pairs = []
			for r1, r2 in zip(f1, f2):
				read_pairs.append((r1, r2))
				x += 1
				if x % reads_per_thread == 0:
					pwpool.run(_dummy_wrapper_pairs, args=[read_pairs, layout1, layout2, max_edit_distance, keep_unmatch])
					read_pairs = []
			pwpool.run(_dummy_wrapper_pairs, args=[read_pairs, layout1, layout2, max_edit_distance, keep_unmatch])
		else:
			reads = []
			for r1 in f1:
				reads.append(r1)
				x += 1
				if x % reads_per_thread == 0:
					pwpool.run(_dummy_wrapper_single, args=[reads, layout1, max_edit_distance, keep_unmatch])
					reads = []
			pwpool.run(_dummy_wrapper_single, args=[reads, layout1, max_edit_distance, keep_unmatch])
			
		results = pwpool.get(wait=True).values()
	if not pwpool.check_successful_completion():
		raise Exception("Pool fails.")
	return list(itertools.chain.from_iterable(results))	
@vc
def _cluster_sequences_20240710(seqs, max_edit_distance=1, mode="connected", nthread=1):
	# Stranded
	# Return a tuple of two: clustered sequences in dict 
	useqs = set(seqs)
	sorted_useqs = sorted(useqs)
	if mode == "unique" or (mode == "connected" and max_edit_distance == 0):
		return list(range(len(sorted_useqs))), sorted_useqs#, [d[seq] for seq in seqs]
	elif mode == "connected":
		if max_edit_distance > 1:
			raise Exception("Currently unsupported")
		linkages = []
		
		for seq in useqs:
			linkages.append((seq, seq))
		# Build seed pool
		k = min(len(seq) for seq in useqs) // 2 
		seq_seed_pool = defaultdict(set)
		for seq in seqs:
			for i in range(len(seq) - k + 1):
				seq_seed_pool[seq[i:i+k]].add(seq)
	
		def _dummy_wrapper(seq_seed_pool, seqs, max_edit_distance):
			linkages = []
			for seq in seqs:
				seeded_seqs = set()
				for i in range(len(seq) - k + 1):
					seeded_seqs.update(seq_seed_pool[seq[i:i+k]])
				for match_seq in seeded_seqs:
					if match_seq == seq:
						continue
					if _get_edit_distance_20230120(seq, match_seq, max_edit_distance, rpenalty=True, qpenalty=True) <= max_edit_distance:
						linkages.append((seq, match_seq))
			return linkages
		if nthread == 1:
			processed_linkages = _dummy_wrapper(seq_seed_pool, seqs, max_edit_distance)
		else:
			pwpool = ProcessWrapPool(nthread)
			# Linkages between different seqs
			for i, j in distribute_items_evenly(len(seqs), min(len(seqs), nthread)):
				pwpool.run(_dummy_wrapper, args=(seq_seed_pool, seqs[i:j], max_edit_distance))
			processed_linkages = list(itertools.chain.from_iterable(pwpool.get(wait=True).values()))
			pwpool.close()
		linkages = linkages + processed_linkages
		c = cluster_by_linkages(linkages)
		idmap = {}
		next_id = 0
		final_cluster = {} 
		for k in sorted_useqs:
			v = c[k]
			if id(v) not in idmap:
				idmap[id(v)] = next_id
				next_id += 1
			final_cluster[k] = idmap[id(v)]
		return final_cluster			
	else:
		raise Exception("Unsupported")
	
@vc
def _trim_by_template_20240702(adapter_seq, seqs, direction, max_edit_distance=1, min_match_len=5, nthread=1):
	if nthread > 1:
		pwpool = ProcessWrapPool(nthread)
		results_list_pids = []
		for (start, end) in distribute_items_evenly(len(seqs), nthread):
			results_list_pids.append(pwpool.run(_trim_by_template_20240702, args=[adapter_seq, seqs[start:end], direction, max_edit_distance, min_match_len, 1]))
		final_results = pwpool.get(wait=True).values()
		pwpool.close()
		if not pwpool.check_successful_completion():
			raise Exception("Pool fails.")
		return list(itertools.chain.from_iterable(final_results))
	else:
		new_seqs = []
		for seq in seqs:
			for rindex in range(len(seq) - min_match_len):
				if direction == 1:
					d = _get_edit_distance_20230120(seq, adapter_seq, max_edit_distance, direction, rindex, 0, rpenalty=False, qpenalty=False, allow_indel=False)
					if d <= max_edit_distance:
						new_seqs.append(seq[:rindex])
						break
				elif direction == -1:
					d = _get_edit_distance_20230120(seq, adapter_seq, max_edit_distance, direction, len(seq) - rindex - 1, len(adapter_seq) - 1, rpenalty=False, qpenalty=False, allow_indel=False)
					
					if d <= max_edit_distance:
						new_seqs.append(seq[len(seq) - rindex:])
						break
				else:
					raise Exception()
			else:
				new_seqs.append(seq)	
		return new_seqs
	
@vc	
def _get_align_candidates_20240702(ref_seqs, seqs, strand=0, direction=1, end_seq=None, max_edit_distance=1, min_match_len=16, qpenalty=True, nthread=1):
	if strand not in [1, 0, -1]:
		raise Exception()
	if direction not in [1, -1]:
		raise Exception()
	if nthread <= 0:
		raise Exception()
	
	if nthread > 1:
		pwpool = ProcessWrapPool(nthread)
		results_list_pids = []
		for (start, end) in distribute_items_evenly(len(seqs), nthread):
			results_list_pids.append(pwpool.run(_get_align_candidates_20240702, args=[ref_seqs, seqs[start:end], strand, direction, end_seq, max_edit_distance, min_match_len, qpenalty, 1]))
		final_results = pwpool.get(wait=True).values()
		pwpool.close()
		if not pwpool.check_successful_completion():
			raise Exception("Pool fails.")
		return list(itertools.chain.from_iterable(final_results))

	else:
		if max_edit_distance > 1:
			raise Exception("Currently max edit distance > 1 is not supported")
		if direction == -1:
			ref_seqs = {ref:seq[::-1] for ref, seq in ref_seqs.items()}
			
		fwd_ref_seqs = ref_seqs
		rev_ref_seqs = _reverse_complement_seq_dict_20211004(ref_seqs)
		seed_len = min_match_len // 2		
		seed_database = dict()
		for i in range(max(len(s) for s in ref_seqs.values()) - seed_len):
			for ref, seq in ref_seqs.items():
				if len(seq) < min_match_len:
					continue
				if i+seed_len <= len(seq):
					if not seq[i:i+seed_len] in seed_database:
						seed_database[seq[i:i+seed_len]] = []
					seed_database[seq[i:i+seed_len]].append((ref, 1, i))
		
		for i in range(max(len(s) for s in ref_seqs.values()) - seed_len):
			for ref, seq in rev_ref_seqs.items():
				if len(seq) < min_match_len:
					continue
				if i+seed_len <= len(seq):
					if not seq[i:i+seed_len] in seed_database:
						seed_database[seq[i:i+seed_len]] = []
					seed_database[seq[i:i+seed_len]].append((ref, -1, i))
					
		if end_seq is not None:
			fwd_ref_seqs = {ref: seq + end_seq for ref, seq in ref_seqs.items()}
			rev_ref_seqs = {ref: seq + end_seq for ref, seq in rev_ref_seqs.items()}
		results_list = []
		for seq in seqs:
			if direction == -1:
				seq = seq[::-1]
			candidates = set()
			if len(seq) >= min_match_len:
				for i in range(0, seed_len*3, seed_len):
					if i + seed_len > len(seq):
						continue
					if seq[i:i+seed_len] in seed_database:
						for candidate in seed_database[seq[i:i+seed_len]]:
							candidates.add(candidate)
			candidates = set([(ref, s, p+j) for ref, s, p in candidates for j in [-1, 0, 1] if p+j >=0 and (strand == 0 or s == strand)])
			if len(candidates) == 0:
				results = set()
			else:
				candidate_mismatch_dict = {(ref, s, p):_get_edit_distance_20230120((fwd_ref_seqs if s == 1 else rev_ref_seqs)[ref] , seq, max_edit_distance=max_edit_distance, direction=1, rindex=p, rpenalty=False, qpenalty=qpenalty, allow_indel=True) 
										   for ref, s, p in candidates}
				min_mismatch = min(candidate_mismatch_dict.values())
				if min_mismatch > max_edit_distance:
					results = set()
				else:
					results = set(k for k, v in candidate_mismatch_dict.items() if v == min_mismatch)
				if direction == -1:
					results = set((ref, s, len(ref_seqs[ref]) - p - 1) for ref, s, p in results)
				
			results_list.append(results)	
		return results_list
# Ref ACGGTGGCCCCGCGT
# RC Ref ACGCGGGGCCACCGT
# align_front_fwd:ACGGTGG  --> rc none, align
# align_front_rev:ACGCGG  --> rc seq_dict, align
# align_back_fwd:CCCGCGT   --> rc both, align
# align_back_rev:CCACCGT --> rc seq_dict+rc both=only rc read,  align
	
@vc
def _get_match_candidates_20240702(ref_seqs, seqs, strand, direction=1, end_seq=None, random_start=False, max_edit_distance=1, min_match_len=10, qpenalty=True, nthread=1):
	'''
	Here query is aligned to the reference sequences starting from position 1 at the same orientation
	'''
		
	if nthread > 1:
		pwpool = ProcessWrapPool(nthread)
		results_list_pids = []
		for (start, end) in distribute_items_evenly(len(seqs), nthread):
			results_list_pids.append(pwpool.run(_get_match_candidates_20240702, args=[ref_seqs, seqs[start:end], strand, direction, end_seq, random_start, max_edit_distance, min_match_len, qpenalty, 1]))
		final_results = pwpool.get(wait=True).values()
		pwpool.close()
		if not pwpool.check_successful_completion():
			raise Exception("Pool fails.")
		return list(itertools.chain.from_iterable(final_results))
	else:
		if random_start:
			tmp_results_list = _get_align_candidates_20240702(ref_seqs, seqs, strand, direction, end_seq, max_edit_distance, min_match_len, qpenalty, 1)
			return [set(ref for ref, strand, p in results) for results in tmp_results_list]
		else:
# 			if (direction == 1 and rc) or (direction == -1 and not rc):
# 				ref_seqs = _reverse_complement_seq_dict_20211004(ref_seqs)
			if direction == -1:
				ref_seqs = {ref:seq[::-1] for ref, seq in ref_seqs.items()}
			fwd_ref_seqs = ref_seqs
			rev_ref_seqs = _reverse_complement_seq_dict_20211004(ref_seqs)
			
			seed_database = dict()
			rev_seed_database = dict()
			if max_edit_distance > 1:
				raise Exception("Currently max edit distance > 1 is not supported")
			seed_len = min_match_len // 2
			for j1 in range(0, seed_len*3, seed_len):
				for j2 in [-1, 0, 1]:
					i = j1+j2
					if i < 0:
						continue
					d = dict()
					for ref, seq in fwd_ref_seqs.items():
						if len(seq) < min_match_len:
							continue
						if i+seed_len <= len(seq):
							if not seq[i:i+seed_len] in d:
								d[seq[i:i+seed_len]] = []
							d[seq[i:i+seed_len]].append(ref)
					seed_database[i] = d
			for j1 in range(0, seed_len*3, seed_len):
				for j2 in [-1, 0, 1]:
					i = j1+j2
					if i < 0:
						continue
					d = dict()
					for ref, seq in rev_ref_seqs.items():
						if len(seq) < min_match_len:
							continue
						if i+seed_len <= len(seq):
							if not seq[i:i+seed_len] in d:
								d[seq[i:i+seed_len]] = []
							d[seq[i:i+seed_len]].append(ref)
					rev_seed_database[i] = d
			if end_seq is not None:
				fwd_ref_seqs = {ref: seq + end_seq for ref, seq in fwd_ref_seqs.items()}
				rev_ref_seqs = {ref: seq + end_seq for ref, seq in rev_ref_seqs.items()}
			results_list = []
			for seq in seqs:
				if direction == -1:
					seq = seq[::-1]
				candidate_mismatch_dict = {}
				if strand in [0, 1]:
					candidates = set()
					if len(seq) >= min_match_len:
						for i in range(0, seed_len*3, seed_len):
							if i + seed_len > len(seq):
								continue
							for j2 in [-1, 0, 1]:
								if i+j2 not in seed_database:
									continue
								d = seed_database[i+j2]			
								if seq[i:i+seed_len] in d:
									for ref in d[seq[i:i+seed_len]]:
										candidates.add(ref)
					for k, v in {candidate:_get_edit_distance_20230120(fwd_ref_seqs[candidate], seq, max_edit_distance=max_edit_distance, direction=1, rpenalty=False, qpenalty=qpenalty, allow_indel=True) 
											   for candidate in candidates}.items():
						if k in candidate_mismatch_dict:
							candidate_mismatch_dict[k] = min(candidate_mismatch_dict[k], v)
						else:
							candidate_mismatch_dict[k] = v
				if strand in [0, -1]:
					candidates = set()
					if len(seq) >= min_match_len:
						for i in range(0, seed_len*3, seed_len):
							if i + seed_len > len(seq):
								continue
							for j2 in [-1, 0, 1]:
								if i+j2 not in rev_seed_database:
									continue
								d = rev_seed_database[i+j2]			
								if seq[i:i+seed_len] in d:
									for ref in d[seq[i:i+seed_len]]:
										candidates.add(ref)
					for k, v in {candidate:_get_edit_distance_20230120(rev_ref_seqs[candidate], seq, max_edit_distance=max_edit_distance, direction=1, rpenalty=False, qpenalty=qpenalty, allow_indel=True) 
											   for candidate in candidates}.items():
						if k in candidate_mismatch_dict:
							candidate_mismatch_dict[k] = min(candidate_mismatch_dict[k], v)
						else:
							candidate_mismatch_dict[k] = v
				if len(candidate_mismatch_dict) == 0:
					results = set()
				else:
					min_mismatch = min(candidate_mismatch_dict.values())
					if min_mismatch > max_edit_distance:
						results = set()
					else:
						results = set(k for k, v in candidate_mismatch_dict.items() if v == min_mismatch)
				results_list.append(results)
			return results_list


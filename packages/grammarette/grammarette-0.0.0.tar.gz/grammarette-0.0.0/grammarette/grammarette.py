import re
from collections import defaultdict
from itertools import product
import numpy as np
from .msa import multi_sequence_alignment


VOWELS = ['a','e','i','o','u','y']
CONSONANTS = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z']


class Grammarette:

	def __init__(self, lexicon, dims):
		self.dims = _validate_dims(dims)
		self.n_features = len(self.dims)
		self.lexicon = _validate_lexicon(lexicon, self.dims)
		self.signals = [signal for meaning, signal in lexicon.items()]
		self.meanings = [tuple(map(str, meaning)) for meaning, signal in lexicon.items()]
		self.lexicon_reverse = defaultdict(set)
		for meaning, signal in zip(self.meanings, self.signals):
			self.lexicon_reverse[signal].add(meaning)
		self.shortest_grammar = '|'.join([
			''.join(meaning) + signal for meaning, signal in zip(self.meanings, self.signals)
		])
		self.shortest_codelength = self._codelength(self.shortest_grammar)
		self.grammars = {self.shortest_grammar: self.shortest_codelength}
		self.alignment = self._align_signals()
		self.alignment_reverse = self._align_signals(reverse=True)
		self._find_shortest_grammar()
		self._regex = None
		self._regexc = None

	def __str__(self):
		return f'Grammarette[{self.shortest_grammar}]'

	def _align_signals(self, reverse=False):
		'''
		Produce an alignment of the signals. If reverse is True, the signals
		are first reversed and later unreversed to produce an alignment
		working from the end backwards.
		'''
		if reverse:
			sequences = [list(reversed(signal)) for signal in self.signals]
		else:
			sequences = [list(signal) for signal in self.signals]
		alignment = multi_sequence_alignment(sequences, scoring_fn=_letter_distance)
		# Since multi_sequence_alignment() doesn't retain the original
		# sequence order, we now need to put them back into order.
		signal_checklist = [''.join(sequence) for sequence in sequences]
		ordered_alignment = [None] * len(alignment)
		for aligned_signal in alignment:
			signal_i = signal_checklist.index(''.join(aligned_signal).replace('_', ''))
			signal_checklist[signal_i] = None
			if reverse:
				ordered_alignment[signal_i] = tuple(reversed(aligned_signal))
			else:
				ordered_alignment[signal_i] = aligned_signal
		return np.array(ordered_alignment, dtype=str)

	def _codelength(self, grammar):
		'''
		Calculate the codelength of a grammar string. This is given by

		  -sum( log[Pr(char)] for char in grammar )

		where Pr(char) is the probability of some character appearing in the
		grammar.
		'''
		unique_chars = set(grammar)
		grammar_length = len(grammar)
		char_codelengths = {char: np.log2(grammar.count(char) / grammar_length) for char in unique_chars}
		return -sum([char_codelengths[char] for char in grammar])

	def _produce_signal_for_meaning(self, grammar, target_meaning):
		'''
		Produce a signal for a target meaning according to a given grammar.
		'''
		signal = ''
		for rule in grammar.split('+'):
			for sub_rule in rule.split('|'):
				meaning = tuple(sub_rule[:self.n_features])
				form = sub_rule[self.n_features:]
				if all([m_val == t_val or m_val == '?' for m_val, t_val in zip(meaning, target_meaning)]):
					signal += form
					break
		return signal

	# def _infer_meanings_for_signal(self, grammar, target_signal):
	# 	# grammar = '00buvichoe|01buvikoh|02buvicow|03buvycow|10zeteekow|11zeteecoh|12zeticoe|13zeticoh|20gafeechow|21gafeekoe|22gafykoe|23gafychoe|30wopykow|31wopeecoe|32wopykoh|33wopikow'
	# 	# target_signal = 'buvikoh'
	# 	candidate_meanings = set(product(*[map(str, range(n_values)) for n_values in self.dims]))
	# 	for rule in grammar.split('+'):
	# 		for sub_rule in rule.split('|'):
	# 			meaning = sub_rule[:self.n_features]
	# 			form = sub_rule[self.n_features:]
	# 			if target_signal.startswith(form):
	# 				target_signal = target_signal[len(form):]
	# 				if '?' not in meaning:
	# 					candidate_meanings.add(tuple(meaning))
	# 				for feature_i, value in enumerate(meaning):
	# 					if value == '?':
	# 						continue
	# 					candidate_meanings = set(filter(lambda m: True if m[feature_i] == value else False, candidate_meanings))
	# 				break
	# 			else:
	# 				for feature_i, value in enumerate(meaning):
	# 					if value == '?':
	# 						continue
	# 					candidate_meanings = set(filter(lambda m: False if m[feature_i] == value else True, candidate_meanings))
	# 	# print(candidate_meanings)
	# 	# quit()
	# 	return candidate_meanings
	# 	return self.lexicon_reverse[target_signal]

	def _check_consistency(self, grammar):
		'''
		For each meaning–signal pair in the original input lexicon, check that
		the grammar produces the correct output signal.
		'''
		for meaning, expected_signal in zip(self.meanings, self.signals):
			produced_signal = self._produce_signal_for_meaning(grammar, meaning)
			if expected_signal != produced_signal:
				return False
		# for signal, expected_meanings in self.lexicon_reverse.items():
		# 	inferred_meanings = self._infer_meanings_for_signal(grammar, signal)
		# 	if set(inferred_meanings) != expected_meanings:
		# 		return False
		return True

	def _evaluate_grammar(self, grammar):
		'''
		If the grammar hasn't been observed before and is consistent with the
		input data, calculate its codelength, store it in self.grammars,
		and keep track of the shortest grammar observed so far.
		'''
		if grammar not in self.grammars:
			if self._check_consistency(grammar):
				codelength = self._codelength(grammar)
				self.grammars[grammar] = codelength
				if codelength < self.shortest_codelength:
					self.shortest_grammar = grammar
					self.shortest_codelength = codelength

	def _intersection(self, meanings):
		'''
		Given a list of meanings, return the intersection. If the meanings
		differ on only one feature, change that feature to the wildcard ?.
		For example, given [(2, 2), (2, 1)], return (2, ?).
		'''
		different_features = []
		for feature_i, values in enumerate(zip(*meanings)):
			if len(set(values)) > 1:
				different_features.append(feature_i)
		if len(different_features) == 1:
			intersection = list(meanings[0])
			intersection[different_features[0]] = '?'
			return tuple(intersection)
		return False

	def _reduce_meanings(self, chunk_meanings):
		'''
		Given a list of meanings, if, for feature i, all feature values are
		represented, reduce those feature values to the wildcard '?'. For
		example, given [(0, 1), (0, 2), (0, 3), (0, 4)], return [(0, ?)].
		'''
		reduction = []
		for feature_i, n_values in enumerate(self.dims):
			values_for_feature_i = set([meaning[feature_i] for meaning in chunk_meanings])
			if len(values_for_feature_i) == n_values:
				values_for_feature_i = ['?']
			reduction.append(values_for_feature_i)
		reduced_meanings = []
		for meaning in product(*reduction):
			if '?' in meaning or meaning in chunk_meanings:
				reduced_meanings.append(meaning)
		return reduced_meanings

	def _write_grammar(self, alignment, chunk_boundaries, reduce_sub_grammar=False):
		'''
		Given an alignment of the signals and boundaries for carving up the
		alignment, write a grammar. Within each chunk boundary, get a list
		of the chunks that occur. For each unique chunk, make a list of
		all the meanings it occurs alongside (and reduce that set of
		meanings, if possible). If reduce_sub_grammar is True, in cases
		where a particular unique chunk maps to multiple meanings, try to
		reduce those meanings further by taking their intersection.
		Finally, join the grammar into a string and evaluate it.
		'''
		grammar = []
		for start, end in chunk_boundaries:
			chunks = [''.join(chunk).replace('_', '') for chunk in alignment[:, start:end]]
			chunk_to_meanings = {}
			for unique_chunk in set(chunks):
				if len(unique_chunk) == 0:
					continue
				chunk_to_meanings[unique_chunk] = self._reduce_meanings(
					[self.meanings[i] for i, chunk in enumerate(chunks) if chunk == unique_chunk]
				)
			sub_grammar = []
			for chunk, meanings in chunk_to_meanings.items():
				if reduce_sub_grammar and len(meanings) > 1:
					if (intersection := self._intersection(meanings)) is not False:
						sub_grammar.append(''.join(intersection) + chunk)
						continue
				for meaning in meanings:
					sub_grammar.append(''.join(meaning) + chunk)
			# sub_grammar.sort()
			# grammar.append('|'.join(sorted(sub_grammar, key=lambda x: len(x), reverse=True)))
			grammar.append('|'.join(sorted(sub_grammar)))
		grammar = '+'.join(grammar)
		self._evaluate_grammar(grammar)

	def _find_shortest_grammar(self):
		'''
		For each of the two alignments (forward and reverse), iterate over all
		possible chunk boundaries (partitions of the alignment columns)
		and write a grammar for each chunking of the lexicon.
		'''
		for alignment in [self.alignment, self.alignment_reverse]:
			for chunk_boundaries in _iter_partition_boundaries(len(alignment[0])):
				self._write_grammar(alignment, chunk_boundaries, reduce_sub_grammar=False)
				self._write_grammar(alignment, chunk_boundaries, reduce_sub_grammar=True)

	@property
	def grammar(self):
		return self.shortest_grammar

	@property
	def codelength(self):
		return self.shortest_codelength

	@property
	def regex(self):
		'''
		Return the induced grammar encoded as a regular expression. Meanings
		are encoded in the named groups (with _ representing the wildcard).
		'''
		if self._regex is None:
			self._regex = '^'
			for rule in self.shortest_grammar.split('+'):
				sub_rule_strings = []
				for sub_rule in rule.split('|'):
					meaning = sub_rule[:self.n_features]
					form = sub_rule[self.n_features:]
					meaning_id = f'{generate_random_group_name()}{meaning.replace("?", "_")}'
					sub_rule_strings.append(f'(?P<{meaning_id}>{form})')
				self._regex += '(' + '|'.join(sub_rule_strings) + ')?'
			self._regex += '$'
		return self._regex

	@property
	def regexc(self):
		'''
		Return the compiled regular expression.
		'''
		if self._regexc is None:
			self._regexc = re.compile(self.regex)
		return self._regexc

	def produce(self, meaning):
		'''
		Given a meaning, produce a signal according to the induced grammar.
		'''
		return self._produce_signal_for_meaning(self.grammar, tuple(map(str, meaning)))

	# def comprehend(self, signal):
	# 	return set([tuple(map(int, meaning)) for meaning in self._infer_meanings_for_signal(self.grammar, signal)])

	def comprehend(self, signal):
		'''
		Given a signal, return the possible meanings according to the induced
		grammar. To achieve this we first convert the induced grammar to a
		regular expression, match it against the signal, and infer the
		possible meanings from the named groups required to parse the signal.
		'''
		inferred_meaning = ['?'] * self.n_features
		for meaning_id, form in self.regexc.match(signal).groupdict().items():
			if form is not None:
				meaning_id = meaning_id[-self.n_features:]
				for feature_i, value in enumerate(meaning_id):
					if value != '_':
						inferred_meaning[feature_i] = value
		candidate_meanings = []
		for meaning in self.meanings:
			if all([m_val == i_val or i_val == '?' for m_val, i_val in zip(meaning, inferred_meaning)]):
				candidate_meanings.append(tuple(map(int, meaning)))
		return set(candidate_meanings)


def _letter_distance(a, b):
	'''
	Return the distance between two characters. If the characters are
	identical, return 0. If both characters belong to the same category
	(vowels or consonants), return 1. Otherwise, return 2.
	'''
	if a == b:
		return 0.0
	if a in VOWELS and b in VOWELS:
		return 1.0
	if a in CONSONANTS and b in CONSONANTS:
		return 1.0
	return 2.0


def _iter_partition_boundaries(n):
	'''
	Yield the boundaries needed to partition an object of size n in all ways.
	For example, an object of length 3, like ABC, can be partitioned in
	2^(n-1) = 4 ways: (ABC), (AB C), (A BC),(A B C).
	'''
	for cutpoints in range(1 << (n - 1)):
		result = []
		lastcut = 0
		for i in range(n - 1):
			if (1 << i) & cutpoints != 0:
				result.append((lastcut, i + 1))
				lastcut = i+1
		result.append((lastcut, n))
		yield tuple(result)


def _validate_lexicon(lexicon, dims):
	if not isinstance(lexicon, dict):
		raise TypeError(f'Lexicon should be of type dict, got {lexicon.__class__.__name__}')
	for meaning, signal in lexicon.items():
		if not isinstance(meaning, tuple):
			raise TypeError(f'Meanings should be of type tuple, got {meaning.__class__.__name__}')
		if not isinstance(signal, str):
			raise TypeError(f'Signals should be of type str, got {signal.__class__.__name__}')
		if len(meaning) != len(dims):
			raise ValueError(f'Meaning {meaning} does not match the dimensionality {dims}')
		for feature_value, n_features in zip(meaning, dims):
			if feature_value >= n_features:
				raise ValueError(f'Meaning {meaning} is not within the dimensionality {dims}')
	return lexicon


def _validate_dims(dims):
	if not isinstance(dims, tuple):
		raise TypeError(f'Dims should be of type tuple, got {dims.__class__.__name__}')
	if len(dims) == 0:
		raise ValueError('Dims should have at least one dimension')
	for n_features in dims:
		if not isinstance(n_features, int):
			raise TypeError(f'Dims should be tuple of ints, got tuple containing {n_features.__class__.__name__}')
	return dims


def generate_random_group_name():
	name = ''
	for _ in range(4):
		name += np.random.choice(CONSONANTS)
		name += np.random.choice(VOWELS)
	return name

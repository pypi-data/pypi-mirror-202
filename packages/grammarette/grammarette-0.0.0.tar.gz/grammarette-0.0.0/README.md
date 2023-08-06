Grammarette
===========

Grammarette is a lightweight grammar inducer for toy lexicons. Given a set of meaning–signal pairs (the lexicon), Grammarette produces a regex-like grammar that is as short as possible (in bits). This may be useful for analyzing the results of artificial language learning experiments, where the complexity of a lexicon may be quantified as the length of its shortest description. Grammarette is a work-in-progress and is not guaranteed to produce the shortest grammar. It uses [multiple sequence alignment](https://en.wikipedia.org/wiki/Multiple_sequence_alignment) to align the signals and then writes grammars for all $2^{n-1}$ possible ways of partitioning the alignment. The shortest grammar that remains consistent with the observed lexicon is the grammarette.


Installation
------------

Grammarette can be installed from the PyPI:

```bash
pip install grammarette
```

Grammarette has two dependencies, NumPy and SciPy, and is compatible with Python 3.8+.


Example
-------

```python
import grammarette

lexicon = {
    (0, 0): "buvikoe",
    (0, 1): "buvikoh",
    (0, 2): "buvikoe",
    (0, 3): "buvichoe",
    (1, 0): "zeteekoe",
    (1, 1): "zeteekoh",
    (1, 2): "zeteekoe",
    (1, 3): "zeteechoe",
    (2, 0): "gafykoe",
    (2, 1): "gafykoh",
    (2, 2): "gafykoe",
    (2, 3): "gaffychoe",
    (3, 0): "wopykoe",
    (3, 1): "wopykoh",
    (3, 2): "wopykoe",
    (3, 3): "wopychoe",
}

grmr = grammarette.induce(lexicon, dims=(4, 4))

print(grmr)
# Grammarette[0?buvi|1?zetee|23gaffy|2?gafy|3?wopy+?3ch|??k+?1oh|??oe]

print(grmr.grammar)
# 0?buvi|1?zetee|23gaffy|2?gafy|3?wopy+?3ch|??k+?1oh|??oe

print(grmr.codelength)
# 230.2261782820019

print(grmr.regex)
# ^((?P<kejeboxu0_>buvi)|(?P<hutusifo1_>zetee)|(?P<cedakesu23>gaffy)|(?P<coxycatu2_>gafy)|(?P<kusenewo3_>wopy))?((?P<byfipyxi_3>ch)|(?P<fujuvohy__>k))?((?P<nydepazy_1>oh)|(?P<wyvelesi__>oe))?$

print(grmr.produce( (2, 3) )) # use the induced grammar to produce a signal for meaning (2, 3)
# gaffychoe

print(grmr.comprehend( 'buvikoe' )) # use the induced grammar to infer meanings for "buvikoe"
# [(0, 0), (0, 1), (0, 2), (0, 3)] # this is currently incorrect, should be [(0, 0), (0, 2)]
```

Known issues
------------

- In some cases, a grammarette may not infer the correct set of meanings for a given input signal. This is partly an issue with the grammarette parser and partly an issue with the grammarette itself, which, in some cases, does not properly preserve all meaning information (the compression may be lossy).

- Grammarette is not well tested with more than two dimensions and may not perform well in such cases.

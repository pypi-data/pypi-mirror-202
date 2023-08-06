from . import grammarette as _grammarette

try:
    from ._version import __version__
except ImportError:
    __version__ = "???"


DEFAULT_DIMS = None


def set_default_dims(dims):
	global DEFAULT_DIMS
	DEFAULT_DIMS = _grammarette._validate_dims(dims)


def induce(lexicon, dims=None):
	if dims is None:
		dims = DEFAULT_DIMS
	return _grammarette.Grammarette(lexicon, dims)

import functools


def rsetattr(obj, attr, val):
    """Wrapper for the setattr() function that handles nested strings.

    Parameters
    ----------
    obj
        The object from which the attribute is set
    attr
        The name of the attribute. Can be nested, e.g. 'aa.bb.cc'
    val
        The value to which the attribute is set

    Returns
    -------
        None
    """
    pre, _, post = attr.rpartition(".")
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def rgetattr(obj, attr, *args):
    """Wrapper for the getattr() function that handles nested strings.

    Parameters
    ----------
    obj
        The object from which the attribute is obtained
    attr
        The name of the attribute. Can be nested, e.g. 'aa.bb.cc'
    *args
        [default,] The default return if the attribute is not found. If not supplied, AttributeError can be
        raised

    Returns
    -------
    attribute
        The attribute or the default return when not the attribute is not found

    Raises
    ------
    AttributeError
        When the attribute does not exist and no default is supplied in the *args
    """

    def _getattr(subobj, subattr, *subargs):
        return getattr(subobj, subattr, *subargs)

    return functools.reduce(lambda x, y: _getattr(x, y, *args), [obj] + attr.split("."))

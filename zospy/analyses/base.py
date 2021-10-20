import copy
from collections.abc import MutableMapping


def _pprint(d, indent=0):
    """Pretty print an attribute dict.
    """
    items = []
    for key, value in sorted(d.items(), key=lambda x: str(x[0])):
        if isinstance(key, str):
            strkey = f"'{key}'"
        else:
            strkey = str(key)
        if isinstance(value, MutableMapping):
            items.append(" " * indent + strkey + ":")
            items.extend(_pprint(value, indent + 2))
        else:
            items.append(" " * indent + strkey + ": " + repr(value))
    return items


def _convert_dicttype(dictionary, newtype=dict, convert_nested=True, method='deepcopy'):
    """Packs a nested dictionary to a one-level dictionary with tuple keys.

    Parameters
    ----------
    dictionary: dict
        A dictionary or dictionary subtype, optionally with nested dictionaries
    newtype: type
        The new dictionary (sub)type
    convert_nested: bool
        Whether nested dictionaries should be converted as well. Defaults to True
    method: str
        The method used to copy values. One of 'deepcopy', 'copy' and 'assign'. Defaults to 'deepcopy'

    Returns
    -------
    object
        The converted dictionary type
    """
    ret = newtype()
    for key, value in dictionary.items():
        if convert_nested and isinstance(value, dict):
            ret[key] = _convert_dicttype(value, newtype=newtype, convert_nested=convert_nested, method=method)
        else:
            if method == 'deepcopy':
                ret[key] = copy.deepcopy(value)
            elif method == 'copy':
                ret[key] = copy.copy(value)
            elif method == 'assign':
                ret[key] = value
            else:
                raise ValueError()
    return ret


class AttrDict(dict):
    """Basically a dict with attribute access.

    Equal to scipy's OptimizeResult (https://github.com/scipy/scipy/blob/v1.6.3/scipy/optimize/optimize.py#L82-L138).
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):

        if self.keys():
            return '\n'.join(_pprint(self))
        else:
            return self.__class__.__name__ + "()"

    def __dir__(self):
        return list([key for key in self.keys() if str(key).isidentifier()]) + dir(dict)

    def to_dict(self, convert_nested=True, method='deepcopy'):
        """Converts the AttrDict to a standard dict.

        Parameters
        ----------
        convert_nested: bool
            Whether nested dictionaries should be converted as well. Defaults to True
        method: str
            The method used to copy values. One of 'deepcopy', 'copy' and 'assign'. Defaults to 'deepcopy'

        Returns
        -------
        dict
            The AttrDict as standard Dict
        """
        return _convert_dicttype(self, newtype=dict, convert_nested=convert_nested, method=method)

    @classmethod
    def from_dict(cls, dictionary, convert_nested=True, method='deepcopy'):
        """Creates and AttrDict from a standard dict.

        Parameters
        ----------
        dictionary: dict
            The dictionary that is to be converted
        convert_nested: bool
            Whether nested dictionaries should be converted as well. Defaults to True
        method: str
            The method used to copy values. One of 'deepcopy', 'copy' and 'assign'. Defaults to 'deepcopy'

        Returns
        -------
        AttrDict
            The converted AttrDict
        """
        return _convert_dicttype(dictionary, newtype=cls, convert_nested=convert_nested, method=method)


class AnalysisResult(AttrDict):
    def __init__(self, analysistype, data=None, settings=None, metadata=None, headerdata=None, messages=None, **kwargs):
        """A class designed to hold an OpticStudio analysis.

        The class is basically a dict with attribute level access. However, for an AnalysisResult, certain keys are
        often present and thus automatically set.

        Parameters
        ----------
        analysistype: str
            The type of analysis that has been performed. Will be assigned to AnalysisResult.AnalysisType (also
            available through AnalysisResult['AnalysisType'].
        data: Any, optional
            The analysis data, can be any of the native python datatypes, a pd.Series, pd.DataFrame, np.ndarray or
            AnalysisData. Will be assigned to AnalysisResult.Data (also available through AnalysisResult['Data'].
            Defaults to None.
        settings: pd.Series, optional
            The analysis settings. Will be assigned to AnalysisResult.Settings (also available through
            AnalysisResult['Settings']. Defaults to None.
        metadata: pd.Series, optional
            The analysis metadata. Will be assigned to AnalysisResult.MetaData (also available through
            AnalysisResult['MetaData']. Defaults to None.
        headerdata: list of str, optional
            The analysis headerdata. Will be assigned to AnalysisResult.HeaderData (also available through
            AnalysisResult['HeaderData']. Defaults to None.
        messages: pd.DataFrame, optional:
            The analysis messages. Will be assigned to AnalysisResult.Messages (also available through
            AnalysisResult['Messages']. Defaults to None.
        kwargs:
            Any supplied kwarg will be assigned as an attribute (also available as AnalysisResult[kwarg]. Note that
            'AnalysisType', 'Data', 'Settings' 'MetaData', 'HeaderData' and 'Messages' are not available to be set.


        Returns
        -------
        AnalysisResult:
            A dict with attribute-like access

        Raises
        ------
        SyntaxError:
            If any of the following kwargs is specified 'AnalysisType', 'Data', 'Settings' 'MetaData', 'HeaderData' or
            'Messages'. These are to be set through the default arguments.
        """
        super().__init__(AnalysisType=analysistype, Data=data, Settings=settings, MetaData=metadata,
                         HeaderData=headerdata, Messages=messages, **kwargs)

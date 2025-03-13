"""Constants for the ZOS-API.

Submodule used for package wide access to all ZOS api constants. Note that the constant-naming within this module breaks
pep, but is kept as such to be in-sync with the api documentation. Constants should in general be accessed through
'zospy.constants' (or 'zp.constants'). All constants are obtained dynamically from the api. Therefore, they are only
available after running the code stated under examples.

Examples
--------
>>> import zospy as zp
>>> zos = zp.ZOS()
>>> print(zp.constants.Analysis.AnalysisIDM.ImageSimulation)
"""

from __future__ import annotations

import itertools as _itertools
import logging as _logging
from operator import attrgetter
from types import SimpleNamespace as _SimpleNamespace
from typing import TypeVar

from zospy.api import _ZOSAPI  # noqa: TCH001
from zospy.api._ZOSAPI_constants import *  # noqa
from zospy.utils import clrutils as _clrutils
from zospy.utils import pyutils as _pyutils

_logger = _logging.getLogger(__name__)


# Note: the above imports (and all but one function) are named private, to increase clarity on which Module components
# are constants and which are not.


def _itertools_joinfunc(*args):
    return ".".join(args)


def _construct_from_zosapi_and_enumkeys(zosapi: _ZOSAPI, zosapi_enumkeys: list[str]):
    """Construct the constants from `zosapi` and `zosapi_enumkeys`.

    The acquired constants are added to the zospy.constants namespace

    Parameters
    ----------
    zosapi : ZOSAPI
        A ZOSAPI instance.
    zosapi_enumkeys : list[str]
        The enumeration keys obtained from can be obtained through zp.utils.clrutils.reflect_dll_content()

    Returns
    -------
    None
    """
    zosapi_enumkeys = sorted(zosapi_enumkeys)
    added_namespaces = set()
    for enumkey in zosapi_enumkeys:
        subkeys = enumkey.split(".")

        if len(subkeys) <= 1:  # should at least be 2
            _logger.warning(f"Invalid enumkey {enumkey}.")
            raise ValueError(f"Invalid enumkey {enumkey}.")

        if len(subkeys) == 2:  # No nesting
            clrattr = getattr(zosapi, subkeys[-1], None)

            # Set constant
            globals()[subkeys[-1]] = _clrutils.system_enum_to_namedtuple(clrattr)

        else:  # with nesting
            base = subkeys[1]
            nsp_parts = list(_itertools.accumulate(subkeys[2:-1], func=_itertools_joinfunc))

            if base not in added_namespaces:
                globals()[base] = _SimpleNamespace()  # Create the base as SimpleNamespace
                added_namespaces.add(base)
            for nsp in nsp_parts:
                if f"{base}.{nsp}" in added_namespaces:  # check if already added
                    continue
                _pyutils.attrsetter(globals()[base], nsp, _SimpleNamespace())  # add nested objects
                added_namespaces.add(f"{base}.{nsp}")

            clrattr = attrgetter(".".join(subkeys[1:]))(zosapi)

            # set constants
            _pyutils.attrsetter(globals()[base], ".".join(subkeys[2:]), _clrutils.system_enum_to_namedtuple(clrattr))


Constant = TypeVar("Constant")


def process_constant(constant: type[Constant], value: Constant | str | None) -> Constant:
    """Get member `value` from `constant`.

    `value` can be a constant, a string representing the constant, or None. If `value` is a string, the constant with
    the same name is returned. If `value` is None, the constant `None_` is returned.

    Parameters
    ----------
    constant : type[Constant]
        The type of the constant to be processed.
    value : Constant | str | None
        The value to be processed. Can be a constant, a string representing the constant, or None.

    Returns
    -------
    Constant
        The processed constant value.

    Raises
    ------
    ValueError
        If the value does not match any attribute of the constant type.
    """
    if (value is None or value == "None") and hasattr(constant, "None_"):
        return constant.None_
    if isinstance(value, str) and hasattr(constant, value):
        return getattr(constant, value)
    if value in constant:
        return value

    raise ValueError(f"Constant {type(constant).__name__} does not contain value {value!s}")


def get_constantname_by_value(constant_tuple, value):
    """Obtain a constant name from a value.

    Parameters
    ----------
    constant_tuple : tuple
        The set of constants used to look up the value
    value : int
        The value for which the constant name is to be found

    Returns
    -------
    str
        The constant name
    """
    try:
        if isinstance(value, int):
            return constant_tuple._fields[value]

        return constant_tuple._fields[constant_tuple.index(value)]
    except KeyError as e:
        raise ValueError(f"None of the constants has value {value} assigned") from e

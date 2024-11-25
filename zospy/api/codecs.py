"""Custom object conversions between the CLR and Python.

Python.NET allows to customize the conversion of objects between the Common Language Runtime (CLR) and Python using
Codecs [1]. This module implements codecs for automatic conversions for certain ZOS-API objects.

References
----------
.. [1] Codecs. https://pythonnet.github.io/pythonnet/codecs.html
"""

from __future__ import annotations

import logging

import clr  # noqa
import Python.Runtime
import Python.Runtime.Codecs as Codecs  # noqa

logger = logging.getLogger(__name__)


class OpticStudioInterfaceEncoder(Codecs.RawProxyEncoder):
    """Automatic downcasting of generic interfaces to specific interfaces.

    Some parts of the ZOS-API return a generic interface where a specific implementation is needed. For example,
    the settings object for an analysis can be accessed using `ZOSAPI.Analysis.IA_.GetSettings`, but the returned
    object does not give access to analysis-specific settings. In order to access these settings, the specific
    implementation needs to be used. Python.NET makes this implementation available under the `__implementation__`
    attribute. This encoder automatically downcasts certain objects to their specific implementation.

    More information about this problem is available on the `OpticStudio forum
    <https://community.zemax.com/zos-api-12/pythonnet-3-x-is-fixed-3945?tid=3945&fid=12>`.

    Only a limited number of interfaces is automatically downcast. These are documented at
    https://zospy.readthedocs.io/codecs. It is possible to register additional interfaces with
    `OpticStudioInterfaceEncoder.register_interfaces`. This should ideally be done before loading the ZOS-API with
    `zospy.zpcore.ZOS`, and in any case before the interface is used for the first time.
    """

    # The encoder will not be registered if no namespace is present
    __namespace__ = "ZOSPy.API.Codecs"

    # Types that are downcast by this encoder
    _interfaces = frozenset(
        (
            "ZOSAPI.Analysis.Settings.IAS_",
            "ZOSAPI.Editors.LDE.ISurface",
            "ZOSAPI.Editors.LDE.ISurfaceApertureType",
            "ZOSAPI.Editors.LDE.ISurfaceScatteringType",
            "ZOSAPI.Editors.NCE.IObject",
            "ZOSAPI.Tools.ISystemTool",
        )
    )

    def CanEncode(self, clr_type) -> bool:  # noqa: N802
        """Check if `clr_type` should be encoded.

        An object can be encoded if it is an interface and its full name is present in
        `OpticStudioInterfaceEncoder._interfaces`.
        """
        if clr_type.IsInterface and clr_type.FullName in self._interfaces:
            logger.debug("%s can be encoded by OpticStudioInterfaceEncoder", clr_type.FullName)
            return True

        logger.debug("%s cannot be encoded by OpticStudioInterfaceEncoder", clr_type.FullName)
        return False

    def TryEncode(self, obj):  # noqa: N802
        """Try to downcast `obj` to its implementation."""
        logger.debug("Converting %s to its implementation", obj.GetType().FullName)
        return obj.__implementation__

    @classmethod
    def register_interfaces(cls, new_interfaces: list[str] | str) -> None:
        """Register new interfaces for automatic downcasting.

        Interfaces should be registered before initializing the ZOS-API.

        Parameters
        ----------
        new_interfaces : list[str] | str
            Full interface name or list of full interface names to register.

        Examples
        --------
        >>> import zospy.api.codecs as codecs
        >>> codecs.OpticStudioInterfaceEncoder.register_interfaces(
        ...     "ZOSAPI.Editors.NCE.ISourceColorSettings"
        ... )
        """
        if isinstance(new_interfaces, str):
            new_interfaces = [new_interfaces]

        cls._interfaces |= set(new_interfaces)


def try_register_encoder(encoder: type[Python.Runtime.IPyObjectEncoder]) -> None:
    """Register `encoder` as Python.NET codec.

    Parameters
    ----------
    encoder : Type[Python.Runtime.IPyObjectEncoder]
        A class implementing `Python.Runtime.IPyObjectEncoder`. The most viable way to do this from Python is
        creating a subclass of `Python.Runtime.Codecs.RawProxyEncoder`.

    Raises
    ------
    TypeError
        If the encoder cannot be registered because it is not of the correct type.
    """
    try:
        Python.Runtime.PyObjectConversions.RegisterEncoder(encoder())
        logger.debug("Registered encoder: %s", encoder.__name__)
    except TypeError as e:
        message = f"Could not register encoder {encoder.__name__}."
        raise TypeError(message) from e


def register_codecs():
    """Register all custom codecs.

    This function should be called prior to loading the ZOS-API.
    """
    encoders = [OpticStudioInterfaceEncoder]

    for encoder in encoders:
        try_register_encoder(encoder)

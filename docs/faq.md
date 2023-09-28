# Frequently Asked Questions

(faq/disconnect)=
## How do I disconnect from OpticStudio?

You can disconnect from OpticStudio using `zos.Application.CloseApplication`:

```{code} python
:emphasize-lines: 8, 9
import zospy as zp

zos = zp.ZOS()
oss = zos.connect_as_extension()

# Do work ...

# Disconnect
zos.Application.CloseApplication()
```

If you connect in extension mode, this will close the connection, but keep OpticStudio open.
If you connect in standalone mode, this will stop the standalone OpticStudio instance.
At the end of a script, it is not necessary to disconnect; this is handled automatically when Python terminates.

(faq/reconnect)=
## How do I reconnect to OpticStudio?

You can do this by first [disconnecting](faq/disconnect), then creating a new connection to OpticStudio.
Please note that it is not necessary to create a new instance of [`ZOS`](zospy.zpcore.ZOS). Doing so will 
raise an error, since [only a single ZOS instance is allowed](faq/single-zos-instance).

For example, this will not work:

```{code} python
:emphasize-lines: 11, 12
import zospy as zp

zos = zp.ZOS()
oss = zos.connect_as_extension()

# Do work ...

# Disconnect
zos.Application.CloseApplication()

# Try to create a second connection to the ZOS-API
zos = zp.ZOS()  # ValueError: Cannot have more than one active ZOS instance

oss = zos.connect_as_extension()
```

But this does work:

```{code} python
:emphasize-lines: 11, 12
import zospy as zp

zos = zp.ZOS()
oss = zos.connect_as_extension()

# Do work ...

# Disconnect
zos.Application.CloseApplication()

# Create a new connection
oss = zos.connect_as_extension()
```

(faq/single-zos-instance)=
{#single-zos-instance}
## Why do I get a `ValueError: Cannot have more than one active ZOS instance`?

This error will be raised when creating a new instance of [`ZOS`](zospy.zpcore.ZOS), 
if another instance has been created before. The ZOS-API only supports a single connection per process, and this is
reflected in ZOSPy by allowing only a single instance of the [`ZOS`](zospy.zpcore.ZOS) class.

The [`ZOS`](zospy.zpcore.ZOS) class manages the ZOS-API connection. Closing the connection to OpticStudio 
does not close the connection with the ZOS-API. You therefore only need a single instance of this class. This instance 
can be re-used, for example, if you try to [reconnect to OpticStudio](faq/reconnect).

:::{dropdown} Why doesn't the OpticStudio boilerplate code raise this error?
The OpticStudio boilerplate code suggests that it is possible to create a second ZOS-API connection, but this is not 
really the case. If you try to create a second connection, the `ZOSAPI_NetHelper` will not create a second connection,
but silently return a reference to the existing connection instead. This may lead to errors (e.g. because you assume 
you created a second connection to an empty OpticStudio instance), which is why we chose to raise an error instead of 
silently returning the existing `ZOS` instance.
:::

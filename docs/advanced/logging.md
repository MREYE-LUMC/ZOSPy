# Logging

Some basic logging is implemented through the standard Python [logging](https://docs.python.org/3/library/logging.html) module.

1. To enable logging output from all ZOSPy and other modules using logging.basicConfig:
    ```python
    import logging
       
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ```
2. To enable logging output from all ZOSPy and other modules using a root logger:
    ```python
    import logging
    
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    sh.setLevel(logging.DEBUG)
    
    logger = logging.getLogger()
    logger.addHandler(sh)
    ```
3. To enable logging output from only ZOSPy
    ```python
    import logging
    
    logging.getLogger('zospy').addHandler(logging.StreamHandler())
    logging.getLogger('zospy').setLevel(logging.INFO)
    ```
try:
    from ._dev import *
except:
    from .prod import *
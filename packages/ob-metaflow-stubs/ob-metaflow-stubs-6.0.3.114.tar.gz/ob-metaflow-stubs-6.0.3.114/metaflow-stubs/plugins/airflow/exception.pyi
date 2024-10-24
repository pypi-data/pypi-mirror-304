##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.26.1+obcheckpoint(0.1.1);ob(v1)                               #
# Generated on 2024-10-23T20:57:01.212332                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...


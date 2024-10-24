##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.26.1+obcheckpoint(0.1.1);ob(v1)                               #
# Generated on 2024-10-23T20:57:01.181978                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.cards.card_modules.basic

class SerializationErrorComponent(metaflow.plugins.cards.card_modules.basic.ErrorComponent, metaclass=type):
    def __init__(self, component_name, error_message):
        ...
    ...

def render_safely(func):
    """
    This is a decorator that can be added to any `MetaflowCardComponent.render`
    The goal is to render subcomponents safely and ensure that they are JSON serializable.
    """
    ...


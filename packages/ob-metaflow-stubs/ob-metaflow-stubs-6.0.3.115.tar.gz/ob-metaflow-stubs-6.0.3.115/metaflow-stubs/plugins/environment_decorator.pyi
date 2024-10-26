##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27.1+obcheckpoint(0.1.1);ob(v1)                               #
# Generated on 2024-10-25T21:39:54.778545                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

class EnvironmentDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies environment variables to be set prior to the execution of a step.
    
    Parameters
    ----------
    vars : Dict[str, str], default {}
        Dictionary of environment variables to set.
    """
    def runtime_step_cli(self, cli_args, retry_count, max_user_code_retries, ubf_context):
        ...
    ...


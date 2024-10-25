##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.27                                                            #
# Generated on 2024-10-24T19:27:17.981371                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import abc
    import metaflow.plugins.secrets

class SecretsProvider(abc.ABC, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None) -> typing.Dict[str, str]:
        """
        Retrieve the secret from secrets backend, and return a dictionary of
        environment variables.
        """
        ...
    ...

class InlineSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Intended to be used for testing purposes only.
        """
        ...
    ...


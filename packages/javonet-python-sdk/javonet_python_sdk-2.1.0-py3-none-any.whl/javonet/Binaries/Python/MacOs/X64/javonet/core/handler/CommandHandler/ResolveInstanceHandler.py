from javonet.core.handler.CommandHandler.AbstractCommandHandler import *
from javonet.core.handler.ReferencesCache import ReferencesCache


class ResolveInstanceHandler(AbstractCommandHandler):
    def __init__(self):
        self._required_parameters_count = 1

    def process(self, command):
        try:
            if len(command.payload) != self._required_parameters_count:
                raise Exception("ResolveInstanceHandler parameters mismatch!")

            references_cache = ReferencesCache()
            return references_cache.resolve_reference(command)
        except Exception as e:
            raise Exception(e) from e

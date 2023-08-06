from javonet.core.handler.CommandHandler.AbstractCommandHandler import *


class GetStaticFieldHandler(AbstractCommandHandler):

    def __init__(self):
        self._required_parameters_count = 2

    def process(self, command):
        try:
            if len(command.payload) != self._required_parameters_count:
                raise Exception("GetStaticFieldHandler parameters mismatch!")
            clazz = command.payload[0]
            value = getattr(clazz, command.payload[1])
            return value
        except Exception as e:
            raise Exception(e) from e

import re
import traceback

from javonet.core.exception.JavonetException import JavonetException
from javonet.utils.ExceptionType import ExceptionType
from javonet.utils.Command import Command


class ExceptionThrower:

    @staticmethod
    def throw_exception(command_exception: Command):
        original_exception = ExceptionType.to_exception(command_exception.get_payload()[0])
        javonet_stack_command = command_exception.get_payload()[1]
        exception_name = command_exception.get_payload()[2]
        exception_message = command_exception.get_payload()[3]

        stack_trace = []
        if len(command_exception.get_payload()) > 7:
            stack_classes, stack_methods, stack_lines, stack_files = ExceptionThrower.get_local_stack_trace(command_exception.get_payload()[4],
                                                command_exception.get_payload()[5],
                                                command_exception.get_payload()[6],
                                                command_exception.get_payload()[7])
        else:
            stack_trace = []
        traceback_str = ""
        traceback_list = []

        for i in range(len(stack_methods) - 1):
            traceback_str += "File \"{}\", line {}, in {}\n".format(stack_files[i], stack_lines[i], stack_methods[i])
            if stack_classes[i]:
                traceback_str += "    {}\n".format(stack_classes[i])
            if stack_lines[i] == '':
                stack_lines[i] = 0
            traceback_list.append(traceback.FrameSummary(stack_files[i], int(stack_lines[i]), stack_methods[i]))
            
        exception = JavonetException(exception_name, exception_message, traceback_str )
        ExceptionThrower.throw_javonet_exception(original_exception, exception)


    @staticmethod
    def throw_javonet_exception(original_exception, exception):
        traceback.print_exception(type(exception), exception, exception.__traceback__)
        raise original_exception

    @staticmethod
    def get_local_stack_trace(stack_trace_classes, stack_trace_methods, stack_trace_lines, stack_trace_files):
        stack_classes = re.split("\\|", stack_trace_classes)
        stack_methods = re.split("\\|", stack_trace_methods)
        stack_lines = re.split("\\|", stack_trace_lines)
        stack_files = re.split("\\|", stack_trace_files)

        return [stack_classes, stack_methods, stack_lines, stack_files]
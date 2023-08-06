require_relative 'abstract_command_handler'

class ArraySetItemHandler < AbstractCommandHandler
  def process(command)
    array = command.payload[0]
    value = command.payload[1]
    index = command.payload[2,]
    array[index] = value
    return 0
  end
end
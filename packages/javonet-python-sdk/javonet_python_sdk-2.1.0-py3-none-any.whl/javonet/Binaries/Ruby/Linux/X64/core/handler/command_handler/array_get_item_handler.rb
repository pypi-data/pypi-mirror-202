require_relative 'abstract_command_handler'

class ArrayGetItemHandler < AbstractCommandHandler
  def process(command)
    array = command.payload[0]
    index = command.payload[1,]
    return array[index]
  end
end
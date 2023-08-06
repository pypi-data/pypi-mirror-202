require_relative 'abstract_command_handler'

class ArrayGetSizeHandler < AbstractCommandHandler
  def process(command)
    array = command.payload[0]
    return array.length()
  end
end
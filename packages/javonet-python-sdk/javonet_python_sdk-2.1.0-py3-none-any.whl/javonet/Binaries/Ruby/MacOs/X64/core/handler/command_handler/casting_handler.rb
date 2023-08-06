require_relative 'abstract_command_handler'

class CastingHandler < AbstractCommandHandler
  def process(command)
    raise "Explicit cast is forbidden in dynamically typed languages"
  end
end
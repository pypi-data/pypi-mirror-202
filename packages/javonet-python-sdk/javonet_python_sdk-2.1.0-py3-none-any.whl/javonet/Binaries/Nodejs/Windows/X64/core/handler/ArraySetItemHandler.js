const AbstractHandler =  require("./AbstractHandler")


class ArraySetItemHandler extends AbstractHandler {
    process(command) {
        let array = command.payload[0]
        let value = command.payload[1]
        let indexes = command.payload.slice(2)
        array[indexes] = value
        return 0;
    }
}

module.exports = new ArraySetItemHandler()
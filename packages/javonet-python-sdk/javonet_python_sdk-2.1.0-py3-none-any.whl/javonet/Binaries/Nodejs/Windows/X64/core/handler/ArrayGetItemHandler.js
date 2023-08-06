const AbstractHandler =  require("./AbstractHandler")


class ArrayGetItemHandler extends AbstractHandler {
    process(command) {
        let array = command.payload[0]
        let indexes = command.payload.slice(1)
        return array[indexes]
    }
}

module.exports = new ArrayGetItemHandler()
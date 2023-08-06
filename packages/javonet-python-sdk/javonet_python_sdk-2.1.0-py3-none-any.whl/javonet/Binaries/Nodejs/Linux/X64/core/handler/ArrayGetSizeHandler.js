const AbstractHandler =  require("./AbstractHandler")


class ArrayGetSizeHandler extends AbstractHandler {
    process(command) {
        let array = command.payload[0]
        return array.length
    }
}

module.exports = new ArrayGetSizeHandler()
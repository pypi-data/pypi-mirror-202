const AbstractHandler =  require("./AbstractHandler")


class ArrayGetRankHandler extends AbstractHandler {
    process(command) {
        throw new Error("ArrayGetRankHandler not implemented")
    }
}

module.exports = new ArrayGetRankHandler()
const AbstractHandler = require("./AbstractHandler");

class GetStaticFieldHandler extends AbstractHandler {
    constructor() {
        super()
    }

    process(command) {
        try {
            const {payload} = command
            let type = payload[0]
            let field = payload[1]

            return type[field]
        } catch (error) {
            return error
        }
    }
}


module.exports = new GetStaticFieldHandler()
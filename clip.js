var http = require("http")

http.createServer(function(req, res) {
    response.writeHead(200, {"Content-Type":  "text/plain"})
    response.end("Hello world\n")
}).listen(process.env.PORT)
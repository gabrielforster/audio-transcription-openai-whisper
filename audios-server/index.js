const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

const directoryPath = path.join(__dirname);

const server = http.createServer((req, res) => {
  const filePath = path.join(directoryPath, req.url);
  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
      return;
    }

    res.writeHead(200, { 'Content-Type': 'audio/ogg' });
    const readStream = fs.createReadStream(filePath);
    readStream.pipe(res);
  });
});

server.listen(PORT, () => {
  console.info(`server is listening on http://localhost:${PORT}`);
});

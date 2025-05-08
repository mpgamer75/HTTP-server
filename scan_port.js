const net = require('net');
const { performance } = require('perf_hooks');

function scanPort(host, port) {
  return new Promise((resolve) => {
    const socket = new net.Socket();
    socket.setTimeout(1000);
    socket.on('connect', () => {
      socket.destroy();
      resolve(true);
    });
    socket.on('timeout', () => {
      socket.destroy();
      resolve(false);
    });
    socket.on('error', () => {
      socket.destroy();
      resolve(false);
    });
    socket.connect(port, host);
  });
}

async function scanPorts(host, startPort, endPort) {
  console.log(`Scanning ports ${startPort}-${endPort} on ${host}...`);
  const openPorts = [];
  for (let port = startPort; port <= endPort; port++) {
    const isOpen = await scanPort(host, port);
    if (isOpen) {
      openPorts.push(port);
      console.log(`Port ${port} is OPEN`);
    } else {
      console.log(`Port ${port} is CLOSED`);
    }
  }
  return openPorts;
}

(async () => {
  const host = '127.0.0.1';
  const startPort = 1;
  const endPort = 1024;

  const startTime = performance.now();
  const openPorts = await scanPorts(host, startPort, endPort);
  const endTime = performance.now();

  console.log(`\nScan completed in ${(endTime - startTime) / 1000} seconds.`);
  console.log(`\nOpen ports: ${openPorts.join(', ')}`);
})();
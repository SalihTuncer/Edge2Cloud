/* eslint-disable no-undef */
let cpuData;
let memData;
let diskData;

let cpuOptions;
let memOptions;
let diskOptions;

let cpuChart;
let memChart;
let diskChart;

let index = 0;
let first = true;

// load current chart package
google.charts.load('current', {
  packages: ['corechart', 'line'],
});

// a chart which shows the percentage usage of the cpu of the corresponding device
function drawCPUChart() {
  // create data object with default value
  cpuData = google.visualization.arrayToDataTable([
    ['Year', 'Usage'],
    [0, 0.0],
  ]);

  // create options object with titles, colors, etc.
  cpuOptions = {
    title: 'CPU',
    hAxis: {
      title: 'Time',
    },
    vAxis: {
      title: '',
    },
    trendlines: {
      0: {
        color: 'purple',
        labelInLegend: 'trend',
        visibleInLegend: true,
        opacity: 0.4,
      },
    },
  };

  // draw chart on load
  cpuChart = new google.visualization.LineChart(document.getElementById('cpu_chart_div'));
  cpuChart.draw(cpuData, cpuOptions);
}

// a chart which shows the usage and total memory of the disk of the corresponding device
function drawMEMChart() {
  memData = google.visualization.arrayToDataTable([
    ['Year', 'Usage', 'Capacity'],
    [0, 0.0, 0.0],
  ]);

  memOptions = {
    title: 'RAM',
    hAxis: {
      title: 'Time',
    },
    vAxis: {
      title: '',
    },
    trendlines: {
      0: {
        color: 'blue',
        labelInLegend: 'trend',
        visibleInLegend: true,
        opacity: 0.4,
      },
    },
  };
  // draw chart on load
  memChart = new google.visualization.LineChart(document.getElementById('mem_chart_div'));
  memChart.draw(memData, memOptions);
}

// a chart which shows the read and write of the disk of the corresponding device
function drawDISKChart() {
  diskData = google.visualization.arrayToDataTable([
    ['Year', 'Read', 'Write'],
    [0, 0.0, 0.0],
  ]);

  diskOptions = {
    title: 'DISK',
    hAxis: {
      title: 'Time',
    },
    vAxis: {
      title: '',
    },
    trendlines: {
      0: {
        color: 'blue',
        labelInLegend: 'r-trend',
        visibleInLegend: true,
        opacity: 0.4,
      },
      1: {
        color: 'red',
        labelInLegend: 'w-trend',
        visibleInLegend: true,
        opacity: 0.4,
      },
    },
  };
  // draw chart on load
  diskChart = new google.visualization.LineChart(document.getElementById('disk_chart_div'));
  diskChart.draw(diskData, diskOptions);
}

// set callback function when api loaded
google.charts.setOnLoadCallback(drawCPUChart);

google.charts.setOnLoadCallback(drawMEMChart);

google.charts.setOnLoadCallback(drawDISKChart);

const clientId = `mqttjs_${Math.random().toString(16).substr(2, 8)}`;

const host = 'ws://localhost:9001/mqtt';

// these are the options which are used for the mqtt connection with the broker
const options = {
  keepalive: 30,
  protocolId: 'MQTT',
  protocolVersion: 4,
  clean: true,
  reconnectPeriod: 1000,
  connectTimeout: 30 * 1000,
  will: {
    topic: 'health_monitoring',
    payload: 'Connection Closed abnormally..!',
    qos: 0,
    retain: false,
  },
  rejectUnauthorized: false,
};

console.log('connecting mqtt client');
const client = mqtt.connect(host, options);

// we add the incoming messages from the health monitoring and put them in our charts
client.on('message', (topic, message, packet) => {
  // console.log('Received Message: ' + message.toString() + '\nOn topic: ' + topic)

  data = JSON.parse(message);

  if (first) {
    cpuOptions.vAxis.title = 'Usage in %';
    memOptions.vAxis.title = `Usage in ${data[1].used_mem[1]}`;
    diskOptions.vAxis.title = `Usage in ${data[2].disk_read[1]}`;
    first = false;
  }

  cpuData.addRow([index, data[0].cpu_usage]);
  cpuChart.draw(cpuData, cpuOptions);
  memData.addRow([index, data[1].used_mem[0], data[1].total_mem[0]]);
  memChart.draw(memData, memOptions);
  diskData.addRow([index, data[2].disk_read[0], data[2].disk_write[0]]);
  diskChart.draw(diskData, diskOptions);

  index += 1;
});

/* 
    we can change the interval at which messages are sent by health monitoring

    source: https://stackoverflow.com/questions/175739/built-in-way-in-javascript-to-check-if-a-string-is-a-valid-number
    first we check whether the value is a numeric number 
*/
function isNumeric(str) {
  return !str.isNaN && !parseFloat(str.isNaN);
}

// now we can send the value to the health monitoring via mqtt
function changeInterval() {
  value = document.getElementById('interval').value;
  if (isNumeric(value)) {
    client.publish('health_monitoring_interval', value);
  }
}

// generic callback functions which normally will never be called

client.on('error', (err) => {
  console.log('Connection error: ', err);
  client.end();
});

client.on('reconnect', () => {
  console.log('Reconnecting...');
});

client.on('connect', () => {
  console.log(`Client connected:${clientId}`);
  client.subscribe('health_monitoring', { qos: 0 });
});

client.on('close', () => {
  console.log(`${clientId} disconnected`);
});

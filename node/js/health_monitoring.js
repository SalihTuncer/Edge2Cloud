let cpu_data;
let mem_data;
let disk_data;

let cpu_options;
let mem_options;
let disk_options;

let cpu_chart;
let mem_chart;
let disk_chart;

let index = 0;
let first = true;

// load current chart package
google.charts.load('current', {
    packages: ['corechart', 'line']
});

// set callback function when api loaded
google.charts.setOnLoadCallback(drawCPUChart);

google.charts.setOnLoadCallback(drawMEMChart);

google.charts.setOnLoadCallback(drawDISKChart);

// a chart which shows the percentage usage of the cpu of the corresponding device
function drawCPUChart() {

    // create data object with default value
    cpu_data = google.visualization.arrayToDataTable([
        ['Year', 'Usage'],
        [0,  0.0],]);

    // create options object with titles, colors, etc.
    cpu_options = {
        title: 'CPU',
        hAxis: {
            title: 'Time'
        },
        vAxis: {
            title: ''
        },
        trendlines: {
                0: {
                color: 'purple',
                labelInLegend: 'trend',
                visibleInLegend: true,
                opacity: 0.4
                } 
        }
    };

    // draw chart on load
    cpu_chart = new google.visualization.LineChart(
        document.getElementById('cpu_chart_div')
    );
    cpu_chart.draw(cpu_data, cpu_options);

}

// a chart which shows the usage and total memory of the disk of the corresponding device
function drawMEMChart() {
    mem_data = google.visualization.arrayToDataTable([
        ['Year', 'Usage', 'Capacity'],
        [0,  0.0, 0.0],]);


    mem_options = {
        title: 'RAM',
        hAxis: {
            title: 'Time'
        },
        vAxis: {
            title: ''
        },
        trendlines: {
            0: {
                color: 'blue',
                labelInLegend: 'trend',
                visibleInLegend: true,
                opacity: 0.4
                }
        }
    };
    // draw chart on load
    mem_chart = new google.visualization.LineChart(
        document.getElementById('mem_chart_div')
    );
    mem_chart.draw(mem_data, mem_options);

}

// a chart which shows the read and write of the disk of the corresponding device
function drawDISKChart() {
    disk_data = google.visualization.arrayToDataTable([
        ['Year', 'Read', 'Write'],
        [0,  0.0, 0.0],]);

    disk_options = {
        title: 'DISK',
        hAxis: {
            title: 'Time'
        },
        vAxis: {
            title: ''
        },
        trendlines: {
            0: {
                color: 'blue',
                labelInLegend: 'r-trend',
                visibleInLegend: true,
                opacity: 0.4
                },
                1: {
                color: 'red',
                labelInLegend: 'w-trend',
                visibleInLegend: true,
                opacity: 0.4
                }
        }
    };
    // draw chart on load
    disk_chart = new google.visualization.LineChart(
        document.getElementById('disk_chart_div')
    );
    disk_chart.draw(disk_data, disk_options);
}

const clientId = 'mqttjs_' + Math.random().toString(16).substr(2, 8)

const host = 'ws://localhost:9001/mqtt'

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
        retain: false
    },
    rejectUnauthorized: false
}

console.log('connecting mqtt client')
const client = mqtt.connect(host, options)

// we add the incoming messages from the health monitoring and put them in our charts
client.on('message', (topic, message, packet) => {
    // console.log('Received Message: ' + message.toString() + '\nOn topic: ' + topic)

    message = JSON.parse(message)

    if(first){
        cpu_options.vAxis.title = 'Usage in %'
        mem_options.vAxis.title = `Usage in ${message[1].used_mem[1]}` 
        disk_options.vAxis.title = `Usage in ${message[2].disk_read[1]}` 
        first = false;
    }

    cpu_data.addRow([index, message[0].cpu_usage]);
    cpu_chart.draw(cpu_data, cpu_options);
    mem_data.addRow([index, message[1].used_mem[0], message[1].total_mem[0]]);
    mem_chart.draw(mem_data, mem_options);
    disk_data.addRow([index, message[2].disk_read[0], message[2].disk_write[0]]);
    disk_chart.draw(disk_data, disk_options);

    index++;
})

/* 
    we can change the interval at which messages are sent by health monitoring

    source: https://stackoverflow.com/questions/175739/built-in-way-in-javascript-to-check-if-a-string-is-a-valid-number
    first we check whether the value is a numeric number 
*/
function isNumeric(str) {
    return !isNaN(str) && !isNaN(parseFloat(str))
}

// now we can send the value to the health monitoring via mqtt 
function change_interval() {
    value = document.getElementById("interval").value
    if(isNumeric(value)){
        client.publish('health_monitoring_interval', value)
    }
}

// generic callback functions which normally will never be called

client.on('error', (err) => {
    console.log('Connection error: ', err)
    client.end()
})

client.on('reconnect', () => {
    console.log('Reconnecting...')
})

client.on('connect', () => {
    console.log('Client connected:' + clientId)
    client.subscribe('health_monitoring', { qos: 0 })
})

client.on('close', () => {
    console.log(clientId + ' disconnected')
})
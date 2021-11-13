const mqtt = require('mqtt')
const fs = require('fs')
const { Command } = require('commander')

const program = new Command()
program
  .option('-p, --protocol <type>', 'connect protocol: ws, wss. default is mqtt', 'ws')
  .parse(process.argv)

const host = 'localhost'
const port = '9001'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`

// connect options
const OPTIONS = {
  clientId,
  clean: true,
  connectTimeout: 4000,
  reconnectPeriod: 1000,
}
// protocol list
const PROTOCOLS = ['ws']

// default is mqtt, unencrypted tcp connection
let connectUrl = `ws://${host}:${port}`
const mountPath = '/mqtt' // mount path, connect emqx via WebSocket
connectUrl = `ws://${host}:9001${mountPath}`

const topic = 'health_monitoring'

const client = mqtt.connect(connectUrl, OPTIONS)

client.on('connect', () => {
  console.log(`${program.protocol}: Connected`)
  client.subscribe([topic], () => {
    console.log(`${program.protocol}: Subscribe to topic '${topic}'`)
  })
})

client.on('reconnect', (error) => {
  console.log(`Reconnecting(${program.protocol}):`, error)
})

client.on('error', (error) => {
  console.log(`Cannot connect(${program.protocol}):`, error)
})

client.on('message', (topic, payload) => {
  console.log('Received Message:', topic, payload.toString())
})
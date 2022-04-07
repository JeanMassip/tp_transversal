const clientId = 'mqttjs'
const host = 'ws://172.19.128.169:9001'

const options = {
  keepalive: 60,
  clientId: clientId,
  protocolId: 'MQTT',
  protocolVersion: 4,
  clean: true,
  reconnectPeriod: 1000,
  connectTimeout: 30 * 1000,
  will: {
    topic: 'WillMsg',
    payload: 'Connection Closed abnormally..!',
    qos: 0,
    retain: false
  },
}

console.log('Connecting mqtt client')
const client = mqtt.connect(host, options)

client.on('error', (err) => {
  console.log('Connection error: ', err)
  client.end()
})

client.on('connect', () => {
  console.log('Client connected:' + clientId)
  client.subscribe('/denm/latest', { qos: 0 })
})

client.on('reconnect', () => {
  console.log('Reconnecting...')
})

client.on('message', (topic, message, packet) => {
  console.log('Received Message: ' + message.toString() + '\nOn topic: ' + topic)
  data = JSON.parse(message.toString())
  display = document.getElementById("state")
  state.innerHTML = data.message.cause_name
})
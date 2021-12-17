var mqtt
var host = "127.0.0.1"
var port = 1883

MQTTConnect = () => {
    console.log("connecting to " + host + ":" + port)
    mqtt = Paho.MQTT.Client(host, port, "clientjs")
    var options = {
        timeout: 3,
        onSuccess: onconnect,
        onFailure: onfailure,
    }
    mqtt.onMessageArrived = onMessageArrived
    mqtt.connect(options)
}

onFailure = (message) => {
    console.error("Unable to connect to " + host + ": " + message)
}

onMessageArrived = (message) => {
    console.log("Message received : " + message.payloadString)
}
package receiver

import (
	"context"
	"fmt"
	"math/rand"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

type Receiver struct {
	MessageChan           chan *string
	Client                mqtt.Client
	MessageHandler        func(client mqtt.Client, msg mqtt.Message)
	ConnectHandler        func(client mqtt.Client)
	ConnectionLostHandler func(client mqtt.Client, err error)
	cancelFunc            context.CancelFunc
}

func New() (*Receiver, error) {
	r := Receiver{
		MessageChan: make(chan *string),
	}

	r.ConnectionLostHandler = func(client mqtt.Client, err error) {
		fmt.Printf("Connection to Broker lost : %v\n", err)
		r.cancelFunc()
		close(r.MessageChan)
	}

	r.ConnectHandler = func(client mqtt.Client) {
		fmt.Println("Connected !")
	}

	r.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
		strMsg := string(msg.Payload())
		fmt.Printf("message received : %s\n", strMsg)
		r.MessageChan <- &strMsg
	}

	return &r, nil
}

func (r *Receiver) Connect() context.Context {
	opts := mqtt.NewClientOptions()
	opts.AddBroker("tcp://127.0.0.1:1883")
	opts.SetClientID(fmt.Sprintf("receiver-%d", rand.Intn(1000)))
	opts.SetDefaultPublishHandler(r.MessageHandler)
	opts.OnConnect = r.ConnectHandler
	opts.OnConnectionLost = r.ConnectionLostHandler
	r.Client = mqtt.NewClient(opts)
	if token := r.Client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}

	ctx, cancel := context.WithCancel(context.Background())
	r.cancelFunc = cancel
	return ctx
}

func (r *Receiver) Subscribe(topic string) {
	token := r.Client.Subscribe(topic, 0, nil)
	token.Wait()
	fmt.Printf("Subscribed to %s \n", topic)
}

func (r *Receiver) Unsubscribe(topic string) {
	r.cancelFunc()
	token := r.Client.Unsubscribe(topic)
	token.Wait()
	fmt.Printf("Unsubscribed from %s \n", topic)
}

func (r *Receiver) Disconnect() {
	r.cancelFunc()
	r.Client.Disconnect(2500)
}

package broker

import (
	"fmt"
	"jk/broker/handlers"
	"jk/broker/receiver"
)

type Broker struct {
	CAMReceiver  receiver.Receiver
	DENMReceiver receiver.Receiver

	CAMHandler  handlers.CAMHandler
	DENMHandler handlers.DENMHandler
}

func New() (*Broker, error) {
	camReceiver, err := receiver.New()
	if err != nil {
		return nil, err
	}

	denmReceiver, err := receiver.New()
	if err != nil {
		return nil, err
	}

	return &Broker{
		CAMReceiver:  *camReceiver,
		DENMReceiver: *denmReceiver,
		CAMHandler:   *handlers.NewCAMHandler(),
		DENMHandler:  *handlers.NewDENMHandler(),
	}, nil
}

func (b Broker) Start() {
	camContext := b.CAMReceiver.Connect()
	defer b.CAMReceiver.Disconnect()

	denmContext := b.DENMReceiver.Connect()
	defer b.DENMReceiver.Disconnect()

	b.CAMReceiver.Subscribe("/sensors/cam")
	b.DENMReceiver.Subscribe("/sensors/denm")

	for {
		select {
		case message, ok := <-b.CAMReceiver.MessageChan:
			if ok {
				err := b.CAMHandler.HandleMessage(*message)
				if err != nil {
					fmt.Printf("Unable to handle message : %v", err)
				}
			}
		case message, ok := <-b.DENMReceiver.MessageChan:
			if ok {
				err := b.DENMHandler.HandleMessage(*message)
				if err != nil {
					fmt.Printf("Unable to handle message : %v", err)
				}
			}
		case <-camContext.Done():
			fmt.Println("Stopping Broker")
			return
		case <-denmContext.Done():
			fmt.Println("Stopping Broker")
			return
		}
	}
}

func (b Broker) AddVehiculeToHandler(vec handlers.Vehicule) {
	b.CAMHandler.AddVehicule(vec)
}

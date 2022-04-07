package main

import (
	"context"
	"jk/broker/handlers"
	"log"
)

type Broker struct {
	CAMReceiver  Receiver
	DENMReceiver Receiver

	CAMHandler  handlers.CAMHandler
	DENMHandler handlers.DENMHandler
}

func main() {
	broker, err := NewBroker()
	if err != nil {
		log.Fatal(err)
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	broker.Start(ctx)
}

func NewBroker() (*Broker, error) {
	camReceiver, err := NewReceiver()
	if err != nil {
		return nil, err
	}

	denmReceiver, err := NewReceiver()
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

func (b Broker) Start(ctx context.Context) {
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
				b.CAMHandler.HandleMessage(*message)
			}
		case message, ok := <-b.DENMReceiver.MessageChan:
			if ok {
				b.DENMHandler.HandleMessage(*message)
			}
		case <-camContext.Done():
			return
		case <-denmContext.Done():
			return
		}
	}
}

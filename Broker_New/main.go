package main

import (
	"io"
	"jk/broker/handlers"
	"jk/broker/pki"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {

	broker, err := NewBroker()
	if err != nil {
		log.Fatal(err)
	}

	router := mux.NewRouter()
	router.HandleFunc("/auth", func(w http.ResponseWriter, r *http.Request) {
		cert, err := io.ReadAll(r.Body)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte("No certificate provided"))
			return
		}

		cn, err := pki.ValidateCertificate(cert)
		if err != nil {
			w.WriteHeader(http.StatusUnprocessableEntity)
			w.Write([]byte("Invalid certificate"))
			return
		}

		vec := handlers.Vehicule{StationID: cn}
		broker.AddVehiculeToHandler(vec)

		w.WriteHeader(http.StatusAccepted)
		w.Write([]byte("Vehicule authenticated"))
	})

	go broker.Start()
	if err := http.ListenAndServe("0.0.0.0:5000", router); err != nil {
		log.Fatal(err)
	}
	/*
		validCert, err := ioutil.ReadFile("VecCERT.pem")
		if err != nil {
			panic(err)
		}

		cn, err := pki.ValidateCertificate(validCert)
		if err != nil {
			fmt.Println(err)
		}
		fmt.Println(cn)
	*/
}

type Broker struct {
	CAMReceiver  Receiver
	DENMReceiver Receiver

	CAMHandler  handlers.CAMHandler
	DENMHandler handlers.DENMHandler
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

func (b Broker) AddVehiculeToHandler(vec handlers.Vehicule) {
	b.CAMHandler.AddVehicule(vec)
}

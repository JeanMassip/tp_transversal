package pki

import (
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"io/ioutil"
)

func ValidateCertificate(data []byte) (string, error) {
	block, _ := pem.Decode(data)
	if block == nil {
		return "", fmt.Errorf("invalid certificate encoding")
	}

	cert, err := x509.ParseCertificate(block.Bytes)
	if err != nil {
		return "", err
	}

	caCert, err := ioutil.ReadFile("CAcrt.pem")
	if err != nil {
		return "", err
	}

	roots := x509.NewCertPool()
	if ok := roots.AppendCertsFromPEM(caCert); !ok {
		fmt.Println("Certificate not added ")
	}

	opts := x509.VerifyOptions{
		Roots: roots,
	}

	if _, err := cert.Verify(opts); err != nil {
		return "", fmt.Errorf("invalid certificate : %v", err)
	}

	return cert.Subject.CommonName, nil
}

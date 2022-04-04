from ssl import cert_time_to_seconds
from flask import Flask, request
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from getpass import getpass
from pki import sign_csr

app = Flask("__name__")

@app.post("/sign_csr")
def sign_csr_request():
    csr_file = request.get_data(as_text=False)
    csr = x509.load_pem_x509_csr(csr_file, default_backend())

    ca_public_key_file = open("CAcrt.pem", "rb")
    ca_public_key = x509.load_pem_x509_certificate(ca_public_key_file.read(), default_backend())

    ca_private_key_file = open("ca-private-key.pem", "rb")
    ca_private_key =  serialization.load_pem_private_key(ca_private_key_file.read(), getpass().encode("utf-8"), default_backend())

    cert = sign_csr(csr, ca_public_key, ca_private_key)
    return cert, 200 



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
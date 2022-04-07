from datetime import datetime, timedelta
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.x509 import CertificateSigningRequest, NameOID

def sign_csr(csr: CertificateSigningRequest, ca_public_key, ca_private_key):
    valid_from = datetime.utcnow()
    valid_until = valid_from + timedelta(days=30)
    serial_number = x509.random_serial_number()

    builder = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_public_key.subject)
        .public_key(csr.public_key())
        .serial_number(serial_number)
        .not_valid_before(valid_from)
        .not_valid_after(valid_until)
    )

    for extension in csr.extensions:
        builder = builder.add_extension(extension.value, extension.critical)

    public_key = builder.sign(
        private_key=ca_private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend(),
    )
    
    return public_key.public_bytes(serialization.Encoding.PEM)
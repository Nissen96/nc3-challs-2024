from Crypto.PublicKey import RSA
from OpenSSL import crypto


# Generate RSA key files in PEM and PKCS8 format
key = RSA.generate(2048)

with open("keys/key-params.txt", "w") as f:
    f.write(f"p = {key.p}\n")
    f.write(f"q = {key.q}\n")
    f.write(f"n = {key.n}\n")
    f.write(f"e = {key.e}\n")
    f.write(f"d = {key.d}\n")

with open("keys/key.pem", "wb") as f:
    f.write(key.export_key("PEM"))

with open("keys/key.pkcs8", "wb") as f:
    f.write(key.export_key(pkcs=8))


# Generate self-signed certificate
k = crypto.load_privatekey(crypto.FILETYPE_PEM, key.export_key("PEM"))
cert = crypto.X509()
cert.get_subject().C = "GN"
cert.get_subject().ST = "Region Grum"
cert.get_subject().L = "Brokhøj"
cert.get_subject().O = "Kaos A/S"
cert.get_subject().OU = "Afdelingen for Julens Undergang"
cert.get_subject().CN = "julens-undergang.gnom"
cert.get_subject().emailAddress = "support@kaos.gnom"
cert.set_serial_number(24122024)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(k)
cert.sign(k, "sha512")

with open("keys/cert.pem", "wb") as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

import ecdsa

def main():
    privateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    file_out = open("walletkey.pem", "wb+")
    file_out.write(privateKey.to_pem())

if __name__ == "__main__":
    main()

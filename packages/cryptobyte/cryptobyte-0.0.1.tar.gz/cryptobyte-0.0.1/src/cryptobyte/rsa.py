from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify

key = RSA.generate(1024)

private_key = key
public_key = key.publickey()

data_to_encrypt = b"Hello, this is a message to be encrypted."
cipher_rsa = PKCS1_OAEP.new(public_key)

# Encrypt the provided data using the public key
encrypted = cipher_rsa.encrypt(data_to_encrypt)
print("Encrypted:", hexlify(encrypted))

# Decrypt using private key
cipher_rsa = PKCS1_OAEP.new(private_key)
decrypted = cipher_rsa.decrypt(encrypted)

# Display the decrypted result as a UTF-8 encoded string
print("Decrypted:", decrypted.decode("utf-8"))
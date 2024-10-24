import hashlib

message = "Hello this is text"

md5_hash = hashlib.md5(message.encode())
print("MESSAGE:", message)
print("MD5 HASH VALUE:", md5_hash.hexdigest())
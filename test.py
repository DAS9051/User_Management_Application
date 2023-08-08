from hashlib import sha256



password = "hello"
password = sha256(password.encode('utf-8')).hexdigest()
print(password)
print(len(password))
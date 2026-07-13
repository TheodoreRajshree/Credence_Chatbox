import hashlib

password = "admin123"

print(hashlib.md5(password.encode()).hexdigest())
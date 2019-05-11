from fastecdsa import keys, curve, ecdsa
from hashlib import sha256

priv, pub = keys.gen_keypair(curve.P256)

print(priv)
print(pub)
print(sha256( str(pub).encode()).hexdigest())
print(type(pub))

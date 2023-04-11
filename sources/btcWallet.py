from cryptos import *

c = Bitcoin(testnet=True)
priv = sha256('a big long brainwallet password')
print("private:", priv)
pub = c.privtopub(priv)
print("pub:", pub)
with c.pubtoaddr(pub) as addr:
    print("addr:", addr)
    print(c.unspent(addr))


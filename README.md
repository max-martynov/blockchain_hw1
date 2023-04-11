# Digital signature algorithm using RSA

Fot this home assignment I chose to implement RSA algorithm for the signing and verfication of simple text documents. 

## Description

I chose to implement the algorithm from scratch instead of using third-party libraries to gain a better understanding of it. The approach I used is similar to traditional encryption using RSA. However, in the case of signing, we first use our private key to leave a unique fingerprint on the document. Then, anyone can verify that the document was properly signed by using the corresponding public key.

## How to use

An example of the use-case is below:
```bash
$ python3 main.py generate keys
$ python3 main.py sign keys/key.pub sample.txt
$ python3 main.py verify keys/key sample_signed.txt
Verification complete :)
```
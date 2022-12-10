# Pailler homomorphic encryption

from phe import pailler as pl
import requests

class RequestError(Exception):
    def __init__(self, message):
        self.message = message

PRECISION = 2**(-16)
URL = 'http://localhost:8000/prediction'

def query_pred(vector, keys=None):
    # Generate public and private key if not provided
    if keys is None:
        pub, priv = pl.generate_paillier_keypair()
    else:
        pub, priv = keys

    # Encrypt each element in the vector
    encrypted = [pub.encrypt(i, precision=PRECISION).ciphertext() for i in vector]

    # Send the vector
    req = requests.post(URL, json={'pub_key_n': pub, 'enc_feature_vector': encrypted})

    # Check request status
    if req.status_code != 200:
        raise RequestError(f'Bad Status: {req.status_code}')

    encrypted_y = req.json()[ 'enc_prediction']

    # Decrypt y by specifying which exponent pailler should use to read the integer
    return priv.decrypt(pl.EncryptedNumber(pub, encrypted_y, -8))


def test():
    assert 2**(-16) > abs(query_pred([0.48555949, 0.29289251, 0.63463107,
                                        0.41933057, 0.78672205, 0.58910837,
                                        0.00739207, 0.31390802, 0.37037496,
                                        0.3375726 ]) - 0.44812144746653826)

if __name__ == '__main__':
    test()
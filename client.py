"""Lado do Cliente. Simula as ações de um cliente que envia as dados criptografados para o servidor."""
import phe as paillier
import json

from linear_model import LinearModel


def generate_key_pair():
    """
    Gera um par de chave pública e privada, de acordo com o esquema Paillier. Uma chave é composta por
    vários elementos, mas os principais são os dois números primos de altíssimo fator, p e q. A partir
    deles, é possível chegar a n através de n = p x q.

    n será a chave pública, uma vez que a multiplicação de várias combinações de números primos pode
    resultar nesse valor.

    p e q serão os elementos privados, já que são os determinantes de n.
    """

    pubKey, privKey = paillier.generate_paillier_keypair()
    keys = {
        'public_key': {'n': pubKey.n},
        'private_key': {'p': privKey.p, 'q': privKey.q}
    }
    with open("vault/client_keys.json", "w") as file:
        json.dump(keys, file)


def retrive_keys_from_vault():
    """Retorna as chaves."""
    with open("vault/client_keys.json", 'r') as file:
        keys = json.load(file)
        pubKey = paillier.PaillierPublicKey(n=int(keys['public_key']['n']))
        privKey = paillier.PaillierPrivateKey(pubKey, keys['private_key']['q'], keys['private_key']['p'])

        return pubKey, privKey


def encrypt_data(pubKey, data):
    "Criptografa os dados que serão enviados para o servidor."
    encrypted_data = [pubKey.encrypt(i) for i in data]

    payload = {
        'public_key': {'n': pubKey.n},
        'values': [(str(i.ciphertext()), i.exponent) for i in encrypted_data]
    }

    payload_to_server = json.dumps(payload)
    return payload


# Fluxo do CLIENTE
if __name__ == '__main__':

    DATA_TO_SERVER = [25, 0, 23, 0, 0, 2]

    # Passo 01 - Chaves Criptográficas são Geradas
    #generate_key_pair()       # É necessário gerar apenas uma vez...

    # Passo 02 - Com as chaves em mão, gerar dados criptográficos e mandar para o servidor.
    pubKey, privKey = retrive_keys_from_vault()
    payload = encrypt_data(pubKey, DATA_TO_SERVER)
    with open('network/data_to_server.json', 'w') as file :
        json.dump(payload, file)

    # ...
    # ...
    # ...
    # Assumindo que o Servidor Respondeu...

    # Passo 03 - Verificar o Resultado do Servidor
    with open('network/server_response.json', 'r') as file:
        response = json.load(file)
        
        pubKey_response = paillier.PaillierPublicKey(n=int(response['public_key']['n']))
        result = paillier.EncryptedNumber(pubKey_response, int(response['values'][0]), 
                                                           int(response['values'][1]))

        # Passo 04 - Se o resultado de Chave Pública bater, Descriptografar a Resposta
        if (pubKey_response == pubKey):
            print(f'O resultado retornado do servidor é {privKey.decrypt(result)}')
    
    # Passo Final - Rodando uma Verificação com dados descriptografados para validar resposta.
    model = LinearModel(dataset="data/insurance-unscaled.csv")
    model.train("charges")
    print(f'O resultado do modelo é {model.run_prediction(DATA_TO_SERVER)}')
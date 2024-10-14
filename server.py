"""Lógica do lado do servidor."""
import json
import phe as paillier

from linear_model import LinearModel


def get_client_data():
    """Buscando os dados que vieram da 'rede'."""

    with open('network/data_to_server.json', 'r') as file:
        payload = json.load(file)
        return payload


def generate_results(data):
    """
    Para gerar os resultados, será criado um modelo linear pré-treinado (o estado que teríamos no 
    servidor), e então serão extraídos os coeficientes dele, que serão correlacionados com nossos dados.
    """
    model = LinearModel(dataset="data/insurance-unscaled.csv")
    print("Gerando Modelo Pré-Treinado....")
    model.train("charges")
    print("Modelo Gerado!\n")
    weights = model.model.coef_

    pubKey = data["public_key"]
    pubkey= paillier.PaillierPublicKey(n=int(pubKey['n']))
    encrypted_data = [paillier.EncryptedNumber(pubkey, int(x[0], int(x[1]))) for x in data['values']]

    return sum([weights[i] * encrypted_data[i] for i in range(len(weights))]), pubKey


def encrypt_result(result, pubKey):
    "Criptografa os dados que serão enviados de volta para o cliente."
    payload = {
        'public_key': {'n': pubKey['n']},
        'values': (str(result.ciphertext()), result.exponent)
    }
    payload_to_client = json.dumps(payload)
    return payload


# Emulando lógica do SERVIDOR
if __name__ == "__main__":
    
    # Passo 01 - Buscar os Dados Enviados do Cliente
    data = get_client_data()

    # Passo 02 - Gerar os Resultados Esperados
    result, pubKey = generate_results(data)

    # Passo 03 - Enviar os Dados de Volta
    return_data = encrypt_result(result, pubKey)
    with open('network/server_response.json', 'w') as file:
        json.dump(return_data, file)
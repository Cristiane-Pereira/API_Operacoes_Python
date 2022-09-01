from ast import Return
import json
import logging
import jsonschema
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    STATUS_CODE = 200

    BODY_VALIDATION = {
        "title": "Request",
        "type": "object",
        "required": ["token", "operacao", "numero_1", "numero_2"],
        "properties": {
            "token": {
                "type": "string",
            },
            "operacao": {
                "type": "string",
                "enun": ['soma', 'subtração', 'multiplicação', 'divisão']
            },
            "numero_1": {
                "type": "number"
            },
            "numero_2": {
                "type": "number"
            },
        }
    }
    try:
        req_body = req.get_json()
        jsonschema.validate(req_body, BODY_VALIDATION)
        # response = req_body

        validaToken(req_body['token'])

        numero_1 = req_body.get('numero_1')
        numero_2 = req_body.get('numero_2')
        operacao = req_body.get('operacao')

        if operacao == 'soma':
            resultado = soma(numero_1, numero_2)
            response = {
                "msg": f"A {operacao} do número {numero_1} com o número {numero_2} é {resultado}."
            }

        elif operacao == 'subtração':
            resultado = subtracao(numero_1, numero_2)
            response = {
                "msg": f"A {operacao} do número {numero_1} com o número {numero_2} é {resultado}."
            }

        elif operacao == 'multiplicação':
            resultado = multiplicacao(numero_1, numero_2)
            response = {
                "msg": f"A {operacao} do número {numero_1} com o número {numero_2} é {resultado}."
            }

        elif operacao == 'divisão':
            resultado = divisao(numero_1, numero_2)
            response = {
                "msg": f"A {operacao} do número {numero_1} com o número {numero_2} é {resultado}."
            }

    except jsonschema.exceptions.ValidationError as validation_error:
        STATUS_CODE = 400
        response = {
            "error": f"JSON inválido - {validation_error.message}"
        }

    except TokenInvalido:
        STATUS_CODE = 403
        response = {
            "msg": f"Token inválido."
        }

    except:
        STATUS_CODE: 503
        response = {'error': 'Erro na operação!!!'}

    finally:
        return func.HttpResponse(body=json.dumps(response), status_code=STATUS_CODE, mimetype='Aplication/json')


def soma(numero_1: int, numero_2: int) -> int:
    logging.warn(numero_1 + numero_2)
    return numero_1 + numero_2


def subtracao(numero_1: int, numero_2: int) -> int:
    logging.warn(numero_1 - numero_2)
    return numero_1 - numero_2


def multiplicacao(numero_1: int, numero_2: int) -> int:
    logging.warn(numero_1 * numero_2)
    return numero_1 * numero_2


def divisao(numero_1: int, numero_2: int) -> int:
    logging.warn(numero_1 / numero_2)
    return numero_1 / numero_2


def validaToken(token: str) -> None:

    TOKENS = [
        '46070d4bf934fb0d4b06d9e2c46e346944e322444900a435d7d9a95e6d7435f5',
        '46070d4bf934fb0d4b06d9e2c46e346944e322444900a435d7d9a95e6d7435g6',
        '46070d4bf934fb0d4b06d9e2c46e346944e322444900a435d7d9a95e6d7435h7',
        '46070d4bf934fb0d4b06d9e2c46e346944e322444900a435d7d9a95e6d7435i8'
    ]

    if token not in TOKENS:
        raise TokenInvalido()


class TokenInvalido(Exception):
    pass 
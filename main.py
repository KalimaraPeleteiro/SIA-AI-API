import pickle
from flask import Flask, request, jsonify, make_response

app = Flask("IA API")

# CONSTANTES
COLUNAS_ANALISE_SOLO_CULTURA = ["Nitrogênio", "Fósforo", "Potássio", "Temperatura", "Umidade", "pH", "Chuva"]
COLUNAS_ANALISE_SOLO_FERTILIZANTE = ["Temperatura", "Umidade do Ar", "Umidade do Solo", "Nitrogênio", "Potássio", "Fósforo"]
COLUNAS_PREVISAO_SAFRA = ["Cultura", "Ano", "Pesticidas (ton)", "Temperatura", "Chuva Anual"]
DICIONARIO_ANALISE_SOLO_CULTURA = {
    0: 'Arroz',
    1: 'Milho',
    2: 'Juta',
    3: 'Algodão',
    4: 'Coco',
    5: 'Mamão',
    6: 'Laranja',
    7: 'Maçã',
    8: 'Melão',
    9: 'Melancia',
    10: 'Uva',
    11: 'Manga',
    12: 'Banana',
    13: 'Romã',
    14: 'Lentilha',
    15: 'Feijão Preto',
    16: 'Feijão Fradinho',
    17: 'Feijão Mariposa',
    18: 'Feijão Guandu',
    19: 'Feijão Roxo',
    20: 'Grão de Bico',
    21: 'Café'
}
DICIONARIO_ANALISE_SOLO_FERTILIZANTE = {
    0: 'Ureia',
    1: 'Fosfato Diamônico (DAP)',
    2: 'Fertilizante Proporção 28-28-0',
    3: 'Fertilizante Proporção 14-35-14',
    4: 'Fertilizante Proporção 20-20',
    5: 'Fertilizante Proporção 17-17-17',
    6: 'Fertilizante Proporção 10-26-26'
}
DICIONARIO_CULTURAS_PREVISAO_SAFRA = {
    "Mandioca": 0,
    "Milho": 1,
    "Batata": 2,
    "Arroz": 3,
    "Sorgo": 4,
    "Soja": 5,
    "Batata Doce": 6,
    "Trigo": 7,
    "Inhame": 8
}


# Rota para a previsão de culturas (Análise do Solo)
@app.route("/analise/solo/cultura/", methods=["POST"])
def previsao_cultura():
    dados = request.get_json()
    
    # Verificando se os parâmetros estão corretos
    if list(dados.keys()) != COLUNAS_ANALISE_SOLO_CULTURA:
        resposta = make_response(
            jsonify(
                {"Aviso!": f"As colunas enviadas não estão de acordo com o exigido. O conjunto correto é {COLUNAS_ANALISE_SOLO_CULTURA}"}),
            400)
        resposta.headers["Content-Type"] = "application/json"
        return resposta
    
    else:
        modelo = pickle.load(open("modelos/recomendacao_cultura.sav", "rb")) # Importando o modelo
        resultado = modelo.predict([list(dados.values())]) # Prevendo o resultado
        resultado = DICIONARIO_ANALISE_SOLO_CULTURA[resultado[0]] # Transformando o resultado para algo legível
        resposta = make_response(
            jsonify(
                {"Resposta": f"{resultado}"}),
            200)
        resposta.headers["Content-Type"] = "application/json"
        return resposta


# Rota para a recomendação de fertilizantes (Análise do Solo)
@app.route("/analise/solo/fertilizante/", methods=["POST"])
def previsao_fertilizante():
    dados = request.get_json()
    
    # Verificando se os parâmetros estão corretos
    if list(dados.keys()) != COLUNAS_ANALISE_SOLO_FERTILIZANTE:
        resposta = make_response(
            jsonify(
                {"Aviso!": f"As colunas enviadas não estão de acordo com o exigido. O conjunto correto é {COLUNAS_ANALISE_SOLO_FERTILIZANTE}"}),
            400)
        resposta.headers["Content-Type"] = "application/json"
        return resposta
    
    else:
        modelo = pickle.load(open("modelos/recomendacao_fertilizante.sav", "rb")) # Importando o modelo
        resultado = modelo.predict([list(dados.values())]) # Prevendo o resultado
        resultado = DICIONARIO_ANALISE_SOLO_FERTILIZANTE[resultado[0]] # Transformando o resultado para algo legível
        resposta = make_response(
            jsonify(
                {"Resposta": f"{resultado}"}),
            200)
        resposta.headers["Content-Type"] = "application/json"
        return resposta


# Rota para a previsão de safra
@app.route("/previsao/safra/", methods=["POST"])
def previsao_safra():
    dados = request.get_json()
    
    # Verificando se os parâmetros estão corretos
    if list(dados.keys()) != COLUNAS_PREVISAO_SAFRA:
        resposta = make_response(
            jsonify(
                {"Aviso!": f"As colunas enviadas não estão de acordo com o exigido. O conjunto correto é {COLUNAS_PREVISAO_SAFRA}"}),
            400)
        resposta.headers["Content-Type"] = "application/json"
        return resposta
    
    else:
        dados = list(dados.values())

        if dados[0] not in DICIONARIO_CULTURAS_PREVISAO_SAFRA.keys(): # Se a cultura não estiver entre as disponíveis, avisar.
            resposta = make_response(
            jsonify(
                {"Aviso!": f"Cultura inválida! As culturas disponíveis para a previsão de safra são {list(DICIONARIO_CULTURAS_PREVISAO_SAFRA.keys())}"}),
            400)
            resposta.headers["Content-Type"] = "application/json"
            return resposta
        
        else: # Caso contrário, fazer a predição
            dados[0] = DICIONARIO_CULTURAS_PREVISAO_SAFRA[dados[0]] # Transformando a string em número
            modelo = pickle.load(open("modelos/previsao_safra.sav", "rb")) # Importando o modelo
            resultado = modelo.predict([dados]) # Prevendo o resultado
            resposta = make_response(
                jsonify(
                    {"Previsão": f"{resultado/10} Kilogramas por Hectare"}),
                200)
            resposta.headers["Content-Type"] = "application/json"
            return resposta


app.run(debug=True)
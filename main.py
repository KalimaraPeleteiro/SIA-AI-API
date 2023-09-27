import pickle
from flask import Flask, request, jsonify, make_response

app = Flask("IA API")

# CONSTANTES
COLUNAS_CULTURA = ["Nitrogênio", "Fósforo", "Potássio", "Temperatura", "Umidade", "pH", "Chuva"]
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


@app.route("/")
def index():
    return "Essa é a rota index. Tente outras rotas para predições de aprendizado de máquina."


# Rota para a previsão de culturas (Análise do Solo)
@app.route("/analise/solo/", methods=["POST"])
def previsao_cultura():
    dados = request.get_json()
    
    if list(dados.keys()) != COLUNAS_CULTURA:
        resposta = make_response(
            jsonify(
                {"Aviso!": "As colunas enviadas não estão de acordo com o exigido. Favor analisar a documentação para entender como estruturar o JSON"}),
            400)
        resposta.headers["Content-Type"] = "application/json"
        return resposta
    
    else:
        modelo = pickle.load(open("modelos/recomendacao_cultura.sav", "rb"))
        resultado = modelo.predict([list(dados.values())])
        resultado = DICIONARIO_ANALISE_SOLO_CULTURA[resultado[0]]
        resposta = make_response(
            jsonify(
                {"Resposta": f"{resultado}"}),
            200)
        resposta.headers["Content-Type"] = "application/json"
        return resposta

app.run(debug=True)
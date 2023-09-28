import pickle
from flask import Flask, request, jsonify, make_response

app = Flask("IA API")



# ========= CONSTANTES =========
COLUNAS_ANALISE_SOLO_CULTURA = ["Nitrogênio", "Fósforo", "Potássio", "Temperatura", "Umidade", "pH", "Chuva"]
COLUNAS_ANALISE_SOLO_FERTILIZANTE = ["Temperatura", "Umidade do Ar", "Umidade do Solo", "Nitrogênio", 
                                     "Potássio", "Fósforo"]
COLUNAS_ANALISE_AGUA = ["Alumínio", "Amônia", "Arsênio", "Bário", "Cádmio", "Cloro", "Cromo",
                        "Cobre", "Flúor", "Bactérias", "Vírus", "Chumbo", "Nitrato", "Nitrito", 
                        "Mercúrio", "Perclorato", "Rádio", "Selênio", "Prata", "Urânio"]
COLUNAS_PREVISAO_SAFRA = ["Cultura", "Ano", "Pesticidas (ton)", "Temperatura", "Chuva Anual"]
COLUNAS_RECOMENDACAO_IRRIGACAO = ["Cultura", "Dias Ativos (Cultura)", "Umidade do Solo",
                                  "Temperatura", "Umidade do Ar"]
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
DICIONARIO_ANALISE_AGUA = {
    0: "Insalubre",
    1: "Potável"
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
DICIONARIO_CULTURAS_RECOMENDACAO_IRRIGACAO = {
    "Cana-de-Açúcar": 0,
    "Trigo": 1,
    "Batata": 2,
    "Arroz": 3,
    "Café": 4,
    "Amendoim": 5,
    "Flores": 6,
    "Milho": 7,
    "Vagem": 8
}
DICIONARIO_RECOMENDACAO_IRRIGACAO = {
    0: "Irrigação não é necessária.",
    1: "Irrigação recomendada."
}



# ========= FUNÇÕES =========
""" 
Cada rota da API aceitará somente um conjunto específico de parâmetros para o modelo. Caso a requisição
seja feita com parâmetros incorretos ou fora de ordem, a resposta será um erro HTTP 400. Essa função
compara os dados JSON enviados no pedido POST com os parâmetros e verifica se o pedido é válido.
"""
def verificar_colunas(dados: dict, colunas: list):
    if list(dados.keys()) != colunas:
        resposta = make_response(
            jsonify(
                {"Aviso!": f"As colunas enviadas não estão de acordo com o exigido. O conjunto correto é {colunas}"}),
            400)
        resposta.headers["Content-Type"] = "application/json"
        return resposta
    else:
        return False


"""
Uma vez que as colunas tenham sido verificadas, o modelo é invocado e utilizado para prever o resultado
com base nos parâmetros. Como o resultado é numérico, um dicionário com as respostas equivalentes ao
entregue deve ser usado para a conversão antes de envio da resposta. Essa função realiza esse processo
por inteiro.
"""
def resposta_modelo(dados: dict, modelo_arquivo: str, dicionario: dict):
    modelo = pickle.load(open(modelo_arquivo, "rb")) # Importando o modelo
    resultado = modelo.predict([list(dados.values())]) # Prevendo o resultado
    resultado = dicionario[resultado[0]] # Transformando o resultado para algo legível
    resposta = make_response(
        jsonify(
            {"Resposta": f"{resultado}"}),
        200)
    resposta.headers["Content-Type"] = "application/json"
    return resposta


"""
Alguns modelos tem como seus parâmetros culturas. Logo, é necessário verificar se a cultura enviada no
POST contempla as culturas que o modelo abrange. Essa função faz isso.
"""
def verificar_culturas(cultura: str, dicionario: dict):
    if cultura not in dicionario.keys():
        resposta = make_response(
        jsonify(
            {"Aviso!": f"Cultura inválida! As culturas disponíveis para a previsão de safra são {list(dicionario.keys())}"}),
        400)
        resposta.headers["Content-Type"] = "application/json"
        return resposta
    else:
        return False



# ========= ROTAS DA API =========
# Rota para a previsão de culturas (Análise do Solo)
@app.route("/analise/solo/cultura/", methods=["POST"])
def previsao_cultura():
    dados = request.get_json()
    
    if not verificar_colunas(dados, COLUNAS_ANALISE_SOLO_CULTURA):
        return resposta_modelo(dados, "modelos/analise_cultura.sav", DICIONARIO_ANALISE_SOLO_CULTURA)
    else:
        return verificar_colunas(dados, COLUNAS_ANALISE_SOLO_CULTURA)


# Rota para a recomendação de fertilizantes (Análise do Solo)
@app.route("/analise/solo/fertilizante/", methods=["POST"])
def previsao_fertilizante():
    dados = request.get_json()
    
    if not verificar_colunas(dados, COLUNAS_ANALISE_SOLO_FERTILIZANTE):
        return resposta_modelo(dados, "modelos/analise_fertilizante.sav", DICIONARIO_ANALISE_SOLO_FERTILIZANTE)
    else:
        return verificar_colunas(dados, COLUNAS_ANALISE_SOLO_FERTILIZANTE)


# Rota para a indicação de água potável (Análise de Água)
@app.route("/analise/agua/", methods=["POST"])
def previsao_agua():
    dados = request.get_json()
    
    if not verificar_colunas(dados, COLUNAS_ANALISE_AGUA):
        return resposta_modelo(dados, "modelos/analise_agua.sav", DICIONARIO_ANALISE_AGUA)
    else:
        return verificar_colunas(dados, COLUNAS_ANALISE_AGUA)


# Rota para a Recomendação de Irrigação
@app.route("/recomendacao/irrigacao/", methods = ["POST"])
def previsao_irrigacao():
    dados = request.get_json()
    if not verificar_colunas(dados, COLUNAS_RECOMENDACAO_IRRIGACAO):
        dados = list(dados.values())
        if not verificar_culturas(dados[0], DICIONARIO_CULTURAS_RECOMENDACAO_IRRIGACAO):
            dados[0] = DICIONARIO_CULTURAS_RECOMENDACAO_IRRIGACAO[dados[0]] # Transformando a string em número
            modelo = pickle.load(open("modelos/recomendacao_irrigacao.sav", "rb")) # Importando o modelo
            resultado = modelo.predict([dados]) # Prevendo o resultado
            resultado = DICIONARIO_RECOMENDACAO_IRRIGACAO[resultado[0]]
            resposta = make_response(
                jsonify(
                    {"Recomendação": f"{resultado}"}),
                200)
            resposta.headers["Content-Type"] = "application/json"
            return resposta
        else:
            return verificar_culturas(dados[0], DICIONARIO_CULTURAS_RECOMENDACAO_IRRIGACAO)
    else:
        return verificar_colunas(dados, COLUNAS_RECOMENDACAO_IRRIGACAO)


""" 
Rota para a previsão de safra

Essa rota é um pouco especial por se tratar de um caso de regressão, e não de classificação. Logo,
ao invés de fazer uso da função resposta_modelo, a predição é feita de modo "manual".

Pequena observação: o resultado do modelo é em Hectogramas por Hectare, mas o mesmo é convertido
para Kilogramas por Hectare em prol de retorna uma resposta que possibilita melhor entendimento.
"""
@app.route("/previsao/safra/", methods=["POST"])
def previsao_safra():
    dados = request.get_json()
    
    if not verificar_colunas(dados, COLUNAS_PREVISAO_SAFRA):
        dados = list(dados.values()) # Extraindo os valores

        if not verificar_culturas(dados[0], DICIONARIO_CULTURAS_PREVISAO_SAFRA):
            dados[0] = DICIONARIO_CULTURAS_PREVISAO_SAFRA[dados[0]] # Transformando a string em número
            modelo = pickle.load(open("modelos/previsao_safra.sav", "rb")) # Importando o modelo
            resultado = modelo.predict([dados]) # Prevendo o resultado
            resposta = make_response(
                jsonify(
                    {"Previsão": f"{resultado[0]/10 :.2f} Kilogramas por Hectare"}),
                200)
            resposta.headers["Content-Type"] = "application/json"
            return resposta
        else:
            return verificar_culturas(dados[0], DICIONARIO_CULTURAS_PREVISAO_SAFRA)
        
    else:
        return verificar_colunas(dados, COLUNAS_PREVISAO_SAFRA)


app.run(debug=True)
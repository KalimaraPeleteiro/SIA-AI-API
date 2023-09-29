<h1 align="center"> SIA-AI-API </h1>
<p align = "center">Um dos componentes do projeto da SIA. Uma API Flask com rotas POST que dão acesso aos modelos de Machine Learning desenvolvidos para usos na SIA.</p>

## Rotas
Todas as rotas aceitam somente métodos POST com um JSON associado. Os parâmetros de como o JSON deve ser formado variam para cada rota, e, caso ele não
se encaixe no formato adequado, uma mensagem de erro será retornada.

> **Análise de Solo - Cultura**
> <br>
> *Caminho: /analise/solo/cultura/*
> <br>
> Rota para a recomendação de cultura com base em fatores do solo e climáticos. A resposta é uma das 22 culturas listadas disponíveis.
> <br>
> <br>
> Medidas de Nitrogênio, Fósforo e Potásio em mg/m². A temperatura referida é a temperatura média, em ºC. "Umidade" refere-se a umidade do
> ar, e é medida em %. "Chuva" é o valor mensal médio, em mm.
> <br>
> <br>
> Exemplo de JSON
> ```
> {
>   "Nitrogênio": 56.7,
>   "Fósforo": 83,
>   "Potássio": 34,
>   "Temperatura": 26,
>   "Umidade": 63,
>   "pH": 4.57,
>   "Chuva": 280
> }
> ```

<br>

> **Análise de Solo - Fertilizante**
> <br>
> *Caminho: /analise/solo/fertilizante/*
> <br>
> Rota para a recomendação de fertilizantes com base em fatores do solo e climáticos. A resposta é uma dos 07 fertilizantes listadas disponíveis.
> <br>
> <br>
> Medidas de Nitrogênio, Fósforo e Potásio em mg/m². A temperatura referida é a temperatura média, em ºC, enquanto as Umidades são verificadas em %.
> <br>
> <br>
> Exemplo de JSON
> ```
> {
>   "Temperatura": 28.4,
>   "Umidade do Ar": 83,
>   "Umidade do Solo": 23.5,
>   "Nitrogênio": 65.4,
>   "Potássio": 63.2,
>   "Fósforo": 4.57
> }
> ```

<br>

> **Análise de Água**
> <br>
> *Caminho: /analise/agua/*
> <br>
> Rota para a análise de água. Com base em vários fatores de análise, a água é indicada como sendo própria ou não para consumo.
> <br>
> <br>
> Medidas minerais em mg/ml. O índice de Bactérias e Vírus é medido em mol/ml.
> <br>
> <br>
> Exemplo de JSON
> ```
> {
>   "Alumínio": 0,
>   "Amônia": 0,
>   "Arsênio": 0,
>   "Bário": 0,
>   "Cádmio": 1.5,
>   "Cloro": 0,
>   "Cromo": 1.2,
>   "Cobre": 2.4,
>   "Flúor": 4.6,
>   "Bactérias": 0,
>   "Vírus": 0,
>   "Chumbo": 12.6,
>   "Nitrato": 3.2,
>   "Nitrito": 7.6,
>   "Mercúrio": 0,
>   "Perclorato": 0,
>   "Rádio": 0,
>   "Selênio": 0,
>   "Prata": 2.3,
>   "Urânio": 0
> }
> ```

<br>

> **Recomendação - Irrigação**
> <br>
> *Caminho: /recomendacao/irrigacao/*
> <br>
> Com base no estado atual de uma cultura, bem como a própria cultua em si, a necessidade de irrigação (naquele dia) é apontada como positiva ou não.
> <br>
> <br>
> As culturas disponíveis são: Cana-de-Açúcar, Trigo, Batata, Arroz, Café, Amendoim, Flores, Milho e Vagem. Inserir qualquer cultura que não sejam estas resultará em um erro.
> <br>
> A temperatura referida é a temperatura média, em ºC, enquanto as Umidades são verificadas em %.
> <br>
> <br>
> Exemplo de JSON
> ```
> {
>   "Cultura": "Milho",
>   "Dias Ativos (Cultura)": 27,
>   "Umidade do Solo": 44.5,
>   "Temperatura": 33.8,
>   "Umidade do Ar": 78.9
> }
> ```

<br>

> **Recomendação - Pesticida**
> <br>
> *Caminho: /recomendacao/pesticida/*
> <br>
> Com base no uso de pesticidas no plantio atual, três respostas são possíveis. O uso pode ficar a descrição
> do produtor (não é nem incentivado nem desmotivado), o uso pode ser recomendado ou considerado perigoso
> para a vida do plantio.
> <br>
> <br>
> Os usos de pesticidas disponíveis são: "Nunca Usado Anteriormente", "Usado Anteriormente" e "Usando Atualmente"
> <br>
> A quantidade de insetos é medida por m².
> <br>
> <br>
> Exemplo de JSON
> ```
> {
>   "Quantidade de Insetos": 23,
>   "Uso de Pesticida": "Usando Atualmente",
>   "Número de Doses Semanais": 3,
>   "Número de Semanas de Uso": 4,
>   "Número de Semanas sem Uso": 0
> }
> ```

<br>

> **Previsão de Safra**
> <br>
> *Caminho: /previsao/safra/*
> <br>
> Tendo em vista diversos fatores e a cultura sendo produzida, uma previsão de colheita é entregue.
> <br>
> <br>
> As culturas disponíveis são: Mandioca, Milho, Batata, Arroz, Sorgo, Soja, Batata Doce, Trigo e Inhame. Inserir qualquer cultura que não sejam estas resultará em um erro.
> <br>
> A temperatura referida é a temperatura média, em ºC. A medida de chuva é em mm.
> <br>
> <br>
> Exemplo de JSON
> ```
> {
>   "Cultura": "Milho",
>   "Ano": 2023,
>   "Pesticidas (ton)": 0.08,
>   "Temperatura": 33.8,
>   "Chuva Anual": 2288
> }
> ```

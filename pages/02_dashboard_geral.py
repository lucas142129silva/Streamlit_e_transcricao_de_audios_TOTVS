import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import re
import unidecode
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import json
import time
import navbar
import streamlit as st

try:
	nltk.download("punkt")
except BrokenPipeError:
	pass

navbar.nav('Dashboard Geral')
st.title("Dashboard de Acompanhamento")


# Sucesso de transcrição
dados_semana_acuracia = pd.DataFrame(
	{
		"Dia": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
		"Acurácia de transcrição": [0.9666, 0.9814, 0.9876, 0.9767, 0.9548, 0.9889, 0.9815, 0.9689,
       0.9685, 0.9668, 0.9674, 0.9876, 0.9735, 0.9681, 0.9705, 0.975 ,
       0.9797, 0.9866, 0.9716, 0.9835, 0.9759, 0.9855, 0.9719, 0.971, 0.9657]
	}

)

# Total de áudios por dia
dados_semana_total_audio = pd.DataFrame(
	{
		"Dia": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
		"Total de áudios": [81, 81, 81, 80, 79, 80, 81, 80, 80, 79, 82, 78, 80, 80, 80, 80, 79,
       80, 79, 82, 79, 81, 79, 79, 79]
	}

)

# Dados de tempo
dados_semana_tempo_exec = pd.DataFrame(
	{
		"Dia": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
		"Tempo execução": [52.84, 51.76, 51.4 , 51.26, 51.11, 51.02, 52.03, 51.14, 53.09,
       51.12, 52.78, 51.83, 52.45, 53.14, 52.22, 52.77, 53.15, 51.47,
       51.86, 52.64, 51.88, 51.57, 52.23, 50.56, 50.92]
	}

)
tempo_medio_por_audio = dados_semana_tempo_exec["Tempo execução"].mean() / dados_semana_total_audio["Total de áudios"].mean()

# Colunas de KPIs
c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
st.markdown("----")
start_date, end_date = st.select_slider("Selecione o intervalo de data:",
                                        value=(1, 25), options=list(range(1, 26)),)
st.markdown("\n\n----")

# Filtro de data
if start_date is not None and end_date is not None:
	# Filtrar com o slider
	dados_semana_tempo_exec = dados_semana_tempo_exec[dados_semana_tempo_exec["Dia"].between(start_date, end_date)]
	dados_semana_total_audio = dados_semana_total_audio[dados_semana_total_audio["Dia"].between(start_date, end_date)]
	dados_semana_acuracia = dados_semana_acuracia[dados_semana_acuracia["Dia"].between(start_date, end_date)]


# Escreve KPIs
with c1:
	st.page_link('pages/03_analise_dos_audios.py', label='**Análise dos áudios**', icon="🔎")
	st.page_link('pages/04_analise_de_operacao.py', label='**Análise da operação**', icon="⚙️")

# KPIs
c2.metric("WER", "%.2f%%" % (dados_semana_acuracia["Acurácia de transcrição"].mean()*100))
c3.metric("Tempo de execução", "%dh%dm" %
            (dados_semana_tempo_exec["Tempo execução"].mean() // 60,
             dados_semana_tempo_exec["Tempo execução"].mean() % 60))
c4.metric("Transcrições por dia", "%.0f" % (dados_semana_total_audio["Total de áudios"].mean()))
c5.metric("Tempo médio por áudio", "%dm%ds" %
            (tempo_medio_por_audio // 1, (tempo_medio_por_audio % 1) * 60))
c6.metric("Positividade", "50.63%")
c7.metric("Negatividade", "11.39%")
c8.metric("Mensuração NPS", "62.5%")


# Segunda camada de colunas
z1, z2, z3 = st.columns(3)
with z1:
	st.markdown("\n\n###### Tempo de execução da carga diária:")
	st.line_chart(dados_semana_tempo_exec, x="Dia", y="Tempo execução", color="#025EF1")
	st.markdown("\n\n###### Total de áudios transcritos:")
	st.bar_chart(dados_semana_total_audio, x="Dia", y="Total de áudios", color="#025EF1")

st.markdown("----")


sentiment = SentimentIntensityAnalyzer()

remover_acentos = lambda x: unidecode.unidecode(x)

# Trazer as stopwords para o código
with open("stopwords", "r") as f:
	stop_words = json.load(f)

remover_stop_words = lambda x: [word for word in x if word.isalnum() and word not in stop_words]

# Possibilidades de como pode ser encontrado no texto quando mensuram
encontrar_perguntas_de_nota = ["0 a 10", "zero a 10", "0 a dez", "zero a dez"]

# Formas que as notas podem se apresentar
notas = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
         "um", "dois", "tres", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez"]

numeros_por_extenso = {
    'zero': 0, 'um': 1, 'dois': 2, 'tres': 3, 'quatro': 4, 'cinco': 5, 'seis': 6,
    'sete': 7,'oito': 8,'nove': 9,'dez': 10,
    '0': 0,'1': 1,'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,
}

# Regex para encontrar quando a nota se apresenta
notas = re.compile("(" + "|".join(notas) + ")")


def flatten_list(list_):
	output = []
	for sublist in list_:
		output.extend(sublist)

	return output

def gerar_wordcloud(texto):
	if type(texto)==list:
		texto_wordcloud = " ".join(texto)
	else:
		texto_wordcloud=texto

	wordcloud = WordCloud(width=800, height=400, background_color='white', colormap="winter").generate(texto_wordcloud)

	fig = plt.figure(figsize=(10, 5))
	plt.imshow(wordcloud)
	plt.axis('off')
	st.pyplot(fig)

def retornas_notas_de_texto(texto):
	positions_a_string_matches = list()

	# Encontrar as posições que tem a escala de 0 a 10, escrito de várias maneiras
	for nota in encontrar_perguntas_de_nota:
		p = re.compile(nota)

		for m in p.finditer(texto):
			positions_a_string_matches.append(m.start())

	notas_finais = list()

	for posicao in positions_a_string_matches:
		contexto = texto[posicao:posicao + 200]

		# Se a lista passar de 8 itens, o número significa outra coisa: telefone, CNPJ
		if len(notas.findall(contexto)) > 8:
			continue

		notas_finais.append(notas.findall(contexto))

	# Com as notas escritas por extenso, trasnformei em número e retirei o "um" (estava fazendo match com 'algum')
	notas_finais = [numeros_por_extenso[i] for i in flatten_list(notas_finais) if
	                i != "um" and i != "1" and i != "0" and i != "zero"]

	if len(notas_finais) > 0:
		return sum(notas_finais) / len(notas_finais)
	else:
		return None


# Tratamento dos dados
dados = pd.read_csv("./Áudios transcritos/Audios_transcritos_v2.csv", encoding="latin1", sep=";")

todos_os_textos = " ".join(dados["Texto transcrito"])
todos_os_textos = remover_acentos(todos_os_textos.lower())

# Tokenização e remoção de stopwords
tokens = word_tokenize(todos_os_textos)

# Retirar stop words
filtered_tokens = remover_stop_words(tokens)


# Análise de sentimento
dados["texto tratado"] = dados["Texto transcrito"].apply(remover_acentos).str.lower()
dados["texto tokenizado"] = dados["texto tratado"].apply(word_tokenize)
dados["texto tokenizado"] = dados["texto tokenizado"].apply(remover_stop_words)
dados["texto final"] = dados["texto tokenizado"].str.join(" ")

resultados_sentimento = pd.DataFrame([])
for idx, row in dados.iterrows():
	# Usando função polarity scores para pegar o sentimento do texto sem stop words
	result_sentiment = sentiment.polarity_scores(row["texto final"])

	resultado = pd.DataFrame(result_sentiment, index=[idx])
	resultados_sentimento = pd.concat([resultados_sentimento, resultado])

dados = dados.join(resultados_sentimento)



# Comparando quem mediu e quem não mediu NPS

dados["tem palavra nps"] = dados["texto tratado"].str.contains("0 a 10").astype(int)
nao_mediram_nps = dados[dados["tem palavra nps"]==0].copy()
possuem_nps = dados[dados["tem palavra nps"]==1].copy()

with z2:
	# Wordcloud diferenciando não mediu x mediu
	st.markdown("\n###### Frequência de palavras de quem não mediu NPS:")
	gerar_wordcloud(nao_mediram_nps["texto final"].tolist())

	time.sleep(1.5)

	st.markdown("\n\n\n###### Frequência de palavras de quem mediu NPS:")
	gerar_wordcloud(possuem_nps["texto final"].tolist())


# Notas médias com base nos textos
possuem_nps["nota média"] = possuem_nps["texto tratado"].apply(retornas_notas_de_texto)

time.sleep(1.5)

with z3:
	st.markdown("\n###### Wordcloud com áudios negatvios:")
	gerar_wordcloud(possuem_nps[possuem_nps["nota média"]<6]["texto final"].tolist())

	time.sleep(1.5)

	st.markdown("\n###### Wordcloud com áudios positivos:")
	gerar_wordcloud(possuem_nps[possuem_nps["nota média"]>9]["texto final"].tolist())
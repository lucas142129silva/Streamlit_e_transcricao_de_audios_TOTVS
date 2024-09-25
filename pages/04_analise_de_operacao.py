import streamlit as st
import navbar
import pandas as pd


navbar.nav('Operação')


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


st.title("Análise da operação\n")
st.markdown("\nNesta aba, são apresentados indicadores da pipeline de transcrição de áudios que rodam diariamente."
            " O objetivo é garantir a integridade da execução com o acompanhamento de acurácia do modelo de transcrição,"
            " tempo de execução médio e quantidade de áudios que foram transcritos e carregados para o banco de dados.\n\n")

start_date, end_date = st.select_slider("Selecione o intervalo de data:",
                                        value=(1, 25), options=list(range(1, 26)),)

# Filtro de data
if start_date is not None and end_date is not None:
	# Filtrar com o slider
	dados_semana_tempo_exec = dados_semana_tempo_exec[dados_semana_tempo_exec["Dia"].between(start_date, end_date)]
	dados_semana_total_audio = dados_semana_total_audio[dados_semana_total_audio["Dia"].between(start_date, end_date)]
	dados_semana_acuracia = dados_semana_acuracia[dados_semana_acuracia["Dia"].between(start_date, end_date)]

tempo_medio_por_audio = dados_semana_tempo_exec["Tempo execução"].mean() / dados_semana_total_audio["Total de áudios"].mean()

# Principais KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("WER", "%.2f%%" % (dados_semana_acuracia["Acurácia de transcrição"].mean()*100))
col2.metric("Tempo de execução", "%dh%dm" %
            (dados_semana_tempo_exec["Tempo execução"].mean() // 60,
             dados_semana_tempo_exec["Tempo execução"].mean() % 60))
col3.metric("Transcrições por dia", "%.0f" % (dados_semana_total_audio["Total de áudios"].mean()))
col4.metric("Tempo médio por áudio", "%dm%ds" %
            (tempo_medio_por_audio // 1, (tempo_medio_por_audio % 1) * 60))

st.markdown("----")

st.markdown("### Média de WER (acurácia da transcrição):")
st.markdown("Média de WER: **%.2f%%**" % (dados_semana_acuracia["Acurácia de transcrição"].mean()*100))
st.line_chart(dados_semana_acuracia, x="Dia", y="Acurácia de transcrição", color="#025EF1")
st.markdown("----")

st.markdown("\n\n### Média de tempo de execução da carga diária:")
st.markdown("Média de tempo de execução: **%d horas e %d minutos**" %
            (dados_semana_tempo_exec["Tempo execução"].mean() // 60, dados_semana_tempo_exec["Tempo execução"].mean() % 60))
st.bar_chart(dados_semana_tempo_exec, x="Dia", y="Tempo execução", color="#025EF1")
st.markdown("----")

st.markdown("\n\n### Média de áudios transcritos por dia:")
st.markdown("Média de áudios transcritos por dia: **%.0f**" % (dados_semana_total_audio["Total de áudios"].mean()))
st.bar_chart(dados_semana_total_audio, x="Dia", y="Total de áudios", color="#025EF1")
st.markdown("----")

st.markdown("\nO tempo médio por áudio transcrito é de **%d minutos e %d segundos**" %
            (tempo_medio_por_audio // 1, (tempo_medio_por_audio % 1) * 60))

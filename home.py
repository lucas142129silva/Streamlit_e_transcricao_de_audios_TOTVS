import streamlit as st
import navbar

# Adiciona a imagem de fundo na barra lateral
# st.sidebar.image("Logologo.png", use_column_width=True)

# Display the menu
navbar.nav('Home')

# Interface do Streamlit
st.title("💬 Sobre o :blue[EchoShift]      ")
st.text("")
st.text("")

# Escrever o resto
st.markdown("**EchoShift** é uma Solução automatizada para transcrição e análise de chamadas que converte áudio em texto rapidamente e aplica a inteligência artifical para identificar padrões, emoções e áreas de melhoria")
st.text("")
st.text("")
st.markdown("**Um pouco sobre o desenvolvimento:**")
st.markdown("Utilizamos Notebooks do Kaggle para processamento dos códigos, pois eles possuem uma ferramenta de schedule diário e usam máquinas com GPU,  também fornecem 30h grátis semanais, gerando uma solução rápida, potente, sem custo e que atende a média de 80 áudios por dia.")
st.markdown("Todos os códigos foram desenvolvidos pela nossa equipe, em python.")
st.markdown("Após o tratamento e processamento dos dados, optamos por prototipar a solução com Streamlit. Essa ferramenta gratuita possibilita a execução de modelos de análise de sentimento, além de fornecer uma plataforma interativa para visualização dos resultados, unindo praticidade e eficiência no desenvolvimento e apresentação.")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.markdown("💻 Desenvolvido por: Lucas Vitorino, Marcella Arícia, Danilo Souza e Gabriela Moreno")
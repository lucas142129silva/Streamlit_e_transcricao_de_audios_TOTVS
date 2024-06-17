import streamlit as st
import navbar
from github import Github
import time, os, json, shutil, subprocess

navbar.nav('Transcrição')

# Chave github API
TOKEN_GITHUB = st.secrets["token_github"]


def remove_prefix(list_of_strings: list, prefix: str) -> list:
	return [item[len(prefix):] if item.startswith(prefix)
	        else item for item in list_of_strings]


def rodar_notebook_kaggle():
	notebook_name = "lucas142129silva/teste-kaggle-api"

	ntbk_name = notebook_name.split("/")[1]
	krnl_mtdt_dir = os.path.join("./Metadados_notebooks/", ntbk_name)

	while os.path.exists(krnl_mtdt_dir):
		krnl_mtdt_dir = os.path.join(krnl_mtdt_dir, ntbk_name)

	os.mkdir(krnl_mtdt_dir)

	response = subprocess.run(["kaggle", "kernels", "pull", "-p",
	                           krnl_mtdt_dir, "-m", notebook_name],
	                          capture_output=True)

	krnl_mtdt_file = os.path.join(krnl_mtdt_dir, "kernel-metadata.json")
	orig_krnl_mtdt_file = os.path.join(krnl_mtdt_dir, "kernel-metadata.json.old")
	os.rename(krnl_mtdt_file, orig_krnl_mtdt_file)

	with open(orig_krnl_mtdt_file, "r") as file:
		metadata = json.load(file)

	metadata["dataset_sources"] = remove_prefix(metadata["dataset_sources"], "datasets/")
	metadata["kernel_sources"] = remove_prefix(metadata["kernel_sources"], "code/")

	metadata["enable_internet"] = True
	with open(krnl_mtdt_file, "w") as file:
		metadata = json.dump(metadata, file)

	response = subprocess.run(["kaggle", "kernels", "push", "-p", krnl_mtdt_dir],
	                          capture_output=True)

	shutil.rmtree("./Metadados_notebooks/" + ntbk_name)

	time.sleep(5)


g = Github(TOKEN_GITHUB)
repo = g.get_user().get_repo("KaggleTest")
contents = repo.get_contents("/EntradasAudios")

id_entrada_audio = str(int(contents[0].download_url.split("/")[-1].split("_")[0]) - 1)

# Página
st.title("Transcrição")

uploaded_file = st.file_uploader("Escolha um audio",
                                 type=[".wav", ".mp3"],
                                 accept_multiple_files=False)

if uploaded_file is not None:
	audio_bytes = uploaded_file.read()

	# Enviar arquivo para github
	git_file = "EntradasAudios/" + id_entrada_audio + "_" + uploaded_file.name.split(".")[0] + "_audio" + uploaded_file.name.split(".")[-1]
	repo.create_file(git_file, "committing files", audio_bytes, branch="main")
	st.text(git_file + ' CREATED')

	rodar_notebook_kaggle()

	st.text("Carregando... Sua transcrição já está processando!")

	inicio=time.time()

	# Valor padrão
	transcricao = ""
	arquivo_com_transcricao = id_entrada_audio + "_" + uploaded_file.name.split(".")[0] + "_audio.txt"

	arquivo_de_saida_no_github = False

	# Vai atualizar a cada 1 segundo, e vai retornar a transcrição quando encontrar o arquivo na saida no repositório
	while not arquivo_de_saida_no_github:
		saidas_transcricoes = repo.get_contents("/SaidasTranscricoes")
		for saida in saidas_transcricoes:
			if arquivo_com_transcricao in saida.download_url:
				transcricao = saida.decoded_content.decode("UTF-8")
				arquivo_de_saida_no_github = True
				break

		time.sleep(1)

	tempo_total = time.time() - inicio

	st.text("Transcrição efetuada com sucesso em %d minutos e %d segundos!" % (tempo_total // 60, tempo_total % 60))
	st.markdown(transcricao)
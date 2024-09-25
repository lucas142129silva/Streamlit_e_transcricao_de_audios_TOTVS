import streamlit as st
from streamlit_option_menu import option_menu

# Define the pages and their file paths
pages = {'Home': 'home.py',
         'Transcrição': 'pages/01_pagina_de_upload_e_transcricao.py',
         'Dashboard Geral': 'pages/02_dashboard_geral.py',
         'Análises': 'pages/03_analise_dos_audios.py',
         'Operação': 'pages/04_analise_de_operacao.py'}

# Create a list of the page names
page_list = list(pages.keys())


def nav(current_page=page_list[0]):
	with st.sidebar:
		st.set_page_config(page_title="EchoShift", page_icon="iphone", layout="centered", initial_sidebar_state="auto",
		                   menu_items=None)

		st.sidebar.image("Logologo.png", use_column_width=True)
		p = option_menu("", page_list,
		                default_index=page_list.index(current_page),
		                orientation="vertical",
		                icons=["house", "telephone", "thermometer", "gear"],
		                styles={
			                "container": {"padding": "0!important", "background-color": "#beceea"},
			                "icon": {"font-size": "25px"},
			                "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
			                             "--hover-color": "#eee"},
			                "nav-link-selected": {"background-color": "blue"},
		                }
		                )

		if current_page != p:
			st.switch_page(pages[p])
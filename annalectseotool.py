# File: annalectseotool.py (o il tuo file principale)
import streamlit as st

# 1. Configurazione pagina (DEVE essere il primo comando Streamlit)
try:
    st.set_page_config(page_title="Test Super Minimale", layout="wide")
except Exception as e_cfg:
    st.error(f"Errore FATALE durante st.set_page_config: {e_cfg}")
    st.exception(e_cfg) # Mostra traceback nell'app
    print(f"ERRORE FATALE in set_page_config: {e_cfg}") # Logga anche su console
    st.stop()

# 2. Stampa la versione di Streamlit per conferma ASSOLUTA
try:
    version_str = f"Streamlit Version CONFERMATA in uso: {st.__version__}"
    st.sidebar.title("Diagnosi Ambiente") # Usa la sidebar per non interferire con set_page_config
    st.sidebar.success(version_str)
    print(version_str) # Logga anche su console
except Exception as e_ver:
    st.sidebar.error(f"Errore nel mostrare la versione: {e_ver}")
    print(f"ERRORE nel mostrare la versione: {e_ver}")

# 3. Definisci una funzione pagina semplicissima
def pagina_test_semplice():
    st.title("Pagina di Test Semplice")
    st.write("Se vedi questo, la pagina è stata caricata.")
    st.balloons()

# 4. Tenta di usare st.navigation con st.Page e 'group'
try:
    st.sidebar.write("Tentativo di creare st.navigation...")
    pg = st.navigation([
        st.Page(pagina_test_semplice, title="Test Page", icon="🧪", group="TestGroup")
    ])
    st.sidebar.info("st.navigation con 'group' creato con successo!")
    print("st.navigation con 'group' creato con successo!")
except Exception as e_nav:
    st.sidebar.error(f"Errore CRITICO durante st.navigation: {type(e_nav).__name__}")
    st.sidebar.code(str(e_nav)) # Mostra l'errore specifico nella sidebar
    st.exception(e_nav) # Mostra traceback completo nell'app
    print(f"ERRORE CRITICO in st.navigation: {type(e_nav).__name__} - {e_nav}")
    st.stop() # Interrompi se la navigazione fallisce

# 5. Esegui la navigazione
try:
    st.sidebar.write("Tentativo di eseguire pg.run()...")
    pg.run()
    # Non aggiungere st.write qui fuori, pg.run() controlla il contenuto principale
    print("pg.run() eseguito.")
except Exception as e_run:
    st.sidebar.error(f"Errore CRITICO durante pg.run(): {type(e_run).__name__}")
    st.sidebar.code(str(e_run))
    st.exception(e_run)
    print(f"ERRORE CRITICO in pg.run(): {type(e_run).__name__} - {e_run}")
    st.stop()

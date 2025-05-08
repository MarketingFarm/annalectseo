import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO

# --- Configurazione della Pagina (DEVE ESSERE IL PRIMO COMANDO STREAMLIT) ---
st.set_page_config(
    page_title="Multi-Tool Dashboard SEO",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Stili CSS Personalizzati ---
st.markdown("""
<style>
    /* Colora la progress bar */
    .stProgress > div > div > div { background-color: #f63366 !important; }

    /* Stile per il logo nella sidebar */
    .sidebar-logo {
        text-align: center;
        margin-bottom: 20px;
        margin-top: 10px;
    }
    .sidebar-logo img {
        width: 60px;
    }
    /* Rimuove padding eccessivo dalla sidebar se necessario */
    [data-testid="stSidebarNav"] {
        padding-top: 0rem; /* Riduci padding in cima al menu di navigazione */
    }
</style>
""", unsafe_allow_html=True)

# --- Funzioni dei Tool ---
BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive"
}

def estrai_info_seo(url):
    """Estrae informazioni SEO da un URL."""
    data = {
        "URL": url, "H1": "N/D", "H2": "N/D", "Meta title": "N/D",
        "Meta title length": 0, "Meta description": "N/D",
        "Meta description length": 0, "Canonical": "N/D", "Meta robots": "N/D"
    }
    try:
        current_url_to_process = url 
        url_to_request = url
        if not url.startswith("http://") and not url.startswith("https://"):
            url_to_request = "https://" + url # Default a https per URL senza schema

        resp = requests.get(url_to_request, headers=BASE_HEADERS, timeout=15, allow_redirects=True)
        resp.raise_for_status() 
        
        # Aggiorna l'URL nel dizionario se c'è stato un redirect
        data["URL"] = resp.url if resp.url != url_to_request else current_url_to_process
        
        soup = BeautifulSoup(resp.content, "html.parser")

        h1_tag = soup.find("h1")
        if h1_tag: data["H1"] = h1_tag.get_text(strip=True)
        
        h2_tags = soup.find_all("h2")
        if h2_tags:
            h2_texts = [h.get_text(strip=True) for h in h2_tags if h.get_text(strip=True)]
            if h2_texts: data["H2"] = " | ".join(h2_texts)
        
        title_tag = soup.title
        if title_tag:
            data["Meta title"] = title_tag.get_text(strip=True)
            data["Meta title length"] = len(data["Meta title"])
        
        description_tag = soup.find("meta", attrs={"name": "description"})
        if description_tag and description_tag.has_attr("content"):
            data["Meta description"] = description_tag["content"].strip()
            data["Meta description length"] = len(data["Meta description"])
        
        canonical_tag = soup.find("link", rel="canonical")
        if canonical_tag and canonical_tag.has_attr("href"): data["Canonical"] = canonical_tag["href"].strip()
        
        robots_tag = soup.find("meta", attrs={"name": "robots"})
        if robots_tag and robots_tag.has_attr("content"): data["Meta robots"] = robots_tag["content"].strip()
        
        return data

    except requests.exceptions.RequestException as e:
        # Mostra un warning più conciso nell'interfaccia utente
        st.warning(f"Errore di richiesta per {current_url_to_process}: {type(e).__name__}. Controlla i log per dettagli.")
        # Logga l'errore completo per il debug (visibile nei log di Streamlit Cloud)
        print(f"RequestException for {current_url_to_process}: {e}")
        for key in data: # Popola i campi con un messaggio di errore
            if key != "URL": data[key] = f"Errore Richiesta"
        data["URL"] = current_url_to_process # Mantieni l'URL originale per riferimento
        return data
    except Exception as e:
        st.warning(f"Errore generico per {current_url_to_process}: {type(e).__name__}. Controlla i log per dettagli.")
        print(f"Generic Exception for {current_url_to_process}: {e}")
        for key in data:
            if key != "URL": data[key] = f"Errore Analisi"
        data["URL"] = current_url_to_process
        return data

def pagina_seo_extractor():
    """Pagina per il tool SEO Extractor."""
    st.title("🔍 SEO Extractor")
    st.markdown("Estrai H1, H2, Meta title/length, Meta description/length, Canonical e Meta robots da una lista di URL.")
    st.divider()

    col1_input, col2_options = st.columns([0.65, 0.35], gap="large")

    with col1_input:
        urls_input_str = st.text_area(
            "Incolla gli URL (uno per riga)",
            height=280,
            placeholder="esempio.com/pagina1\nwww.altroesempio.it/articolo\nmiosito.org/contatti",
            label_visibility="collapsed"
        )
        st.caption("Puoi incollare URL con o senza `http://` o `https://`.")

    campi_disponibili = [
        "H1", "H2", "Meta title", "Meta title length",
        "Meta description", "Meta description length", "Canonical", "Meta robots"
    ]
    # 'URL' è gestito separatamente e aggiunto sempre, qui solo i campi SEO specifici
    default_seo_fields = ["H1", "Meta title", "Meta description", "Canonical"] 

    with col2_options:
        st.subheader("Campi SEO da Estrarre")
        campi_selezionati_utente = st.multiselect(
            "Seleziona i campi:",
            options=campi_disponibili, # L'utente seleziona solo i campi SEO specifici
            default=default_seo_fields,
            label_visibility="collapsed"
        )
        st.caption("L'URL (finale, dopo i redirect) verrà sempre mostrato.")

    if st.button("🚀 Avvia Estrazione", type="primary", use_container_width=True):
        urls_raw = [u.strip() for u in urls_input_str.splitlines() if u.strip()]
        
        if not urls_raw:
            st.error("Inserisci almeno un URL.")
            return
        # Non è necessario controllare campi_selezionati_utente se vogliamo che alcuni siano sempre estratti
        # o se l'URL è sempre incluso. Se la selezione può essere vuota e ciò è un problema, aggiungere controllo.

        progress_bar = st.progress(0, text="Inizializzazione analisi...")
        results_list = []
        total_urls = len(urls_raw)
        status_placeholder = st.empty()

        for i, url_originale in enumerate(urls_raw):
            percent_complete = (i + 1) / total_urls
            status_placeholder.text(f"Analizzando: {url_originale} ({i+1}/{total_urls})")
            progress_bar.progress(percent_complete, text=f"Analisi in corso... {int(percent_complete*100)}%")
            
            info_seo = estrai_info_seo(url_originale)
            
            # Costruisci la riga dei risultati: sempre l'URL, più i campi SEO selezionati
            riga_risultati = {"URL": info_seo.get("URL", url_originale)} # Prendi l'URL finale da info_seo
            for campo in campi_selezionati_utente: # Itera solo sui campi SEO selezionati
                riga_risultati[campo] = info_seo.get(campo, "N/D")
            results_list.append(riga_risultati)

        status_placeholder.empty()
        progress_bar.empty()

        if results_list:
            st.success(f"Estrazione completata per {len(results_list)} URL.")
            st.balloons()

            df = pd.DataFrame(results_list)
            
            # Ordina le colonne: URL per primo, poi i campi SEO selezionati nell'ordine di selezione
            colonne_ordinate = ["URL"] + [c for c in campi_selezionati_utente if c in df.columns and c != "URL"]
            df_display = df[colonne_ordinate]

            st.dataframe(df_display, use_container_width=True, hide_index=True)

            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_display.to_excel(writer, index=False, sheet_name='Estrazione SEO')
            excel_data = output.getvalue()
            st.download_button(
                label="📥 Download Report (XLSX)",
                data=excel_data,
                file_name=f"estrazione_seo_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.warning("Nessun dato è stato estratto. Controlla gli URL o i messaggi di avviso sopra.")

def pagina_placeholder(tool_name="Tool Placeholder", icon="🛠️", group_name="N/D"):
    """Pagina placeholder generica per altri tool."""
    st.title(f"{icon} {tool_name}")
    st.subheader(f"Sezione: {group_name}") 
    st.info(f"Questa è una pagina placeholder per il tool: **{tool_name}**.")
    st.write("Il contenuto specifico per questo tool verrà implementato qui.")
    st.image("https://via.placeholder.com/800x300.png?text=Contenuto+del+Tool+in+Arrivo",
             caption=f"Immagine placeholder per {tool_name}")

# --- Sidebar e Navigazione (CON 'group' per Streamlit >= 1.33.0) ---
with st.sidebar:
    st.markdown(
        '<div class="sidebar-logo">'
        '<img src="https://i.ibb.co/0yMG6kDs/logo.png" alt="Logo"/>' # Assicurati che l'URL sia accessibile
        '</div>',
        unsafe_allow_html=True
    )

    # NOTA: La seguente navigazione usa 'group' e richiede Streamlit 1.33.0+
    pg = st.navigation(
        [
            st.Page(pagina_seo_extractor, title="SEO Extractor", icon="🔍", group="On-Page SEO"),
            st.Page(lambda: pagina_placeholder("Struttura Dati", icon="📝", group_name="On-Page SEO"), title="Struttura Dati", icon="📝", group="On-Page SEO"),
            st.Page(lambda: pagina_placeholder("Analisi Contenuto", icon="📰", group_name="On-Page SEO"), title="Analisi Contenuto", icon="📰", group="On-Page SEO"),

            st.Page(lambda: pagina_placeholder("Verifica Robots.txt", icon="🤖", group_name="Technical SEO"), title="Verifica Robots.txt", icon="🤖", group="Technical SEO"),
            st.Page(lambda: pagina_placeholder("Analisi Sitemap", icon="🗺️", group_name="Technical SEO"), title="Analisi Sitemap", icon="🗺️", group="Technical SEO"),
            st.Page(lambda: pagina_placeholder("Controllo Redirect", icon="↪️", group_name="Technical SEO"), title="Controllo Redirect", icon="↪️", group="Technical SEO"),

            st.Page(lambda: pagina_placeholder("Analisi Backlink", icon="🔄", group_name="Off-Page SEO"), title="Analisi Backlink", icon="🔄", group="Off-Page SEO"),
            st.Page(lambda: pagina_placeholder("Ricerca Menzioni", icon="🗣️", group_name="Off-Page SEO"), title="Ricerca Menzioni", icon="🗣️", group="Off-Page SEO"),
        ]
    )

# --- Esegui la Pagina Selezionata ---
pg.run()

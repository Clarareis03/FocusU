def carregar_css():
    return """
<style>
/* Força a cor roxa em TODOS os botões primários (incluindo o formulário) */
button[kind="primary"], 
div[data-testid="stForm"] button {
    background-color: #6C5CE7 !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

/* Efeito ao passar o mouse por cima (hover) */
button[kind="primary"]:hover, 
div[data-testid="stForm"] button:hover {
    background-color: #5A4AD1 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(108, 92, 231, 0.4) !important;
}
/* ==========================================================
   1. ESTRUTURA GERAL DA APLICAÇÃO
   ========================================================== */
.stApp {
    background: #1F1F1F;
}

/* Títulos Globais */
h1 {
    color: #FFFFFF !important;
    font-size: 52px;
    font-weight: 800;
}

h2, h3 {
    color: #A29BFE !important;
}

/* Textos e Links Globais */
p, label, span {
    color: #ECECEC;
}

a {
    color: #A29BFE !important;
}

/* ==========================================================
   2. HEADER (Barra Superior com Linha Colorida)
   ========================================================== */
header[data-testid="stHeader"] {
    background-color: #0E1117 !important;
    border-bottom: 1px solid #1F1F1F;
}

header[data-testid="stHeader"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 8px; /* Espessura da linha colorida */
    background: linear-gradient(90deg, #00C6FF 0%, #0072FF 30%, #8A2BE2 65%, #E024C3 100%);
    z-index: 99999;
}

/* ==========================================================
   3. SIDEBAR (Remoção total das bolinhas + Menu Estilizado)
   ========================================================== */
[data-testid="stSidebar"], section[data-testid="stSidebar"] {
    background-color: #121214 !important;
    border-right: 1px solid #1F1F23 !important;
}

[data-testid="stSidebar"] > div:first-child {
    background-color: transparent;
}

/* Esconde totalmente a bolinha do radio button no Streamlit */
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {
    display: none !important;
    width: 0px !important;
    height: 0px !important;
    opacity: 0 !important;
}

/* Estilo das opções do menu na sidebar */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    color: #A0A0B0 !important;
    padding: 10px 14px !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    margin-bottom: 4px !important;
    background-color: transparent !important;
}

/* Hover na Sidebar */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background-color: #1E1B2E !important;
    color: #FFFFFF !important;
}

/* Item Ativo (Selecionado) na Sidebar */
[data-testid="stSidebar"] .stRadio div[aria-checked="true"] + label {
    background: linear-gradient(90deg, #2D1B4E 0%, #1A122B 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #6C5CE7 !important;
    box-shadow: 0 0 12px rgba(108, 92, 231, 0.3) !important;
    font-weight: bold !important;
}

/* ==========================================================
   4. COMPONENTES NATIVOS DO STREAMLIT
   ========================================================== */
/* Botões */
.stButton > button {
    background: #6C5CE7;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px;
    font-weight: bold;
}

.stButton > button:hover {
    background: #8B7BFF;
}

/* Inputs */
.stTextInput input {
    border-radius: 8px;
}

/* Metric Container */
div[data-testid="metric-container"] {
    background: #2D3436;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #6C5CE7;
}

/* Containers com Borda / Modais */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
    border: 1px solid #6C5CE7 !important;
    background: #2D3436 !important;
    padding: 15px;
}

/* ==========================================================
   5. CARDS CUSTOMIZADOS E BANNER HERO
   ========================================================== */
/* Cards Numéricos (Métricas rápidas) */
.card {
    background: #1E1E1E;
    border: 1px solid #6C5CE7;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    transition: 0.3s;
    height: 170px;
}

.card:hover {
    transform: translateY(-5px);
    border-color: #A29BFE;
    box-shadow: 0 0 18px rgba(108, 92, 231, .35);
}

.card-icon {
    font-size: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.card-title {
    font-size: 18px;
    color: #B2BEC3;
}

.card-value {
    font-size: 42px;
    color: white;
    font-weight: bold;
}

/* Cards de Funcionalidades */
.feature-card {
    background: #1E1E1E;
    border: 1px solid rgba(108, 92, 231, .35);
    border-radius: 18px;
    padding: 28px;
    height: 220px;
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-8px);
    border: 1px solid #A29BFE;
    box-shadow: 0 12px 30px rgba(108, 92, 231, .25);
}

.feature-icon {
    font-size: 0;
    line-height: 0;
    margin-bottom: 12px;
}

.feature-title {
    font-size: 22px;
    font-weight: 700;
    color: white;
    margin-bottom: 10px;
}

.feature-text {
    color: #B2BEC3;
    font-size: 15px;
    line-height: 1.5;
}

.feature-link {
    margin-top: 18px;
    color: #A29BFE;
    font-weight: bold;
}

/* Banner Hero Ajustado com Fundo Escuro + Glow Roxo */
.hero {
    background: linear-gradient(135deg, #161026 0%, #0D0917 100%) !important;
    border: 1px solid #6C5CE7 !important;
    border-radius: 20px !important;
    padding: 30px !important;
    margin-bottom: 25px !important;
    color: white !important;
    box-shadow: 0 0 25px rgba(108, 92, 231, 0.45) !important;
}

.hero h1, .hero h3 {
    color: #A29BFE !important;
    margin-bottom: 8px !important;
}

.hero p {
    font-size: 14px !important;
    color: #E2E2E2 !important;
    margin-bottom: 8px !important;
}

.hero small {
    color: #D6C7FF !important;
    font-size: 13px !important;
    opacity: 1 !important;
}
</style>
"""
def carregar_css():
    return """
<style>

/* Fundo */
.stApp{
    background-color:#1E1E1E;
    color:white;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#2D3436;
}

/* Títulos */

h1,h2,h3{
    color:white;
}

/* Botões */

.stButton>button{

    background:#6C5CE7;

    color:white;

    border:none;

    border-radius:12px;

    padding:10px;

    font-weight:bold;

    width:100%;

}

.stButton>button:hover{

    background:#A29BFE;

}

/* Inputs */

.stTextInput input{

    background:#2D3436;

    color:white;

    border-radius:10px;

}

/* Select */

.stSelectbox{

    color:white;

}

/* Métricas */

[data-testid="metric-container"]{

    background:#2D3436;

    border-radius:15px;

    padding:15px;

}

</style>
"""
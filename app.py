import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------
# 1. CONFIGURAÇÃO INICIAL
# --------------------------------------------------------------------------
st.set_page_config(page_title="Portal Green Express", page_icon="💚", layout="wide") 
# Mudei layout para "wide" para caber tudo na mesma linha melhor

# --------------------------------------------------------------------------
# 2. DESIGN E PERSONALIZAÇÃO (CSS AVANÇADO)
# --------------------------------------------------------------------------
def local_css():
    st.markdown("""
        <style>
        /* Fundo e cores gerais */
        .stApp {
            background-color: #0e1117 !important;
            color: #ffffff !important;
        }
        
        /* Ajuste do Título para ficar alinhado com a Logo */
        .titulo-principal {
            font-family: 'Helvetica', sans-serif;
            font-weight: 700;
            color: #ffffff;
            font-size: 32px;
            padding-top: 10px; /* Ajuste fino vertical */
            margin-bottom: 0px;
        }
        .subtitulo {
            color: #00cc66;
            font-size: 18px;
            font-weight: 400;
            margin-top: -5px;
        }

        /* --- ALINHAMENTO DO FORMULÁRIO DE LOGIN --- */
        /* Isso faz o botão descer um pouco para alinhar com as caixas de texto */
        div[data-testid="stForm"] .stButton {
            margin-top: 28px;
        }
        
        /* Estilo dos Inputs */
        div[data-testid="stTextInput"] input {
            background-color: #262730 !important;
            color: #ffffff !important;
            border: 1px solid #4b5563 !important;
        }
        
        /* Estilo do Botão */
        button[kind="primary"] {
            background-color: #00cc66 !important;
            border: none !important;
            color: #000000 !important;
            font-weight: bold !important;
            width: 100%; /* Botão preenche a coluna */
        }
        button[kind="primary"]:hover {
            background-color: #00e673 !important;
        }

        /* Cartões de Métricas */
        div[data-testid="stMetric"] {
            background-color: #1f2937 !important;
            border: 1px solid #00cc66 !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
            color: #ffffff !important;
        }
        </style>
        """, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 3. CARREGAMENTO DE DADOS
# --------------------------------------------------------------------------
ARQUIVO_VENDAS = 'vendas.csv'
ARQUIVO_USUARIOS = 'usuario.csv'
PORCENTAGEM_COMISSAO_PADRAO = 20.0 

@st.cache_data
def carregar_dados():
    try:
        df_vendas = pd.read_csv(ARQUIVO_VENDAS)
        df_usuarios = pd.read_csv(ARQUIVO_USUARIOS)
        df_usuarios['cupom'] = df_usuarios['cupom'].astype(str).str.upper().str.strip()
        df_usuarios['senha'] = df_usuarios['senha'].astype(str).str.strip()
        return df_vendas, df_usuarios
    except Exception:
        return None, None

# --------------------------------------------------------------------------
# 4. PROGRAMA PRINCIPAL
# --------------------------------------------------------------------------
def main():
    local_css()
    
    # --- CABEÇALHO EM UMA LINHA (LOGO + TEXTO) ---
    # Coluna 1 (Pequena) para Logo | Coluna 2 (Grande) para Texto
    col_logo, col_texto = st.columns([1, 6])
    
    with col_logo:
        try:
            st.image("logo.png", width=100) # Ajuste a largura conforme sua logo
        except:
            st.header("💚")

    with col_texto:
        st.markdown("""
            <div class='titulo-principal'>Portal Green Express</div>
            <div class='subtitulo'>Área Exclusiva de Parceiras</div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    df_vendas, df_usuarios = carregar_dados()

    if df_vendas is None or df_usuarios is None:
        st.error("⚠️ Erro: Arquivos 'vendas.csv' ou 'usuario.csv' não encontrados.")
        st.stop()

    # --- LÓGICA DE ESTADO ---
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
        st.session_state['usuario_atual'] = ''

    # --- TELA DE LOGIN (TUDO EM UMA LINHA) ---
    if not st.session_state['logado']:
        
        with st.form("login_form"):
            st.write("Acesso Rápido:")
            # Cria 3 colunas: Cupom | Senha | Botão
            c1, c2, c3 = st.columns([3, 3, 2])
            
            with c1:
                cupom_input = st.text_input("Cupom").strip().upper()
            with c2:
                senha_input = st.text_input("Senha", type="password").strip()
            with c3:
                # O CSS lá em cima alinha este botão com as caixas de texto
                botao_entrar = st.form_submit_button("Acessar", type="primary")

        if botao_entrar:
            usuario_valido = df_usuarios[
                (df_usuarios['cupom'] == cupom_input) & 
                (df_usuarios['senha'] == senha_input)
            ]

            if not usuario_valido.empty:
                st.session_state['logado'] = True
                st.session_state['usuario_atual'] = cupom_input
                st.rerun()
            else:
                st.error("Dados inválidos.")

    # --- PAINEL LOGADO (RESULTADOS) ---
    else:
        cupom_ativo = st.session_state['usuario_atual']
        
        # Barra superior alinhada
        c_topo1, c_topo2 = st.columns([6, 1])
        c_topo1.success(f"Logada como: **{cupom_ativo}**")
        if c_topo2.button("Sair"):
            st.session_state['logado'] = False
            st.rerun()

        # Processamento
        coluna_codigo = 'código' 
        if 'código' not in df_vendas.columns and 'Codigo' in df_vendas.columns:
            coluna_codigo = 'Codigo'

        dados_vendas = df_vendas[df_vendas[coluna_codigo] == cupom_ativo]

        st.markdown("### 📊 Seus Resultados")
        
        if not dados_vendas.empty:
            vendas = dados_vendas['valor_total_das_vendas'].values[0]
            qtd = dados_vendas['quantidade'].values[0]
            comissao = vendas * (PORCENTAGEM_COMISSAO_PADRAO / 100)

            m1, m2, m3 = st.columns(3)
            m1.metric("Vendas Totais", f"R$ {vendas:,.2f}")
            m2.metric("Quantidade", f"{qtd}")
            m3.metric("Comissão (20%)", f"R$ {comissao:,.2f}")
        else:
            st.info("Sem vendas registradas no momento.")
            m1, m2, m3 = st.columns(3)
            m1.metric("Vendas", "R$ 0,00")
            m2.metric("Qtd", "0")
            m3.metric("Comissão", "R$ 0,00")

    # Admin
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Admin"):
        if st.text_input("Senha") == "admin123":
            st.dataframe(df_vendas)

if __name__ == "__main__":
    main()

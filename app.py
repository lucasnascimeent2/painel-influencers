import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------
# 1. CONFIGURAÇÃO INICIAL
# --------------------------------------------------------------------------
st.set_page_config(page_title="Portal Green Express", page_icon="💚", layout="centered")

# --------------------------------------------------------------------------
# 2. DESIGN E PERSONALIZAÇÃO (CSS AVANÇADO)
# --------------------------------------------------------------------------
def local_css():
    st.markdown("""
        <style>
        /* Fundo e cores gerais */
        .stApp {
            background-color: #0a0a0a !important;
            color: #ffffff !important;
        }
        
        /* Logo e Título */
        .header-container {
            text-align: center;
            padding: 30px 0 20px 0;
        }
        .logo-img {
            max-width: 150px;
            margin: 0 auto;
            display: block;
        }
        .subtitulo {
            color: #00cc66;
            font-size: 16px;
            font-weight: 400;
            margin-top: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Pódio de Ranking - TEXTO SIMPLES */
        .podium-container {
            background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
            border-radius: 15px;
            padding: 30px 20px;
            margin: 20px 0;
            border: 1px solid #00cc66;
        }
        .podium-title {
            color: #ffffff;
            font-size: 20px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 25px;
        }
        .podium-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 15px;
            max-width: 600px;
            margin: 0 auto;
        }
        .podium-card {
            background: #2a2a2a;
            border-radius: 10px;
            padding: 20px 15px;
            text-align: center;
            border: 2px solid;
        }
        .podium-card-1 { border-color: #FFD700; }
        .podium-card-2 { border-color: #C0C0C0; }
        .podium-card-3 { border-color: #CD7F32; }
        
        .podium-position {
            font-size: 48px;
            font-weight: 700;
            margin: 5px 0;
        }
        .podium-cupom {
            color: #00cc66;
            font-weight: 600;
            font-size: 15px;
            margin: 10px 0 8px 0;
        }
        .podium-value {
            color: #ffffff;
            font-size: 14px;
            font-weight: 500;
        }

        /* Card de Resultados */
        .result-card {
            background: linear-gradient(135deg, #1f1f1f 0%, #151515 100%);
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            border: 1px solid #333;
        }
        .result-title {
            color: #ffffff;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 20px;
            text-align: center;
        }
        .metric-box {
            background: #0a0a0a;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin: 10px 0;
            border: 1px solid #00cc66;
        }
        .metric-label {
            color: #888;
            font-size: 14px;
            margin-bottom: 8px;
        }
        .metric-value {
            color: #ffffff;
            font-size: 28px;
            font-weight: 700;
        }
        .metric-value-green {
            color: #00cc66;
            font-size: 32px;
            font-weight: 700;
        }

        /* Seção de Dados Pessoais */
        .personal-data {
            background: #1a1a1a;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border: 1px solid #333;
        }
        .data-title {
            color: #00cc66;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 15px;
            text-align: center;
        }
        .data-item {
            background: #0a0a0a;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid #333;
        }
        .data-label {
            color: #888;
            font-size: 12px;
            margin-bottom: 5px;
        }
        .data-value {
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
            word-break: break-all;
        }

        /* Formulário de Login */
        .login-container {
            max-width: 500px;
            margin: 50px auto;
            padding: 30px;
            background: #1a1a1a;
            border-radius: 15px;
            border: 1px solid #00cc66;
        }
        
        /* Inputs */
        div[data-testid="stTextInput"] input {
            background-color: #0a0a0a !important;
            color: #ffffff !important;
            border: 1px solid #333 !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #00cc66 !important;
        }
        
        /* Botões */
        button[kind="primary"] {
            background-color: #00cc66 !important;
            border: none !important;
            color: #000000 !important;
            font-weight: bold !important;
            width: 100%;
            padding: 12px !important;
            border-radius: 8px !important;
            font-size: 16px !important;
        }
        button[kind="primary"]:hover {
            background-color: #00e673 !important;
            transform: scale(1.02);
        }
        button[kind="secondary"] {
            background-color: #2a2a2a !important;
            color: #ffffff !important;
            border: 1px solid #00cc66 !important;
        }

        /* Logout */
        .logout-container {
            text-align: right;
            margin-bottom: 20px;
        }

        /* Ocultar elementos do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
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
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None

# --------------------------------------------------------------------------
# 4. COMPONENTES VISUAIS
# --------------------------------------------------------------------------
def renderizar_header_centralizado():
    """Header centralizado com logo e texto"""
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    
    # Tenta carregar a logo
    try:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("logo.png", use_container_width=True)
    except:
        st.markdown("💚", unsafe_allow_html=True)
    
    st.markdown("<div class='subtitulo'>Portal de Parceiras Green Express</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def renderizar_podio(df_vendas):
    """Renderiza o pódio com top 3 parceiras - APENAS TEXTO"""
    coluna_codigo = 'código' if 'código' in df_vendas.columns else 'codigo'
    
    # Pega top 3
    top3 = df_vendas.nlargest(3, 'valor_de_vendas_no_mes').head(3)
    
    if len(top3) == 0:
        st.info("Ainda não há dados de vendas para exibir o ranking.")
        return
    
    st.markdown("<div class='podium-container'>", unsafe_allow_html=True)
    st.markdown("<div class='podium-title'>🏆 RANKING DO MÊS</div>", unsafe_allow_html=True)
    st.markdown("<div class='podium-grid'>", unsafe_allow_html=True)
    
    # Ordem: 2º (esquerda), 1º (centro), 3º (direita)
    positions = [1, 0, 2]  # Índices: 2º lugar, 1º lugar, 3º lugar
    medal_colors = {0: '#FFD700', 1: '#C0C0C0', 2: '#CD7F32'}
    medal_numbers = {0: '1', 1: '2', 2: '3'}
    
    for idx in positions:
        if idx < len(top3):
            row = top3.iloc[idx]
            cupom = row[coluna_codigo]
            valor = row['valor_de_vendas_no_mes']
            
            card_class = f"podium-card-{medal_numbers[idx]}"
            
            st.markdown(f"""
            <div class='podium-card {card_class}'>
                <div class='podium-position' style='color: {medal_colors[idx]};'>{medal_numbers[idx]}</div>
                <div class='podium-cupom'>{cupom}</div>
                <div class='podium-value'>R$ {valor:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Card vazio se não houver 3 participantes
            st.markdown("<div class='podium-card' style='opacity: 0.3;'><div class='podium-position'>-</div></div>", unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def renderizar_resultados(vendas_mes, qtd, comissao, vendas_totais):
    """Renderiza os cards de resultados"""
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown("<div class='result-title'>Acesso aos Resultados</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Vendas Totais no mês</div>
            <div class='metric-value'>R$ {vendas_mes:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Quantidade de vendas</div>
            <div class='metric-value'>{qtd}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-label'>Sua Comissão (20%)</div>
        <div class='metric-value-green'>R$ {comissao:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-box' style='border-color: #666;'>
        <div class='metric-label'>Vendas período total</div>
        <div class='metric-value'>R$ {vendas_totais:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def renderizar_dados_pessoais(cupom, link_afiliacao=""):
    """Renderiza a seção de dados pessoais"""
    st.markdown("<div class='personal-data'>", unsafe_allow_html=True)
    st.markdown("<div class='data-title'>📋 Seus Dados</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='data-item'>
        <div class='data-label'>Cupom</div>
        <div class='data-value'>{cupom}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if link_afiliacao:
        st.markdown(f"""
        <div class='data-item'>
            <div class='data-label'>Link de afiliação</div>
            <div class='data-value'>{link_afiliacao}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 5. PROGRAMA PRINCIPAL
# --------------------------------------------------------------------------
def main():
    local_css()
    
    df_vendas, df_usuarios = carregar_dados()

    if df_vendas is None or df_usuarios is None:
        st.error("⚠️ Erro: Arquivos 'vendas.csv' ou 'usuario.csv' não encontrados.")
        st.stop()

    # --- LÓGICA DE ESTADO ---
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
        st.session_state['usuario_atual'] = ''

    # --- TELA DE LOGIN ---
    if not st.session_state['logado']:
        # Header centralizado
        renderizar_header_centralizado()
        
        # Pódio visível antes do login
        renderizar_podio(df_vendas)
        
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<div class='result-title'>Acesso aos Resultados</div>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            cupom_input = st.text_input("Digite seu Cupom", key="cupom").strip().upper()
            senha_input = st.text_input("Digite sua Senha", type="password", key="senha").strip()
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
                st.error("❌ Cupom ou senha inválidos.")
        
        st.markdown("</div>", unsafe_allow_html=True)

    # --- PAINEL LOGADO ---
    else:
        cupom_ativo = st.session_state['usuario_atual']
        
        # Header centralizado (logado)
        renderizar_header_centralizado()
        
        # Botão de logout
        st.markdown("<div class='logout-container'>", unsafe_allow_html=True)
        if st.button("🚪 Sair", type="secondary"):
            st.session_state['logado'] = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Pódio
        renderizar_podio(df_vendas)

        # Processamento de dados - CORRIGIDO
        coluna_codigo = 'código' if 'código' in df_vendas.columns else 'codigo'
        dados_vendas = df_vendas[df_vendas[coluna_codigo] == cupom_ativo]

        if not dados_vendas.empty:
            # Vendas no mês (coluna C)
            vendas_mes = dados_vendas['valor_de_vendas_no_mes'].values[0]
            
            # Quantidade de vendas (coluna B)
            qtd = dados_vendas['quantidade_de_vendas'].values[0]
            
            # Comissão calculada sobre vendas no mês
            comissao = vendas_mes * (PORCENTAGEM_COMISSAO_PADRAO / 100)
            
            # Vendas período total (coluna D) - INDIVIDUAL da influencer
            vendas_totais = dados_vendas['valor_total_de_vendas'].values[0]
        else:
            vendas_mes = 0
            qtd = 0
            comissao = 0
            vendas_totais = 0

        # Renderizar resultados
        renderizar_resultados(vendas_mes, qtd, comissao, vendas_totais)

        # Link de afiliação (buscar do CSV se existir)
        link_afiliacao = ""
        usuario_info = df_usuarios[df_usuarios['cupom'] == cupom_ativo]
        if not usuario_info.empty and 'link' in df_usuarios.columns:
            link_afiliacao = usuario_info['link'].values[0]
        
        renderizar_dados_pessoais(cupom_ativo, link_afiliacao)

        # Admin expandido
        with st.expander("🔧 Admin"):
            senha_admin = st.text_input("Senha Admin", type="password", key="admin_pass")
            if senha_admin == "admin123":
                st.success("✅ Acesso admin concedido")
                st.dataframe(df_vendas)
                st.dataframe(df_usuarios)

if __name__ == "__main__":
    main()

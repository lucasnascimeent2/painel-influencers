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
            padding: 20px 0 15px 0;
        }
        .logo-img {
            max-width: 150px;
            margin: 0 auto;
            display: block;
        }
        .subtitulo {
            color: #00cc66;
            font-size: 14px;
            font-weight: 400;
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-align: center;
        }

        /* Pódio de Ranking - VERTICAL */
        .podium-container {
            background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
            border-radius: 15px;
            padding: 25px 20px;
            margin: 15px 0;
            border: 1px solid #00cc66;
        }
        .podium-title {
            color: #ffffff;
            font-size: 18px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 20px;
        }
        .podium-grid {
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-width: 500px;
            margin: 0 auto;
        }
        .podium-card {
            background: #2a2a2a;
            border-radius: 10px;
            padding: 15px 20px;
            text-align: center;
            border: 2px solid;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .podium-card-1 { border-color: #FFD700; }
        .podium-card-2 { border-color: #C0C0C0; }
        .podium-card-3 { border-color: #CD7F32; }
        
        .podium-position {
            font-size: 36px;
            font-weight: 700;
            margin: 0;
            min-width: 50px;
        }
        .podium-cupom {
            color: #00cc66;
            font-weight: 600;
            font-size: 16px;
            flex: 1;
            text-align: center;
        }
        .podium-value {
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
            min-width: 120px;
            text-align: right;
        }

        /* Card de Resultados */
        .result-card {
            background: linear-gradient(135deg, #1f1f1f 0%, #151515 100%);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid #333;
        }
        .result-title {
            color: #ffffff;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            text-align: center;
        }
        .metric-box {
            background: #0a0a0a;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            margin: 8px 0;
            border: 1px solid #00cc66;
        }
        .metric-label {
            color: #888;
            font-size: 13px;
            margin-bottom: 6px;
        }
        .metric-value {
            color: #ffffff;
            font-size: 24px;
            font-weight: 700;
        }
        .metric-value-green {
            color: #00cc66;
            font-size: 28px;
            font-weight: 700;
        }

        /* Seção de Dados Pessoais */
        .personal-data {
            background: #1a1a1a;
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid #333;
        }
        .data-title {
            color: #00cc66;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 12px;
            text-align: center;
        }
        .data-item {
            background: #0a0a0a;
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid #333;
        }
        .data-label {
            color: #888;
            font-size: 11px;
            margin-bottom: 4px;
        }
        .data-value {
            color: #ffffff;
            font-size: 15px;
            font-weight: 600;
            word-break: break-all;
        }

        /* Formulário de Login */
        .login-container {
            max-width: 500px;
            margin: 30px auto;
            padding: 25px;
            background: transparent;
            border-radius: 15px;
            border: none;
        }
        
        /* Seletor de Mês */
        .month-selector {
            background: #1a1a1a;
            border-radius: 12px;
            padding: 15px;
            margin: 15px 0;
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
        
        /* Selectbox */
        div[data-testid="stSelectbox"] > div > div {
            background-color: #0a0a0a !important;
            color: #ffffff !important;
            border: 1px solid #00cc66 !important;
            border-radius: 8px !important;
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

# Mapeamento dos meses
MESES_PT = {
    'janeiro': 'Janeiro',
    'fevereiro': 'Fevereiro',
    'março': 'Março',
    'abril': 'Abril',
    'maio': 'Maio',
    'junho': 'Junho',
    'julho': 'Julho',
    'agosto': 'Agosto',
    'setembro': 'Setembro',
    'outubro': 'Outubro',
    'novembro': 'Novembro',
    'dezembro': 'Dezembro'
}

@st.cache_data(ttl=60)
def carregar_dados():
    try:
        # Tenta diferentes encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        df_vendas = None
        df_usuarios = None
        
        # Tenta carregar vendas.csv
        for encoding in encodings:
            try:
                df_vendas = pd.read_csv(ARQUIVO_VENDAS, encoding=encoding)
                break
            except:
                continue
        
        if df_vendas is None:
            st.error("Não foi possível carregar vendas.csv com nenhuma codificação")
            return None, None
        
        # Tenta carregar usuario.csv
        for encoding in encodings:
            try:
                df_usuarios = pd.read_csv(ARQUIVO_USUARIOS, encoding=encoding)
                break
            except:
                continue
        
        if df_usuarios is None:
            st.error("Não foi possível carregar usuario.csv com nenhuma codificação")
            return None, None
        
        df_usuarios['cupom'] = df_usuarios['cupom'].astype(str).str.upper().str.strip()
        df_usuarios['senha'] = df_usuarios['senha'].astype(str).str.strip()
        return df_vendas, df_usuarios
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None

def obter_colunas_meses(df):
    """Identifica as colunas de meses na planilha"""
    colunas = df.columns.tolist()
    # Pega todas as colunas entre 'quantidade' e 'valor_total_de_vendas'
    meses_colunas = []
    for col in colunas:
        col_lower = col.lower()
        if col_lower in MESES_PT.keys():
            meses_colunas.append(col)
    return meses_colunas

def calcular_vendas_totais(row, colunas_meses):
    """Calcula o total de vendas somando todos os meses"""
    total = 0
    for mes in colunas_meses:
        valor = row[mes]
        if pd.notna(valor) and valor != '':
            try:
                total += float(valor)
            except:
                pass
    return total

# --------------------------------------------------------------------------
# 4. COMPONENTES VISUAIS
# --------------------------------------------------------------------------
def renderizar_header_centralizado():
    """Header centralizado com logo e texto"""
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    
    try:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("logo.svg", use_container_width=True)
    except:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.markdown("💚", unsafe_allow_html=True)
    
    st.markdown("<div class='subtitulo'>Portal de Parceiras Green Express</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def renderizar_podio(df_vendas, mes_selecionado=None):
    """Renderiza o pódio com top 3 parceiras"""
    colunas = df_vendas.columns.tolist()
    coluna_codigo = colunas[0]
    
    # Se um mês foi selecionado, usa ele, senão calcula o total
    if mes_selecionado and mes_selecionado != "Total (Todos os meses)":
        coluna_ranking = mes_selecionado.lower()
        titulo_podio = f"🏆 RANKING - {mes_selecionado.upper()}"
    else:
        # Calcula total para ranking
        colunas_meses = obter_colunas_meses(df_vendas)
        df_vendas_copy = df_vendas.copy()
        df_vendas_copy['total_calculado'] = df_vendas_copy.apply(
            lambda row: calcular_vendas_totais(row, colunas_meses), axis=1
        )
        coluna_ranking = 'total_calculado'
        titulo_podio = "🏆 RANKING - TOTAL GERAL"
    
    # Pega top 3
    if coluna_ranking == 'total_calculado':
        top3 = df_vendas_copy.nlargest(3, coluna_ranking).head(3)
    else:
        top3 = df_vendas.nlargest(3, coluna_ranking).head(3)
    
    if len(top3) == 0:
        st.info("Ainda não há dados de vendas para exibir o ranking.")
        return
    
    st.markdown("<div class='podium-container'>", unsafe_allow_html=True)
    st.markdown(f"<div class='podium-title'>{titulo_podio}</div>", unsafe_allow_html=True)
    st.markdown("<div class='podium-grid'>", unsafe_allow_html=True)
    
    medal_colors = {0: '#FFD700', 1: '#C0C0C0', 2: '#CD7F32'}
    medal_numbers = {0: '1', 1: '2', 2: '3'}
    
    for idx in range(min(3, len(top3))):
        row = top3.iloc[idx]
        cupom = row[coluna_codigo]
        valor = row[coluna_ranking]
        
        if pd.isna(valor) or valor == '':
            valor = 0
        else:
            valor = float(valor)
        
        card_class = f"podium-card-{medal_numbers[idx]}"
        
        st.markdown(f"""
        <div class='podium-card {card_class}'>
            <div class='podium-position' style='color: {medal_colors[idx]};'>{medal_numbers[idx]}</div>
            <div class='podium-cupom'>{cupom}</div>
            <div class='podium-value'>R$ {valor:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def renderizar_seletor_mes(colunas_meses):
    """Renderiza o seletor de mês"""
    st.markdown("<div class='month-selector'>", unsafe_allow_html=True)
    
    # Adiciona opção de ver todos os meses
    opcoes_meses = ["Total (Todos os meses)"] + [MESES_PT[m.lower()] for m in colunas_meses if m.lower() in MESES_PT]
    
    mes_selecionado = st.selectbox(
        "📅 Selecione o mês para visualizar:",
        opcoes_meses,
        key="seletor_mes"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    return mes_selecionado

def renderizar_resultados(vendas_mes, qtd, comissao, vendas_totais, mes_selecionado):
    """Renderiza os cards de resultados"""
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    
    # Label do mês
    if mes_selecionado == "Total (Todos os meses)":
        label_mes = "Vendas Totais (Todos os meses)"
    else:
        label_mes = f"Vendas em {mes_selecionado}"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>{label_mes}</div>
            <div class='metric-value'>R$ {float(vendas_mes):,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>Quantidade de vendas</div>
            <div class='metric-value'>{int(qtd)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='metric-box'>
        <div class='metric-label'>Sua Comissão (20%)</div>
        <div class='metric-value-green'>R$ {float(comissao):,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Só mostra vendas totais se não estiver no modo "Total"
    if mes_selecionado != "Total (Todos os meses)":
        st.markdown(f"""
        <div class='metric-box' style='border-color: #666;'>
            <div class='metric-label'>Vendas Totais (Todos os períodos)</div>
            <div class='metric-value'>R$ {float(vendas_totais):,.2f}</div>
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

    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
        st.session_state['usuario_atual'] = ''

    # --- TELA DE LOGIN ---
    if not st.session_state['logado']:
        renderizar_header_centralizado()
        renderizar_podio(df_vendas)
        
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
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
        
        renderizar_header_centralizado()
        
        col_space, col_btn = st.columns([4, 1])
        with col_btn:
            if st.button("🚪 Sair", type="secondary"):
                st.session_state['logado'] = False
                st.rerun()

        # Identifica colunas de meses
        colunas = df_vendas.columns.tolist()
        coluna_codigo = colunas[0]
        coluna_qtd = colunas[1]
        colunas_meses = obter_colunas_meses(df_vendas)
        
        # Seletor de mês
        mes_selecionado = renderizar_seletor_mes(colunas_meses)
        
        # Pódio com mês selecionado
        renderizar_podio(df_vendas, mes_selecionado)

        # Busca dados do usuário
        dados_vendas = df_vendas[df_vendas[coluna_codigo] == cupom_ativo]

        if not dados_vendas.empty:
            qtd = dados_vendas[coluna_qtd].values[0]
            
            # Calcula vendas totais (soma de todos os meses)
            vendas_totais = calcular_vendas_totais(dados_vendas.iloc[0], colunas_meses)
            
            # Se selecionou um mês específico
            if mes_selecionado == "Total (Todos os meses)":
                vendas_mes = vendas_totais
            else:
                # Busca valor do mês selecionado
                mes_coluna = mes_selecionado.lower()
                if mes_coluna in dados_vendas.columns:
                    vendas_mes = dados_vendas[mes_coluna].values[0]
                    if pd.isna(vendas_mes) or vendas_mes == '':
                        vendas_mes = 0
                    else:
                        vendas_mes = float(vendas_mes)
                else:
                    vendas_mes = 0
            
            comissao = vendas_mes * (PORCENTAGEM_COMISSAO_PADRAO / 100)
        else:
            vendas_mes = 0
            qtd = 0
            comissao = 0
            vendas_totais = 0

        renderizar_resultados(vendas_mes, qtd, comissao, vendas_totais, mes_selecionado)

        link_afiliacao = ""
        usuario_info = df_usuarios[df_usuarios['cupom'] == cupom_ativo]
        if not usuario_info.empty and 'link' in df_usuarios.columns:
            link_afiliacao = usuario_info['link'].values[0]
        
        renderizar_dados_pessoais(cupom_ativo, link_afiliacao)

        with st.expander("🔧 Admin"):
            senha_admin = st.text_input("Senha Admin", type="password", key="admin_pass")
            if senha_admin == "admin123":
                st.success("✅ Acesso admin concedido")
                st.dataframe(df_vendas)
                st.dataframe(df_usuarios)

if __name__ == "__main__":
    main()

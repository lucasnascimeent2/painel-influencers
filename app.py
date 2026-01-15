import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------
# 1. CONFIGURAÇÃO INICIAL (Obrigatório ser a primeira linha)
# --------------------------------------------------------------------------
st.set_page_config(page_title="Portal do Parceiro Green Express", layout="centered")

# --------------------------------------------------------------------------
# 2. DESIGN E PERSONALIZAÇÃO (CSS REFORÇADO)
# --------------------------------------------------------------------------
def local_css():
    st.markdown("""
        <style>
        /* Fundo geral escuro */
        .stApp {
            background-color: #0e1117 !important;
            color: #ffffff !important;
        }
        
        /* Título principal */
        h1 {
            color: #00cc66 !important;
            text-align: center;
            font-family: 'Helvetica', sans-serif;
            font-weight: 700;
            padding-bottom: 20px;
        }
        
        /* Campos de Entrada de Texto (Login/Senha) */
        div[data-testid="stTextInput"] input {
            background-color: #262730 !important;
            color: #ffffff !important;
            border: 1px solid #4b5563 !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #00cc66 !important;
            box-shadow: 0 0 0 1px #00cc66 !important;
        }
        div[data-testid="stTextInput"] label {
            color: #e5e7eb !important;
        }

        /* Botões (Primary) */
        button[kind="primary"] {
            background-color: #00cc66 !important;
            border: none !important;
            color: #000000 !important;
            font-weight: bold !important;
            transition: all 0.3s ease;
        }
        button[kind="primary"]:hover {
            background-color: #00e673 !important;
            transform: scale(1.02);
        }

        /* Cartões de Métricas (Design "Card") */
        div[data-testid="stMetric"] {
            background-color: #1f2937 !important;
            border: 1px solid #00cc66 !important;
            border-radius: 10px !important;
            padding: 15px !important;
            text-align: center !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Texto dos Labels (ex: "Vendas Totais") */
        div[data-testid="stMetricLabel"] {
            color: #9ca3af !important;
            font-size: 14px !important;
        }
        
        /* Texto dos Valores (ex: "R$ 1.000,00") */
        div[data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-size: 26px !important;
            font-weight: bold !important;
        }
        
        /* Mensagens de Sucesso/Info */
        div[data-testid="stAlert"] {
            background-color: #1f2937 !important;
            color: #ffffff !important;
            border: 1px solid #4b5563 !important;
        }
        </style>
        """, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 3. CONFIGURAÇÕES DO SISTEMA
# --------------------------------------------------------------------------
ARQUIVO_VENDAS = 'vendas.csv'
ARQUIVO_USUARIOS = 'usuario.csv'  # <--- ALTERADO PARA SINGULAR
PORCENTAGEM_COMISSAO_PADRAO = 20.0 

# --------------------------------------------------------------------------
# 4. FUNÇÃO DE CARREGAMENTO DE DADOS
# --------------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    try:
        # Carrega as Vendas
        df_vendas = pd.read_csv(ARQUIVO_VENDAS)
        
        # Carrega os Usuários
        df_usuarios = pd.read_csv(ARQUIVO_USUARIOS)
        
        # Tratamento de dados (segurança contra erros de digitação)
        df_usuarios['cupom'] = df_usuarios['cupom'].astype(str).str.upper().str.strip()
        df_usuarios['senha'] = df_usuarios['senha'].astype(str).str.strip()
        
        return df_vendas, df_usuarios
        
    except FileNotFoundError as e:
        # Mensagem de erro amigável se o arquivo não existir
        st.error(f"⚠️ Erro de Arquivo: {e}")
        st.info(f"Verifique se o arquivo '{ARQUIVO_USUARIOS}' foi criado no GitHub/Pasta.")
        return None, None
    except Exception as e:
        st.error(f"Erro desconhecido: {e}")
        return None, None

# --------------------------------------------------------------------------
# 5. PROGRAMA PRINCIPAL
# --------------------------------------------------------------------------
def main():
    # Aplica o CSS imediatamente ao iniciar
    local_css()
    
    st.title("💚 Portal Green Express")
    st.markdown("---")

    df_vendas, df_usuarios = carregar_dados()

    if df_vendas is not None and df_usuarios is not None:
        
        # Inicializa estado da sessão (para manter o login ativo)
        if 'logado' not in st.session_state:
            st.session_state['logado'] = False
            st.session_state['usuario_atual'] = ''

        # --- TELA DE LOGIN ---
        if not st.session_state['logado']:
            st.subheader("Acesso do Parceiro")
            
            with st.form("login_form"):
                col1, col2 = st.columns(2)
                with col1:
                    cupom_input = st.text_input("Seu Cupom:").strip().upper()
                with col2:
                    senha_input = st.text_input("Sua Senha:", type="password").strip()
                
                # Botão centralizado
                st.markdown("<br>", unsafe_allow_html=True)
                botao_entrar = st.form_submit_button("Acessar Painel", type="primary")

            if botao_entrar:
                # Validação
                usuario_valido = df_usuarios[
                    (df_usuarios['cupom'] == cupom_input) & 
                    (df_usuarios['senha'] == senha_input)
                ]

                if not usuario_valido.empty:
                    st.session_state['logado'] = True
                    st.session_state['usuario_atual'] = cupom_input
                    st.rerun()
                else:
                    st.error("❌ Acesso Negado. Cupom ou Senha incorretos.")
        
        # --- PAINEL DE RESULTADOS (LOGADO) ---
        else:
            cupom_ativo = st.session_state['usuario_atual']
            
            # Cabeçalho com botão de sair
            col_topo1, col_topo2 = st.columns([3, 1])
            with col_topo1:
                st.success(f"Olá, **{cupom_ativo}**!")
            with col_topo2:
                if st.button("Sair / Logout"):
                    st.session_state['logado'] = False
                    st.rerun()

            st.markdown("---")

            # Busca dados nas Vendas
            coluna_codigo = 'código' 
            if 'código' not in df_vendas.columns and 'Codigo' in df_vendas.columns:
                    coluna_codigo = 'Codigo'

            dados_vendas = df_vendas[df_vendas[coluna_codigo] == cupom_ativo]

            if not dados_vendas.empty:
                vendas_totais = dados_vendas['valor_total_das_vendas'].values[0]
                quantidade = dados_vendas['quantidade'].values[0]
                comissao = vendas_totais * (PORCENTAGEM_COMISSAO_PADRAO / 100)

                # Exibe Métricas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Vendas Totais", f"R$ {vendas_totais:,.2f}")
                with col2:
                    st.metric("Quantidade", f"{quantidade}")
                with col3:
                    st.metric(f"Comissão ({int(PORCENTAGEM_COMISSAO_PADRAO)}%)", f"R$ {comissao:,.2f}")
                
            else:
                st.info("Nenhuma venda registrada para este cupom no período atual.")
                col1, col2, col3 = st.columns(3)
                with col1: st.metric("Vendas", "R$ 0,00")
                with col2: st.metric("Qtd", "0")
                with col3: st.metric("Comissão", "R$ 0,00")

    # --- ADMIN (Rodapé Oculto) ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("🔐 Área Administrativa"):
        senha_admin = st.text_input("Senha Admin", type="password")
        if senha_admin == "admin123":
            if df_vendas is not None:
                st.write("### Base de Vendas Completa")
                st.dataframe(df_vendas)
                st.write(f"Total Loja: R$ {df_vendas['valor_total_das_vendas'].sum():,.2f}")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------
# 1. CONFIGURAÇÃO INICIAL DA PÁGINA
# --------------------------------------------------------------------------
st.set_page_config(page_title="Portal do Parceiro Green Express", layout="centered")

# --------------------------------------------------------------------------
# 2. DESIGN E PERSONALIZAÇÃO (CSS)
# --------------------------------------------------------------------------
def local_css():
    st.markdown("""
        <style>
        /* Fundo geral escuro */
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        
        /* Título principal em Verde Neon */
        h1 {
            color: #00cc66 !important;
            text-align: center;
            font-family: 'Helvetica', sans-serif;
            font-weight: 700;
        }
        
        /* Subtítulos */
        h3 {
            color: #e5e7eb;
            font-weight: 400;
        }

        /* Cartões de Métricas (Quadrados com borda verde) */
        div[data-testid="stMetric"] {
            background-color: #1f2937;
            border: 2px solid #00cc66;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        /* Texto dos Labels (ex: "Vendas Totais") */
        div[data-testid="stMetricLabel"] {
            color: #9ca3af;
            font-size: 14px;
        }
        
        /* Texto dos Valores (ex: "R$ 1.000,00") */
        div[data-testid="stMetricValue"] {
            color: #ffffff;
            font-size: 26px;
            font-weight: bold;
        }

        /* Botão de Login */
        button[kind="primary"] {
            background-color: #00cc66;
            border: none;
            color: #000;
            font-weight: bold;
        }
        button[kind="primary"]:hover {
            background-color: #00e673;
            color: #000;
        }
        </style>
        """, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 3. CONFIGURAÇÕES DO SISTEMA
# --------------------------------------------------------------------------
ARQUIVO_VENDAS = 'vendas.csv'
ARQUIVO_USUARIOS = 'usuario.csv'
PORCENTAGEM_COMISSAO_PADRAO = 20.0 

# --------------------------------------------------------------------------
# 4. FUNÇÃO DE CARREGAMENTO DE DADOS
# --------------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    try:
        # Carrega as Vendas
        df_vendas = pd.read_csv(ARQUIVO_VENDAS)
        
        # Carrega os Usuários (Logins)
        df_usuarios = pd.read_csv(ARQUIVO_USUARIOS)
        
        # Tratamento de dados para evitar erros de digitação (espaços extras, maiúsculas)
        # Converte para texto (string), remove espaços e joga para maiúsculo
        df_usuarios['cupom'] = df_usuarios['cupom'].astype(str).str.upper().str.strip()
        df_usuarios['senha'] = df_usuarios['senha'].astype(str).str.strip()
        
        return df_vendas, df_usuarios
        
    except FileNotFoundError as e:
        st.error(f"ERRO CRÍTICO: Arquivo não encontrado. Detalhes: {e}")
        st.warning("Certifique-se de que 'vendas.csv' e 'usuarios.csv' estão na mesma pasta.")
        return None, None
    except Exception as e:
        st.error(f"Erro desconhecido ao ler arquivos: {e}")
        return None, None

# --------------------------------------------------------------------------
# 5. PROGRAMA PRINCIPAL
# --------------------------------------------------------------------------
def main():
    local_css() # Aplica o design
    
    st.title("💚 Portal Green Express")
    st.markdown("---")

    df_vendas, df_usuarios = carregar_dados()

    # Só continua se os arquivos carregaram corretamente
    if df_vendas is not None and df_usuarios is not None:
        
        # --- TELA DE LOGIN ---
        if 'logado' not in st.session_state:
            st.session_state['logado'] = False
            st.session_state['usuario_atual'] = ''

        if not st.session_state['logado']:
            st.subheader("Acesso do Parceiro")
            
            with st.form("login_form"):
                col1, col2 = st.columns(2)
                with col1:
                    cupom_input = st.text_input("Seu Cupom:").strip().upper()
                with col2:
                    senha_input = st.text_input("Sua Senha:", type="password").strip()
                
                botao_entrar = st.form_submit_button("Acessar Painel", type="primary")

            if botao_entrar:
                # Verifica credenciais no arquivo usuarios.csv
                usuario_valido = df_usuarios[
                    (df_usuarios['cupom'] == cupom_input) & 
                    (df_usuarios['senha'] == senha_input)
                ]

                if not usuario_valido.empty:
                    st.session_state['logado'] = True
                    st.session_state['usuario_atual'] = cupom_input
                    st.rerun() # Recarrega a página para mostrar o painel
                else:
                    st.error("Acesso Negado. Verifique Cupom e Senha.")
        
        # --- PAINEL DE RESULTADOS (Só aparece se estiver logado) ---
        else:
            cupom_ativo = st.session_state['usuario_atual']
            st.success(f"Bem-vindo(a), **{cupom_ativo}**!")
            
            # Botão de Sair
            if st.button("Sair / Logout"):
                st.session_state['logado'] = False
                st.rerun()

            st.markdown("---")

            # Busca dados nas Vendas
            # Verifica colunas possíveis para evitar erro (código ou Codigo)
            coluna_codigo = 'código' 
            if 'código' not in df_vendas.columns and 'Codigo' in df_vendas.columns:
                    coluna_codigo = 'Codigo'

            dados_vendas = df_vendas[df_vendas[coluna_codigo] == cupom_ativo]

            if not dados_vendas.empty:
                # Extrai números
                vendas_totais = dados_vendas['valor_total_das_vendas'].values[0]
                quantidade = dados_vendas['quantidade'].values[0]
                comissao = vendas_totais * (PORCENTAGEM_COMISSAO_PADRAO / 100)

                # Mostra Cartões
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Vendas Totais", f"R$ {vendas_totais:,.2f}")
                with col2:
                    st.metric("Quantidade", f"{quantidade}")
                with col3:
                    st.metric(f"Sua Comissão ({int(PORCENTAGEM_COMISSAO_PADRAO)}%)", f"R$ {comissao:,.2f}")
                
            else:
                st.info("Nenhuma venda registrada para este cupom no período atual.")
                col1, col2, col3 = st.columns(3)
                with col1: st.metric("Vendas", "R$ 0,00")
                with col2: st.metric("Qtd", "0")
                with col3: st.metric("Comissão", "R$ 0,00")

    # --- ÁREA ADMIN (Escondida no rodapé) ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.expander("🔐 Área Administrativa"):
        senha_admin = st.text_input("Senha Admin", type="password")
        if senha_admin == "admin123":
            st.write("### Base de Vendas Completa")
            if df_vendas is not None:
                st.dataframe(df_vendas)
                st.write(f"Faturamento Total da Loja: R$ {df_vendas['valor_total_das_vendas'].sum():,.2f}")

if __name__ == "__main__":
    main()


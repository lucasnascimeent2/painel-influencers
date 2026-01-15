import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------
# 1. CONFIGURAÇÃO INICIAL
# --------------------------------------------------------------------------
st.set_page_config(page_title="Portal Green Express", page_icon="💚", layout="centered")

# --------------------------------------------------------------------------
# 2. CARREGAR DADOS
# --------------------------------------------------------------------------
ARQUIVO_VENDAS = 'vendas.csv'
ARQUIVO_USUARIOS = 'usuario.csv'
PORCENTAGEM_COMISSAO_PADRAO = 20.0 

@st.cache_data
def carregar_dados():
    try:
        df_vendas = pd.read_csv(ARQUIVO_VENDAS)
        df_usuarios = pd.read_csv(ARQUIVO_USUARIOS)
        
        # Tratamento de dados
        df_usuarios['cupom'] = df_usuarios['cupom'].astype(str).str.upper().str.strip()
        df_usuarios['senha'] = df_usuarios['senha'].astype(str).str.strip()
        
        return df_vendas, df_usuarios
    except Exception as e:
        return None, None

# --------------------------------------------------------------------------
# 3. PROGRAMA PRINCIPAL
# --------------------------------------------------------------------------
def main():
    
    # --- EXIBIÇÃO DA LOGO (NOVA PARTE) ---
    # Usamos colunas para centralizar a imagem
    col_esq, col_meio, col_dir = st.columns([1, 2, 1])
    with col_meio:
        try:
            # Tenta carregar a logo.png se ela estiver no GitHub
            st.image("logo.png", use_container_width=True)
        except:
            # Se não tiver logo, mostra apenas o título escrito
            st.title("💚 Green Express")

    st.markdown("---")

    df_vendas, df_usuarios = carregar_dados()

    # Verifica se os arquivos carregaram (se não, mostra erro amigável)
    if df_vendas is None or df_usuarios is None:
        st.error("⚠️ Erro de Sistema")
        st.warning("Verifique se os arquivos 'vendas.csv' e 'usuario.csv' estão no GitHub.")
        st.stop() # Para a execução aqui

    # --- LÓGICA DE LOGIN ---
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
        st.session_state['usuario_atual'] = ''

    if not st.session_state['logado']:
        st.subheader("Acesso Restrito")
        
        with st.form("login_form"):
            st.write("Entre com suas credenciais de parceiro:")
            cupom_input = st.text_input("Seu Cupom").strip().upper()
            senha_input = st.text_input("Sua Senha", type="password").strip()
            
            botao_entrar = st.form_submit_button("Entrar no Painel", type="primary")

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
                st.error("❌ Dados incorretos. Tente novamente.")
    
    # --- PAINEL (LOGADO) ---
    else:
        cupom_ativo = st.session_state['usuario_atual']
        
        # Barra de boas-vindas
        col1, col2 = st.columns([3, 1])
        col1.success(f"Logado como: **{cupom_ativo}**")
        if col2.button("Sair"):
            st.session_state['logado'] = False
            st.rerun()

        # Busca vendas
        coluna_codigo = 'código' 
        if 'código' not in df_vendas.columns and 'Codigo' in df_vendas.columns:
            coluna_codigo = 'Codigo'

        dados_vendas = df_vendas[df_vendas[coluna_codigo] == cupom_ativo]

        st.markdown("### Seus Resultados")
        
        if not dados_vendas.empty:
            vendas = dados_vendas['valor_total_das_vendas'].values[0]
            qtd = dados_vendas['quantidade'].values[0]
            comissao = vendas * (PORCENTAGEM_COMISSAO_PADRAO / 100)

            # Cartões de Métricas (Simples e Eficiente)
            c1, c2, c3 = st.columns(3)
            c1.metric("Vendas Totais", f"R$ {vendas:,.2f}")
            c2.metric("Quantidade", f"{qtd}")
            c3.metric("Comissão (20%)", f"R$ {comissao:,.2f}")
        else:
            st.info("Ainda não há vendas registradas para este período.")
            c1, c2, c3 = st.columns(3)
            c1.metric("Vendas", "R$ 0,00")
            c2.metric("Qtd", "0")
            c3.metric("Comissão", "R$ 0,00")

    # Admin Oculto
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("Admin"):
        if st.text_input("Senha") == "admin123":
            st.dataframe(df_vendas)

if __name__ == "__main__":
    main()

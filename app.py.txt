import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Portal do Influencer", layout="centered")

# --- CONFIGURAÇÕES ---
ARQUIVO_DADOS = 'green-line-premium3-relatorio-de-vendas-por-cupom-15_01_2026_09_52_52-FkcQO.csv'
PORCENTAGEM_COMISSAO_PADRAO = 10.0  # Defina aqui a comissão padrão (ex: 10%)

# Função para carregar dados
@st.cache_data
def carregar_dados():
    try:
        # Carrega o CSV. O separador parece ser vírgula baseado na análise prévia.
        df = pd.read_csv(ARQUIVO_DADOS)
        return df
    except FileNotFoundError:
        st.error(f"Arquivo '{ARQUIVO_DADOS}' não encontrado. Verifique se ele está na mesma pasta do script.")
        return None

def main():
    st.title("💚 Portal do Parceiro Green Line")
    st.markdown("---")

    df = carregar_dados()

    if df is not None:
        # Área de Login (Simples)
        st.subheader("Acesso aos Resultados")
        cupom_input = st.text_input("Digite seu Cupom de Parceiro (ex: SEUNOME10):").strip().upper()

        if cupom_input:
            # Filtra os dados pelo cupom
            dados_influencer = df[df['código'] == cupom_input]

            if not dados_influencer.empty:
                # Extrai os valores
                vendas_totais = dados_influencer['valor_total_das_vendas'].values[0]
                quantidade = dados_influencer['quantidade'].values[0]
                
                # Cálculo da comissão
                comissao = vendas_totais * (PORCENTAGEM_COMISSAO_PADRAO / 100)

                st.success(f"Dados encontrados para: **{cupom_input}**")
                
                # Exibe métricas em cartões
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Vendas Totais", f"R$ {vendas_totais:,.2f}")
                with col2:
                    st.metric("Quantidade Vendida", f"{quantidade}")
                with col3:
                    st.metric("Sua Comissão (estimada)", f"R$ {comissao:,.2f}")
                
                st.info(f"Parabéns! Seu cupom representa {dados_influencer['porcentagem_das_vendas'].values[0]}% das vendas totais da loja.")

            else:
                st.warning("Cupom não encontrado ou sem vendas registradas neste período.")

    # Rodapé / Área Admin (Opcional)
    st.markdown("---")
    with st.expander("Área Administrativa (Apenas Interno)"):
        senha = st.text_input("Senha Admin", type="password")
        if senha == "admin123": # Você pode mudar essa senha
            st.write("Visão Geral de Todas as Vendas:")
            st.dataframe(df)
            st.write(f"Total Geral Vendido: R$ {df['valor_total_das_vendas'].sum():,.2f}")

if __name__ == "__main__":
    main()
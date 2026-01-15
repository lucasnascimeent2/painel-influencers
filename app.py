import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Portal do Influencer", layout="centered")

# --- CONFIGURAÇÕES ---
ARQUIVO_DADOS = 'vendas.csv'
PORCENTAGEM_COMISSAO_PADRAO = 20.0 

# Função para carregar dados
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv(ARQUIVO_DADOS)
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
        return None

def main():
    st.title("💚 Portal do Parceiro Green Express")
    st.markdown("---")

    df = carregar_dados()

    if df is None:
        st.error(f"O arquivo '{ARQUIVO_DADOS}' não foi encontrado.")
        st.warning("DICA: Verifique se o arquivo da planilha está na mesma pasta e se o nome é exatamente 'vendas.csv'.")
    else:
        # Área de Login
        st.subheader("Acesso aos Resultados")
        cupom_input = st.text_input("Digite seu Cupom de Parceiro:").strip().upper()

        if cupom_input:
            # Tenta encontrar a coluna correta
            coluna_codigo = 'código' 
            if 'código' not in df.columns and 'Codigo' in df.columns:
                 coluna_codigo = 'Codigo'

            if coluna_codigo in df.columns:
                dados_influencer = df[df[coluna_codigo] == cupom_input]

                if not dados_influencer.empty:
                    vendas_totais = dados_influencer['valor_total_das_vendas'].values[0]
                    quantidade = dados_influencer['quantidade'].values[0]
                    
                    # Cálculo da comissão
                    comissao = vendas_totais * (PORCENTAGEM_COMISSAO_PADRAO / 100)

                    st.success(f"Dados encontrados para: **{cupom_input}**")
                    
                    # Exibe apenas as métricas importantes
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Vendas Totais", f"R$ {vendas_totais:,.2f}")
                    with col2:
                        st.metric("Quantidade", f"{quantidade}")
                    with col3:
                        st.metric("Sua Comissão (20%)", f"R$ {comissao:,.2f}")
                    
                else:
                    st.warning("Cupom não encontrado nas vendas deste período.")
            else:
                st.error("Erro na Planilha: A coluna 'código' não foi encontrada.")

    # Área Admin (Mantive oculta, mas se quiser tirar também, me avise)
    st.markdown("---")
    with st.expander("Área Administrativa"):
        senha = st.text_input("Senha Admin", type="password")
        if senha == "admin123":
            if df is not None:
                st.write(df)
                st.write(f"Total Geral: R$ {df['valor_total_das_vendas'].sum():,.2f}")

if __name__ == "__main__":
    main()

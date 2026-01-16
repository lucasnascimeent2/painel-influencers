@st.cache_data(ttl=60)
def carregar_dados():
    try:
        # Tenta diferentes encodings comuns para arquivos brasileiros
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        df_vendas = None
        df_usuarios = None
        
        # Tenta carregar vendas.csv
        for encoding in encodings:
            try:
                df_vendas = pd.read_csv(ARQUIVO_VENDAS, encoding=encoding)
                print(f"✅ vendas.csv carregado com encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        # Tenta carregar usuario.csv
        for encoding in encodings:
            try:
                df_usuarios = pd.read_csv(ARQUIVO_USUARIOS, encoding=encoding)
                print(f"✅ usuario.csv carregado com encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if df_vendas is None or df_usuarios is None:
            raise Exception("Não foi possível carregar os arquivos com nenhum encoding testado")
        
        # DEBUG: Mostrar colunas encontradas
        st.info(f"🔍 Colunas em vendas.csv: {df_vendas.columns.tolist()}")
        st.info(f"🔍 Colunas em usuario.csv: {df_usuarios.columns.tolist()}")
        
        # Limpa nomes das colunas (remove espaços extras)
        df_vendas.columns = df_vendas.columns.str.strip()
        df_usuarios.columns = df_usuarios.columns.str.strip()
        
        # Verifica se a coluna 'cupom' existe
        if 'cupom' not in df_usuarios.columns:
            colunas_disponiveis = df_usuarios.columns.tolist()
            raise Exception(f"Coluna 'cupom' não encontrada. Colunas disponíveis: {colunas_disponiveis}")
        
        # Processamento dos dados
        df_usuarios['cupom'] = df_usuarios['cupom'].astype(str).str.upper().str.strip()
        df_usuarios['senha'] = df_usuarios['senha'].astype(str).str.strip()
        
        return df_vendas, df_usuarios
        
    except FileNotFoundError as e:
        st.error(f"❌ Arquivo não encontrado: {e}")
        return None, None
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None, None

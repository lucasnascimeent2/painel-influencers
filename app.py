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
        
        # Botão de logout - CORRIGIDO
        col_space, col_btn = st.columns([4, 1])
        with col_btn:
            if st.button("🚪 Sair", type="secondary"):
                st.session_state['logado'] = False
                st.rerun()

        # Pódio
        renderizar_podio(df_vendas)

        # Processamento de dados - CORREÇÃO AQUI
        colunas = df_vendas.columns.tolist()
        coluna_codigo = colunas[0]  # Coluna A - código
        coluna_qtd = colunas[1]     # Coluna B - quantidade
        coluna_vendas_mes = colunas[2]  # Coluna C - vendas_mes
        
        # IMPORTANTE: A coluna D (valor_total_de_vendas) parece não estar correta
        # Vamos calcular o total REAL somando todas as vendas do mês
        vendas_totais_reais = df_vendas[coluna_vendas_mes].sum()
        
        dados_vendas = df_vendas[df_vendas[coluna_codigo] == cupom_ativo]

        if not dados_vendas.empty:
            # Vendas Totais no mês = coluna C (vendas_mes do vendedor)
            vendas_mes = dados_vendas[coluna_vendas_mes].values[0]
            
            # Quantidade de vendas = coluna B
            qtd = dados_vendas[coluna_qtd].values[0]
            
            # Comissão calculada sobre vendas do mês
            comissao = vendas_mes * (PORCENTAGEM_COMISSAO_PADRAO / 100)
            
            # Vendas período total = SOMA de TODAS as vendas do mês (R$ 15.000,00)
            # Usamos o valor real calculado, não a coluna D
            vendas_totais = vendas_totais_reais
        else:
            vendas_mes = 0
            qtd = 0
            comissao = 0
            vendas_totais = 0

        # Renderizar resultados
        renderizar_resultados(vendas_mes, qtd, comissao, vendas_totais)

        # Link de afiliação
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
                
                # Mostrar estatísticas úteis para debug
                st.subheader("📊 Estatísticas do Sistema")
                st.write(f"Total de vendedores: {len(df_vendas)}")
                st.write(f"Vendas totais do mês (soma): R$ {vendas_totais_reais:,.2f}")
                st.write(f"Seu cupom: {cupom_ativo}")
                
                st.subheader("📁 Dados de Vendas")
                st.dataframe(df_vendas)
                
                st.subheader("👥 Dados de Usuários")
                st.dataframe(df_usuarios)

import streamlit as st

st.set_page_config(page_title="Calculadora de Custos", page_icon="🧮")
st.title("🧮 Calculadora de Custo Unitário com Conversão de Unidades")

st.markdown("""
Adicione os ingredientes e suas quantidades para calcular o custo por unidade do seu produto!
""")

# -----------------------
# Inicializar session_state
# -----------------------
if "ingredientes" not in st.session_state:
    st.session_state.ingredientes = []

# A lista de índices para remover é gerenciada de forma mais simples e sem st.session_state.indices_para_remover
# para evitar complicações com o rerun.

# -----------------------
# Função de conversão de unidades
# -----------------------
def converter_para_base(qtd, unidade):
    """Converte kg->g, l->ml, mantendo g, ml e unidade igual. Trata erros de unidade."""
    unidade = unidade.lower()
    if unidade == "kg":
        return qtd * 1000
    elif unidade == "g":
        return qtd
    elif unidade == "l":
        return qtd * 1000
    elif unidade == "ml":
        return qtd
    elif unidade == "unidade":
        return qtd
    else:
        st.warning(f"Unidade '{unidade}' não reconhecida para conversão. Usando o valor diretamente.")
        return qtd

# -----------------------
# Formulário para adicionar ingrediente
# -----------------------
with st.form("ingrediente_form", clear_on_submit=True):
    st.subheader("Adicionar Novo Ingrediente")
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    
    with col1:
        nome = st.text_input("Nome do Ingrediente", key="form_nome")
    with col2:
        quantidade_usada = st.number_input("Qtd usada na receita", min_value=0.0, value=0.0, format="%.2f", key="form_qtd_usada")
        unidade_usada = st.selectbox("Unidade usada", ["g","kg","ml","l","unidade"], key="form_u1")
    with col3:
        quantidade_total = st.number_input("Qtd total comprada", min_value=0.0, value=0.0, format="%.2f", key="form_qtd_total")
        unidade_total = st.selectbox("Unidade total", ["g","kg","ml","l","unidade"], key="form_u2")
    with col4:
        valor_total = st.number_input("Valor total (R$)", min_value=0.0, value=0.0, format="%.2f", key="form_valor")
    
    submitted = st.form_submit_button("➕ Adicionar Ingrediente")
    
    if submitted and nome and quantidade_usada > 0 and quantidade_total > 0 and valor_total >= 0:
        st.session_state.ingredientes.append({
            "nome": nome,
            "quantidade_usada": quantidade_usada,
            "unidade_usada": unidade_usada,
            "quantidade_total": quantidade_total,
            "unidade_total": unidade_total,
            "valor_total": valor_total
        })
        # REMOVEMOS O st.experimental_rerun() AQUI. 
        # A submissão do formulário já causa um rerun e evita o erro.
    elif submitted and not nome:
        st.warning("Por favor, preencha o nome do ingrediente.")
    elif submitted and (quantidade_usada <= 0 or quantidade_total <= 0):
        st.warning("As quantidades usada e total devem ser maiores que zero.")

# -----------------------
# Lista de ingredientes adicionados
# -----------------------
if st.session_state.ingredientes:
    st.subheader("Resumo dos Ingredientes e Custos")
    
    # Cabeçalho da tabela
    col_h1, col_h2, col_h3, col_h4, col_h5 = st.columns([3,2,2,2,1])
    col_h1.write("**Ingrediente**")
    col_h2.write("**Qtd Usada**")
    col_h3.write("**Custo Total (R$)**")
    col_h4.write("**Custo na Receita (R$)**")
    col_h5.write("")
    st.markdown("---")
    
    custo_total = 0
    indices_para_remover = []

    for i, ing in enumerate(st.session_state.ingredientes):
        
        # Lógica de Cálculo do Custo
        qtd_usada_base = converter_para_base(ing['quantidade_usada'], ing['unidade_usada'])
        qtd_total_base = converter_para_base(ing['quantidade_total'], ing['unidade_total'])
        
        if qtd_total_base > 0:
            custo_unitario_base = ing['valor_total'] / qtd_total_base
            custo_ingrediente = custo_unitario_base * qtd_usada_base
        else:
            custo_ingrediente = 0
        
        custo_total += custo_ingrediente

        # Exibição na tabela
        col1, col2, col3, col4, col5 = st.columns([3,2,2,2,1])
        
        with col1:
            st.write(f"**{ing['nome']}**")
            # Opcional: Mostrar a conversão para depuração
            # st.caption(f"1 {ing['unidade_total']} = R$ {custo_unitario_base:.4f} / base")
        with col2:
            st.write(f"{ing['quantidade_usada']:.2f} {ing['unidade_usada']}")
        with col3:
            st.write(f"R$ {ing['valor_total']:.2f} p/ {ing['quantidade_total']:.2f} {ing['unidade_total']}")
        with col4:
            st.write(f"R$ {custo_ingrediente:.2f}")
        with col5:
            if st.button("🗑️", key=f"del_{i}"):
                indices_para_remover.append(i)

    # st.markdown("---") # Removido para evitar linha dupla com a separação de colunas
    
    # Remover ingredientes
    if indices_para_remover:
        for index in sorted(indices_para_remover, reverse=True):
            st.session_state.ingredientes.pop(index)
        st.rerun() # Usando st.rerun() no lugar do deprecated st.experimental_rerun()

    st.markdown("---")
    st.markdown(f"**Custo Total dos Ingredientes: R$ {custo_total:.2f}**")

    # -----------------------
    # Cálculo do custo unitário
    # -----------------------
    st.subheader("Cálculo do Custo Unitário")
    unidades_produzidas = st.number_input(
        "Quantas unidades (porções) serão produzidas com esta receita?",
        min_value=1,
        value=1,
        key="unidades"
    )
    
    if unidades_produzidas > 0:
        custo_unitario = custo_total / unidades_produzidas
        st.metric(
            label="Custo por Unidade (Ingredientes)",
            value=f"R$ {custo_unitario:.2f}",
            delta_color="off"
        )
else:
    st.info("Adicione seus primeiros ingredientes usando o formulário acima!")

# -----------------------
# Instruções de uso
# -----------------------
with st.expander("ℹ️ Instruções de Uso"):
    st.markdown("""
    1. **Preencha o Formulário** para cada ingrediente:
       - **Nome:** O nome do ingrediente (ex: Farinha de Trigo).
       - **Qtd usada na receita:** A quantidade exata que a sua receita utiliza (ex: 500 g).
       - **Qtd total comprada:** O volume da embalagem que você comprou (ex: 5 kg).
       - **Valor total (R$):** O preço que você pagou pela embalagem (ex: 15,00).
    2. **Conversão Automática:** O sistema converte automaticamente unidades compatíveis (`kg` para `g` e `l` para `ml`) para fazer o cálculo correto, garantindo que o custo unitário seja preciso.
    3. **Calcule o Custo Final:** Informe quantas unidades (porções) a receita rende. O custo final por unidade será exibido.
    4. Use o botão **🗑️** para remover um ingrediente da lista.
    """)

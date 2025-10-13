import streamlit as st

st.set_page_config(page_title="Calculadora de Custos", page_icon="🧮")
st.title("🧮 Calculadora de Custo Unitário com Conversão de Unidades")

st.markdown("""
Adicione os ingredientes e suas quantidades para calcular o custo por unidade do seu produto!
""")

# Inicializar lista de ingredientes na sessão
if "ingredientes" not in st.session_state:
    st.session_state.ingredientes = []

# Função de conversão para gramas/mililitros
def converter_para_base(qtd, unidade):
    """Converte kg->g, l->ml, mantendo g, ml e unidade igual."""
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
        return qtd

# Formulário para adicionar ingredientes
with st.form("ingrediente_form"):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        nome = st.text_input("Nome do Ingrediente")
    with col2:
        quantidade_usada = st.number_input("Qtd usada", min_value=0.0, format="%.2f")
        unidade_usada = st.selectbox("Unidade usada", ["g","kg","ml","l","unidade"], key="u1")
    with col3:
        quantidade_total = st.number_input("Qtd total comprada", min_value=0.0, format="%.2f")
        unidade_total = st.selectbox("Unidade total", ["g","kg","ml","l","unidade"], key="u2")
    with col4:
        valor_total = st.number_input("Valor total (R$)", min_value=0.0, format="%.2f")
    
    submitted = st.form_submit_button("Adicionar Ingrediente")
    if submitted and nome:
        st.session_state.ingredientes.append({
            "nome": nome,
            "quantidade_usada": quantidade_usada,
            "unidade_usada": unidade_usada,
            "quantidade_total": quantidade_total,
            "unidade_total": unidade_total,
            "valor_total": valor_total
        })
        st.experimental_rerun()

# Lista de ingredientes adicionados
if st.session_state.ingredientes:
    st.subheader("Ingredientes Adicionados")
    custo_total = 0
    for i, ing in enumerate(st.session_state.ingredientes):
        col1, col2, col3, col4, col5, col6 = st.columns([3,2,2,2,2,1])
        with col1:
            st.write(f"**{ing['nome']}**")
        with col2:
            st.write(f"Usada: {ing['quantidade_usada']} {ing['unidade_usada']}")
        with col3:
            st.write(f"Comprada: {ing['quantidade_total']} {ing['unidade_total']}")
        with col4:
            # Converter para mesma unidade base
            qtd_usada_base = converter_para_base(ing['quantidade_usada'], ing['unidade_usada'])
            qtd_total_base = converter_para_base(ing['quantidade_total'], ing['unidade_total'])
            if qtd_total_base > 0:
                custo_ingrediente = (ing['valor_total'] / qtd_total_base) * qtd_usada_base
            else:
                custo_ingrediente = 0
            st.write(f"R$ {custo_ingrediente:.2f}")
        with col5:
            st.write(f"R$/base")
        with col6:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.ingredientes.pop(i)
                st.experimental_rerun()
        custo_total += custo_ingrediente

    st.markdown(f"**Custo Total dos Ingredientes: R$ {custo_total:.2f}**")

    # Cálculo do custo unitário
    st.subheader("Cálculo do Custo Unitário")
    unidades_produzidas = st.number_input(
        "Quantas unidades serão produzidas?",
        min_value=1,
        value=1,
        key="unidades"
    )
    
    if unidades_produzidas > 0:
        custo_unitario = custo_total / unidades_produzidas
        st.metric(
            label="Custo por Unidade",
            value=f"R$ {custo_unitario:.2f}"
        )
else:
    st.info("Adicione seus primeiros ingredientes usando o formulário acima!")

# Instruções de uso
with st.expander("ℹ️ Como usar:"):
    st.markdown("""
    1. Adicione cada ingrediente com:
       - Nome (ex: "Farinha")
       - Quantidade usada na receita e unidade (ex: 200 g)
       - Quantidade total comprada e unidade (ex: 2 kg)
       - Valor total pago no ingrediente (ex: 8,50)
    2. Informe quantas unidades serão produzidas
    3. O custo por unidade será calculado automaticamente
    *O sistema agora converte automaticamente unidades compatíveis (kg->g, l->ml)*
    """)

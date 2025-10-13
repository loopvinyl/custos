import streamlit as st

st.set_page_config(page_title="Calculadora de Custos", page_icon="🧮")
st.title("🧮 Calculadora de Custo Unitário")

st.markdown("""
Adicione os ingredientes e suas quantidades para calcular o custo por unidade do seu produto!
""")

# Inicializar lista de ingredientes na sessão
if "ingredientes" not in st.session_state:
    st.session_state.ingredientes = []

# Formulário para adicionar ingredientes
with st.form("ingrediente_form"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nome = st.text_input("Nome do Ingrediente")
    with col2:
        quantidade_usada = st.number_input("Qtd usada", min_value=0.0, format="%.2f")
    with col3:
        quantidade_total = st.number_input("Qtd total comprada", min_value=0.0, format="%.2f")
    with col4:
        valor_total = st.number_input("Valor total (R$)", min_value=0.0, format="%.2f")
    
    submitted = st.form_submit_button("Adicionar Ingrediente")
    if submitted and nome:
        st.session_state.ingredientes.append({
            "nome": nome,
            "quantidade_usada": quantidade_usada,
            "quantidade_total": quantidade_total,
            "valor_total": valor_total
        })
        st.experimental_rerun()

# Lista de ingredientes adicionados
if st.session_state.ingredientes:
    st.subheader("Ingredientes Adicionados")
    custo_total = 0
    for i, ing in enumerate(st.session_state.ingredientes):
        col1, col2, col3, col4, col5 = st.columns([3,2,2,2,1])
        with col1:
            st.write(f"**{ing['nome']}**")
        with col2:
            st.write(f"Usada: {ing['quantidade_usada']}")
        with col3:
            st.write(f"Comprada: {ing['quantidade_total']}")
        with col4:
            # Custo proporcional do ingrediente
            if ing['quantidade_total'] > 0:
                custo_ingrediente = (ing['valor_total'] / ing['quantidade_total']) * ing['quantidade_usada']
            else:
                custo_ingrediente = 0
            st.write(f"R$ {custo_ingrediente:.2f}")
        with col5:
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
       - Quantidade usada na receita (ex: 200 g)
       - Quantidade total comprada (ex: 2 kg)
       - Valor total pago no ingrediente (ex: 8,50)
    2. Informe quantas unidades serão produzidas
    3. O custo por unidade será calculado automaticamente
    *Obs: O sistema não converte unidades! Use a mesma unidade para quantidade usada e total comprada.*
    """)

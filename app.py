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
    col1, col2, col3 = st.columns(3)
    with col1:
        nome = st.text_input("Nome do Ingrediente")
    with col2:
        quantidade = st.number_input("Quantidade", min_value=0.0, format="%.2f")
    with col3:
        valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    
    submitted = st.form_submit_button("Adicionar Ingrediente")
    if submitted and nome:
        st.session_state.ingredientes.append({
            "nome": nome,
            "quantidade": quantidade,
            "valor": valor
        })
        st.rerun()

# Lista de ingredientes adicionados
if st.session_state.ingredientes:
    st.subheader("Ingredientes Adicionados")
    custo_total = 0
    for i, ing in enumerate(st.session_state.ingredientes):
        col1, col2, col3, col4 = st.columns([3,2,2,1])
        with col1:
            st.write(f"**{ing['nome']}**")
        with col2:
            st.write(f"Qtd: {ing['quantidade']}")
        with col3:
            custo_ingrediente = ing['valor']
            st.write(f"R$ {custo_ingrediente:.2f}")
        with col4:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.ingredientes.pop(i)
                st.rerun()
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
       - Quantidade total utilizada (ex: 2 kg)
       - Valor total pago no ingrediente (ex: 8.50)
    2. Informe quantas unidades serão produzidas
    3. O custo por unidade será calculado automaticamente
    *Obs: O sistema não converte unidades! Use a mesma unidade de medida para quantidade e valor.*
    """)

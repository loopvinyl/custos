# Lista de ingredientes adicionados
if st.session_state.ingredientes:
    st.subheader("Ingredientes Adicionados")
    custo_total = 0
    # Lista para marcar índices a remover
    indices_para_remover = []

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
                indices_para_remover.append(i)
        custo_total += custo_ingrediente

    # Remover após o loop
    if indices_para_remover:
        for index in sorted(indices_para_remover, reverse=True):
            st.session_state.ingredientes.pop(index)
        st.experimental_rerun()  # agora fora do loop

    st.markdown(f"**Custo Total dos Ingredientes: R$ {custo_total:.2f}**")

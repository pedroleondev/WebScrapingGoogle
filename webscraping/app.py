import streamlit as st
import sqlite3
import pandas as pd
from crawler_google import Crawler, salvar_produto  # Importa o Crawler e função de salvar

# 📌 Função para conectar ao banco e obter os produtos
def obter_produtos():
    conn = sqlite3.connect("precos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, preco, link FROM produtos ORDER BY id DESC LIMIT 100")  # Limita 100 itens
    produtos = cursor.fetchall()
    conn.close()
    return produtos

# 📌 Função para excluir um produto do banco
def excluir_produto(produto_id):
    conn = sqlite3.connect("precos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()

# 📌 Interface com Streamlit
st.set_page_config(page_title="Rastreamento de Preços", layout="wide")

st.title("🛒 Rastreamento de Preços - Google Shopping")

# 🟢 **Seção: Adicionar um novo produto para pesquisa**
st.header("🔍 Adicionar um novo produto para rastreamento")

produto_input = st.text_input("Digite o nome do produto para pesquisar no Google Shopping:")
if st.button("➕ Adicionar e Buscar"):
    if produto_input:
        st.info(f"Buscando preços para: {produto_input}")
        crawler = Crawler()
        produtos = crawler.coletar_precos_google_shopping(produto_input)  # Executa o crawler

        if produtos:
            for produto in produtos:
                salvar_produto(produto.nome, produto.preco, produto.link)
            st.success("✅ Produtos coletados e armazenados com sucesso!")
        else:
            st.warning("⚠️ Nenhum produto encontrado!")

# 🟢 **Seção: Tabela de Produtos**
st.header("📋 Produtos rastreados")

produtos = obter_produtos()
if produtos:
    df = pd.DataFrame(produtos, columns=["ID", "Nome", "Preço", "Link"])
    
    # Criar coluna de botões para exclusão
    df["Remover"] = df["ID"].apply(lambda x: f"🗑️ Excluir {x}")
    
    # Exibir a tabela no Streamlit
    st.dataframe(df[["ID", "Nome", "Preço", "Link"]], height=400)

    # Criar botões para remover produtos
    excluir_id = st.text_input("Digite o ID para remover:")
    if st.button("❌ Remover Produto"):
        if excluir_id.isnumeric():
            excluir_produto(int(excluir_id))
            st.success(f"Produto ID {excluir_id} removido!")
            st.experimental_rerun()
        else:
            st.warning("⚠️ Insira um ID válido.")

else:
    st.info("Nenhum produto cadastrado ainda.")


# WebScrapingGoogle
### 🛒 Ferramenta com interface web para raspagem de produtos no Google Shopping

🚀 **Monitoramento automático de preços em tempo real!**

Este projeto é uma aplicação **Python** que permite pesquisar produtos no **Google Shopping** e armazenar os preços para consulta futura. Com ele, você pode acompanhar variações de preços e encontrar as melhores ofertas.

![image](https://github.com/user-attachments/assets/aa5d2b34-0f02-4e69-95d4-a9df2cabdf86)

---

## 🔹 Tecnologias Utilizadas:
- **Streamlit** - Interface web simples e interativa  
- **Python + Selenium** - Raspagem de preços no Google Shopping  
- **SQLite** - Armazenamento local de dados  

---

## 📌 Funcionalidades:
✔️ Pesquisar qualquer produto no Google Shopping  
✔️ Armazenar preços automaticamente em um banco de dados  
✔️ Visualizar e gerenciar a lista de produtos rastreados  
✔️ Remover produtos indesejados com um clique  

---

## 📥 Como Instalar e Rodar
### 🔹 1️⃣ Criando o ambiente virtual (Recomendado)
Para evitar conflitos de bibliotecas, **crie um ambiente Conda** antes de instalar as dependências:

```sh
conda create --name webscraping-google python=3.10 -y
conda activate webscraping-google
```

### 🔹 2️⃣ Execute o install do requirements, ou, instale os pacotes essenciais
```sh
pip install -r requirements.txt

pip install streamlit pandas selenium webdriver-manager undetected-chromedriver beautifulsoup4 requests
```

### 🔹 3️⃣ Iniciando o banco de dados
Antes de rodar a aplicação, certifique-se de criar a base de dados:

```sh
python crawler_google.py
```
### 🔹 4️⃣ Rodando a interface web
 ```sh
streamlit run app.py
 ```

Acesse http://localhost:8501 no navegador para visualizar a aplicação 🎉

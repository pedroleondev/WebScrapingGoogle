import json
import time
import sqlite3
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc  # Mantém o original


# BANCO DE DADOS



# 📌 Criar banco de dados e tabela se não existir
def criar_banco():
    conn = sqlite3.connect("precos.db")  # Nome do arquivo do banco
    cursor = conn.cursor()
    
    # Criando a tabela caso ainda não exista
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            link TEXT UNIQUE NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

# Chamando a função para garantir que o banco está pronto
criar_banco()

####

def salvar_produto(nome, preco, link):
    """Salva o produto no banco de dados SQLite"""
    try:
        conn = sqlite3.connect("precos.db")
        cursor = conn.cursor()

        # Insere os dados no banco, ignorando duplicatas pelo link (UNIQUE)
        cursor.execute("""
            INSERT OR IGNORE INTO produtos (nome, preco, link)
            VALUES (?, ?, ?)
        """, (nome, preco, link))

        conn.commit()
        conn.close()
        print(f"✅ Produto salvo: {nome} - R$ {preco}")

    except Exception as e:
        print(f"⚠️ Erro ao salvar produto: {e}")









############################################################################################################




# 🕵️‍♂️**GITHUB ISSUE FIX(OSError: [WinError 6] The handle is invalid
#955) Redefinindo a classe Chrome para evitar OSError**
class Chrome(uc.Chrome):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def quit(self):
        try:
            super().quit()
        except OSError:
            pass  # Ignora o erro OSError ao fechar


# **Classe Produto para armazenar os dados**
class Produto:
    def __init__(self, nome, preco, link):
        self.nome = nome
        self.preco = preco
        self.link = link

    def to_dict(self):
        return {"nome": self.nome, "preco": self.preco, "link": self.link}


# **Classe Crawler para gerenciar o WebDriver e a coleta**
class Crawler:
    def __init__(self):
        """Inicia o WebDriver com a classe modificada para evitar OSError"""
        self.driver = self.iniciar_driver()

    def iniciar_driver(self):
        """Inicia o Chrome indetectável sem erro ao fechar"""
        options = uc.ChromeOptions()
        options.add_argument("--headless")  # Rodar sem interface gráfica
        options.add_argument("--disable-gpu") # Evitar erro de GPU
        options.add_argument("--no-sandbox") # Evitar erro de sandbox
        options.add_argument("--disable-blink-features=AutomationControlled") # Evitar detecção
        # options.add_argument("start-maximized") # Iniciar maximizado

        driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    
    def coletar_precos_google_shopping(self, query):
        """Coleta preços do Google Shopping"""
        if not self.driver:
            return []

        try:
            base_url = f"https://www.google.com/search?tbm=shop&q={query.replace(' ', '+')}"
            self.driver.get(base_url)
            time.sleep(5)

            produtos = []
            itens = self.driver.find_elements(By.CSS_SELECTOR, "div.sh-dgr__content")

            for item in itens:
                try:
                    """Capturar o nome, preço e link do produto com css selector"""
                    nome = item.find_element(By.CSS_SELECTOR, "h3.tAxDx").text.strip()
                    preco = item.find_element(By.CSS_SELECTOR, "span.a8Pemb.OFFNJ").text.replace("+ impostos", "").strip()
                    link = item.find_element(By.CSS_SELECTOR, "a.shntl").get_attribute("href")
                    
                    # Salvar no banco SQLite

                    salvar_produto(nome, preco, link)
                    
                    
                    produtos.append(Produto(nome, preco, link))
                except Exception:
                    continue  

            return produtos
        except Exception as e:
            print(f"Erro ao acessar o Google Shopping: {e}")
            return []

    def fechar_driver(self):
        """Fecha o driver manualmente quando necessário"""
        if self.driver:
            self.driver.quit()

# **🟢 Criando o Crawler**
crawler = Crawler()

# **🟢 Testando com um exemplo**
produtos = crawler.coletar_precos_google_shopping("placa de vídeo RTX 3060")

# **🟢 Retornar os dados formatados em JSON**
json_produtos = json.dumps([produto.to_dict() for produto in produtos], indent=4, ensure_ascii=False)
print(json_produtos)

# **🟢 Fechando o driver manualmente**
crawler.fechar_driver()

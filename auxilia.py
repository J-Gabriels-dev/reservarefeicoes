from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule as sch

tabela = pd.read_csv("logins.csv", sep= ";", dtype=str)

def refeicoes():
    navegador = webdriver.Firefox()
    acao = ActionChains(navegador)
    
    # Login 
    time.sleep(3)
    navegador.get("http://angical.ifpi.edu.br/sari/login.jsf")
    for posicao in tabela.index:
        navegador.get("http://angical.ifpi.edu.br/sari/login.jsf")
        cpf = tabela.loc[posicao,"cpf"]
        navegador.find_element(By.ID, "j_username").send_keys(cpf)

        senha = tabela.loc[posicao,"senha"]
        navegador.find_element(By.ID, "j_password").send_keys(senha)

        navegador.find_element(By.NAME, "j_idt24").click()

        # Espera e clica em "Gerenciar conta"
        botao_gerenciar_conta = WebDriverWait(navegador,20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='btnGerenciaMinhaConta']"))
        )
        time.sleep(2)
        botao_gerenciar_conta.click()

        # Passa o mouse em "Solicitar ticket"
        botao_solicitar_ticket = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form[2]/div/ul/li[2]"))
        )
        acao.move_to_element(botao_solicitar_ticket).perform()

        # Clica em "Solicitar ticket"
        solicitar_ticket = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "btnCompraTicketUsuario"))
        )
        solicitar_ticket.click()

        time.sleep(2)
        primeiroTicket = navegador.find_element(By.XPATH, "//button[@title='Adicionar Ticket']")

        primeiroTicket.click()

        time.sleep(2)
        segundoTicket = navegador.find_element(By.XPATH, "//button[@title='Adicionar Ticket']")

    
        segundoTicket.click()

        time.sleep(2)
        sair = navegador.find_element(By.XPATH,"/html/body/div[13]/div[1]/a[1]/span")
        sair.click()
        
        sair_do_sari = WebDriverWait(navegador,10).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/form[2]/div/ul/li[3]/a"))
        )

        acao.move_to_element(sair_do_sari).perform()
    
        sair_do_sistema = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((By.ID, "j_idt27"))
        )
        sair_do_sistema.click()

        nome = tabela.loc[posicao,"nome"]
        print(f"Refeição do(a) {nome} Feita !")

if __name__ == "__main__":
    refeicoes()
    sch.every().monday.at("20:30").do(refeicoes)
    sch.every().tuesday.at("20:30").do(refeicoes)
    sch.every().wednesday.at("20:30").do(refeicoes)
    sch.every().thursday.at("20:30").do(refeicoes)
    sch.every().friday.at("20:30").do(refeicoes)
    sch.every().sunday.at("20:30").do(refeicoes)

    while True:
        sch.run_pending()
        time.sleep(1)

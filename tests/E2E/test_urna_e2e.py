import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestUrnaE2E(unittest.TestCase):

    def setUp(self):
        self.BASE_URL = "http://127.0.0.1:5000"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(self.BASE_URL)
        self.wait = WebDriverWait(self.driver, 10)

    def clicar_numero(self, numero):
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[text()='{numero}']")))
        btn.click()
        time.sleep(0.5) # Pausa meio segundo ao digitar cada número

    def test_fluxo_completo_votacao(self):
        time.sleep(2) # Pausa 2 segundos na tela inicial para você ver o menu

        # ==========================================
        # 1. VOTO EM BRANCO (Prefeito)
        # ==========================================
        btn_prefeito = self.wait.until(EC.element_to_be_clickable((By.ID, "btn-Prefeito")))
        btn_prefeito.click()
        time.sleep(1) # Pausa para ver a tela do Prefeito

        btn_branco = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-branco")))
        btn_branco.click()
        time.sleep(1) # Pausa para ver o aviso de "VOTO EM BRANCO"

        btn_confirma = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-confirma")))
        btn_confirma.click()
        time.sleep(1) # Pausa ao voltar pro menu

        # ==========================================
        # 2. CORREÇÃO E VOTO NULO (Governador)
        # ==========================================
        btn_governador = self.wait.until(EC.element_to_be_clickable((By.ID, "btn-Governador")))
        btn_governador.click()
        time.sleep(1)

        self.clicar_numero('9')
        self.clicar_numero('9')
        time.sleep(1) # Vê a tela mostrando VOTO NULO

        btn_corrige = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-corrige")))
        btn_corrige.click()
        time.sleep(1) # Vê a tela limpar após corrigir

        self.clicar_numero('9')
        self.clicar_numero('9')
        time.sleep(1)
        btn_confirma.click()
        time.sleep(1)

        # ==========================================
        # 3. VOTO VÁLIDO NO CANDIDATO (Presidente)
        # ==========================================
        btn_presidente = self.wait.until(EC.element_to_be_clickable((By.ID, "btn-Presidente")))
        btn_presidente.click()
        time.sleep(1)

        self.clicar_numero('9')
        self.clicar_numero('0')
        time.sleep(1) # Vê a foto e os dados do candidato Pedro Paulo

        btn_confirma.click()
        time.sleep(2) # Pausa maior para ver a transição para o relatório

        # ==========================================
        # 4. VERIFICAR A IMPRESSÃO DO VOTO (Relatório)
        # ==========================================
        btn_imprimir = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Imprimir Relatório')]")))
        btn_imprimir.click()
        time.sleep(3) # Pausa 3 segundos para você ler a tabela de relatório final

        tabela = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        self.assertTrue(tabela.is_displayed())

        texto_relatorio = tabela.text
        self.assertIn("Voto em Branco", texto_relatorio)
        self.assertIn("Voto Nulo", texto_relatorio)
        self.assertIn("Pedro Paulo", texto_relatorio)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
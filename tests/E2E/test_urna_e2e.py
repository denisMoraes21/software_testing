import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class TestUrnaE2E(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Inicializa o navegador uma única vez para todas as etapas"""
        cls.BASE_URL = "http://127.0.0.1:5000"
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.get(cls.BASE_URL)
        cls.wait = WebDriverWait(cls.driver, 10)

        # Nome único baseado no tempo para evitar conflitos no banco
        cls.nome_eleitor = f"Eleitor_Robo_{int(time.time())}"

    @classmethod
    def tearDownClass(cls):
        """Fecha o navegador apenas depois de rodar todas as etapas"""
        time.sleep(3)
        cls.driver.quit()

    def clicar_numero(self, numero):
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[text()='{numero}']")))
        btn.click()
        time.sleep(0.5)

    # ==========================================
    # ETAPA 1: CADASTRO E LIBERAÇÃO
    # ==========================================
    def test_01_criar_e_liberar_eleitor(self):
        time.sleep(2)  # Pausa para carregar a tela do mesário

        # Criar o Eleitor
        input_eleitor = self.wait.until(EC.presence_of_element_located((By.ID, "novo-eleitor")))
        input_eleitor.send_keys(self.nome_eleitor)
        time.sleep(1)

        btn_adicionar = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Adicionar')]")
        btn_adicionar.click()
        time.sleep(2)  # Espera a tabela do banco de dados atualizar

        # Liberar a Urna
        xpath_liberar = f"//tr[td[contains(text(), '{self.nome_eleitor}')]]//button[contains(text(), 'Liberar Urna')]"
        btn_liberar = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_liberar)))
        btn_liberar.click()
        time.sleep(1)

    # ==========================================
    # ETAPA 2: VOTO EM BRANCO (Prefeito)
    # ==========================================
    def test_02_voto_branco_prefeito(self):
        btn_prefeito = self.wait.until(EC.element_to_be_clickable((By.ID, "btn-Prefeito")))
        btn_prefeito.click()
        time.sleep(1)

        btn_branco = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-branco")))
        btn_branco.click()
        time.sleep(1)

        btn_confirma = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-confirma")))
        btn_confirma.click()
        time.sleep(1)

    # ==========================================
    # ETAPA 3: CORREÇÃO E VOTO NULO (Governador)
    # ==========================================
    def test_03_voto_nulo_governador(self):
        btn_governador = self.wait.until(EC.element_to_be_clickable((By.ID, "btn-Governador")))
        btn_governador.click()
        time.sleep(1)

        # Digita errado para testar o corrige
        self.clicar_numero('9')
        self.clicar_numero('9')
        time.sleep(1)

        btn_corrige = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-corrige")))
        btn_corrige.click()
        time.sleep(1)

        # Digita e confirma o nulo
        self.clicar_numero('9')
        self.clicar_numero('9')
        time.sleep(1)

        btn_confirma = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-confirma")))
        btn_confirma.click()
        time.sleep(1)

    # ==========================================
    # ETAPA 4: VOTO VÁLIDO E FIM DA SESSÃO
    # ==========================================
    def test_04_voto_valido_presidente_e_alerta(self):
        btn_presidente = self.wait.until(EC.element_to_be_clickable((By.ID, "btn-Presidente")))
        btn_presidente.click()
        time.sleep(1)

        self.clicar_numero('9')
        self.clicar_numero('0')
        time.sleep(1)

        btn_confirma = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-confirma")))
        btn_confirma.click()

        # Trata o alerta de sucesso
        alerta = self.wait.until(EC.alert_is_present())
        self.assertEqual(alerta.text, "Sessão encerrada com sucesso!")
        time.sleep(1)
        alerta.accept()
        time.sleep(2)  # Espera voltar para o painel do mesário

    # ==========================================
    # ETAPA 5: VALIDAÇÃO DOS RESULTADOS NO PAINEL
    # ==========================================
    def test_05_validar_bloqueio_e_relatorio(self):
        # Verificar se o botão mudou para "Já Votou" e está desativado
        xpath_bloqueado = f"//tr[td[contains(text(), '{self.nome_eleitor}')]]//button[contains(text(), 'Já Votou')]"
        btn_ja_votou = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_bloqueado)))
        self.assertFalse(btn_ja_votou.is_enabled(), "O botão deveria estar desativado após os 3 votos!")
        time.sleep(1)

        # Verificar a impressão dos votos no relatório
        xpath_ver_votos = f"//tr[td[contains(text(), '{self.nome_eleitor}')]]//button[contains(text(), 'Ver Votos')]"
        btn_ver_votos = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_ver_votos)))
        btn_ver_votos.click()
        time.sleep(2)

        tabela = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tabela-relatorio table")))
        self.assertTrue(tabela.is_displayed())

        texto_relatorio = tabela.text
        self.assertIn("Voto em Branco", texto_relatorio)
        self.assertIn("Voto Nulo", texto_relatorio)
        self.assertIn("Pedro Paulo", texto_relatorio)


if __name__ == "__main__":
    unittest.main()
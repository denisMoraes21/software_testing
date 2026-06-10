import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestPessoaE2E(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def obter_alerta(self):

        wait = WebDriverWait(
            self.driver,
            10
        )

        return wait.until(
            EC.alert_is_present()
        )

    def preencher_formulario(
            self,
            nome="Joao Silva",
            cpf="11144477735",
            email="joao@gmail.com",
            cep="69050010"
    ):

        driver = self.driver

        driver.get(
            "http://127.0.0.1:5000/pessoas/register"
        )

        driver.find_element(
            By.ID,
            "nome_completo"
        ).send_keys(nome)

        driver.find_element(
            By.ID,
            "cpf"
        ).send_keys(cpf)

        driver.find_element(
            By.ID,
            "data_nascimento"
        ).send_keys("2000-01-01")

        driver.find_element(
            By.ID,
            "sexo"
        ).send_keys("Masculino")

        driver.find_element(
            By.ID,
            "estado_civil"
        ).send_keys("Solteiro")

        driver.find_element(
            By.ID,
            "nacionalidade"
        ).send_keys("Brasileiro")

        driver.find_element(
            By.ID,
            "telefone"
        ).send_keys("9233334444")

        driver.find_element(
            By.ID,
            "celular"
        ).send_keys("92999998888")

        driver.find_element(
            By.ID,
            "email"
        ).send_keys(email)

        driver.find_element(
            By.ID,
            "cep"
        ).send_keys(cep)

        driver.find_element(
            By.ID,
            "logradouro"
        ).send_keys("Rua A")

        driver.find_element(
            By.ID,
            "numero"
        ).send_keys("10")

        driver.find_element(
            By.ID,
            "bairro"
        ).send_keys("Centro")

        driver.find_element(
            By.ID,
            "cidade"
        ).send_keys("Manaus")

        driver.find_element(
            By.ID,
            "estado"
        ).send_keys("AM")

    def test_cadastro_sucesso(self):

        self.preencher_formulario(
            cpf="39053344705",
            email="sucesso@gmail.com"
        )

        self.driver.find_element(
            By.ID,
            "button-create"
        ).click()

        alert = self.obter_alerta()

        self.assertEqual(
            alert.text,
            "Pessoa cadastrada com sucesso!"
        )

        alert.accept()

    def test_cpf_invalido(self):

        self.preencher_formulario(
            cpf="12345678900"
        )

        self.driver.find_element(
            By.ID,
            "button-create"
        ).click()

        alert = self.obter_alerta()

        self.assertEqual(
            alert.text,
            "CPF inválido"
        )

        alert.accept()

    def test_email_invalido(self):

        self.preencher_formulario(
            email="joao@gmail"
        )

        self.driver.find_element(
            By.ID,
            "button-create"
        ).click()

        alert = self.obter_alerta()

        self.assertEqual(
            alert.text,
            "E-mail inválido"
        )

        alert.accept()

    def test_nome_sem_sobrenome(self):

        self.preencher_formulario(
            nome="Joao"
        )

        self.driver.find_element(
            By.ID,
            "button-create"
        ).click()

        alert = self.obter_alerta()

        self.assertEqual(
            alert.text,
            "Informe nome e sobrenome"
        )

        alert.accept()

    def test_cep_invalido(self):

        self.preencher_formulario(
            cep="123"
        )

        self.driver.find_element(
            By.ID,
            "button-create"
        ).click()

        alert = self.obter_alerta()

        self.assertEqual(
            alert.text,
            "CEP inválido"
        )

        alert.accept()


# if __name__ == "__main__":
#     unittest.main()
from unittest import TestCase

from dask.dataframe.core import quantile

from leilao.dominio import Usuario, Lance, Leilao


class TestLeilao(TestCase):

    def setUp(self):
        self.edson = Usuario('Edson')
        self.lance_do_edson = Lance(self.edson, 100.0)
        self.leilao = Leilao('Celular')

    def test_deve_retornar_o_maior_e_o_menor_valor_de_um_lance_quando_adicionados_em_ordem_crescente(self):
        tayne = Usuario('Taynê')

        lance_da_tayne = Lance(tayne, 150.0)
        self.leilao.propoe(self.lance_do_edson)
        self.leilao.propoe(lance_da_tayne)

        menor_valor_esperado = 100.0
        maior_valor_esperado = 150.0

        self.assertEqual(menor_valor_esperado, self.leilao.menor_lance)
        self.assertEqual(maior_valor_esperado, self.leilao.maior_lance)

    def test_nao_deve_permitir_propor_um_lance_em_ordem_descrescente(self):

        with self.assertRaises(ValueError):
            tayne = Usuario('Taynê')
            lance_da_tayne = Lance(tayne, 150.0)
            self.leilao.propoe(lance_da_tayne)
            self.leilao.propoe(self.lance_do_edson)

    def test_deve_retornar_o_mesmo_valor_para_o_maior_e_o_menor_valor_quando_leilao_tiver_um_lance(self):
        self.leilao.propoe(self.lance_do_edson)

        self.assertEqual(100.0, self.leilao.menor_lance)
        self.assertEqual(100.0, self.leilao.maior_lance)

    def test_deve_retornar_o_maior_e_o_menor_valor_quando_o_leilao_tiver_tres_lances(self):
        telma = Usuario('Telma')
        tayne = Usuario('Taynê')

        lance_da_tayne = Lance(tayne, 150.0)
        lance_da_telma = Lance(telma, 200.0)

        self.leilao.propoe(self.lance_do_edson)
        self.leilao.propoe(lance_da_tayne)
        self.leilao.propoe(lance_da_telma)

        menor_valor_esperado = 100.0
        maior_valor_esperado = 200.0

        self.assertEqual(menor_valor_esperado, self.leilao.menor_lance)
        self.assertEqual(maior_valor_esperado, self.leilao.maior_lance)

    # se o leilao não tiver lances, deve permitir propor um lance
    def test_deve_permitir_propor_um_lance_caso_o_leilao_não_tenha_lances(self):
        self.leilao.propoe(self.lance_do_edson)

        quantidade_de_lances_recebida = len(self.leilao.lances)

        self.assertEqual(1, quantidade_de_lances_recebida)

    # se o ultimo usuario for diferente, deve permitir propor o lance
    def test_deve_permitir_propor_um_lance_caso_o_ultimo_usuario_seja_diferente(self):
        tayne = Usuario('Taynê')
        lance_da_tayne = Lance(tayne, 200.0)

        self.leilao.propoe(self.lance_do_edson)
        self.leilao.propoe(lance_da_tayne)

        quantidade_de_lances_recebidos = len(self.leilao.lances)

        self.assertEqual(2, quantidade_de_lances_recebidos)

    # se o ultimo usuario for o mesmo, não deve permitir propor o lance
    def test_nao_deve_permitir_propor_lance_caso_o_usuario_seja_o_mesmo(self):
        lance_do_edson200 = Lance(self.edson, 200.0)

        with self.assertRaises(ValueError):
            self.leilao.propoe(self.lance_do_edson)
            self.leilao.propoe(lance_do_edson200)

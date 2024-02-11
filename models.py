from main import db, app
import openpyxl
import logging
import os
import time
import pandas as pd


class CollectionPlanilhas:
    def __init__(self):
        self.planilhas = []

    def adicionar_planilha(self, planilha):
        self.planilhas.append(planilha)

    def processar_todas_planilhas(self):
        informacoes_gerais = []

        for planilha in self.planilhas:
            informacoes_planilha = planilha.processar_planilha()
            informacoes_gerais.append(informacoes_planilha)

        return informacoes_gerais


class Planilhas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)
    arquivo = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

    def processar_planilha(self):
        categorias_e_funcoes = {
            'Servicos': self.processar_planilha_servicos,
            'IGPD': self.processar_planilha_igpd,
        }
        return categorias_e_funcoes.get(self.categoria, None)()

    def processar_planilha_servicos(self):
        try:
            # Carregar a planilha
            excel_arq = os.path.join(app.config['UPLOAD_EXCEL_PATH'], self.arquivo )
            wb = openpyxl.load_workbook(excel_arq)
            sheet = wb.active

            # Extrair dados
            data = {}
            for row in sheet.iter_rows(min_row=2):
                instituicao = row[0].value
                mes_ano = row[1].value
                valor = row[2].value
                data.setdefault(instituicao, {})[mes_ano] = valor

            # Gerar informações processadas
            informacoes_processadas = []
            for instituicao, meses_valores in data.items():
                for mes_ano, valor in meses_valores.items():
                    try:
                        mes_ano_str = str(mes_ano)
                        variacao = self.calcular_variacao(valor, data[instituicao].get(mes_ano_str[:-2]))

                    except ZeroDivisionError:
                        variacao = None
                    informacoes_processadas.append({
                        'instituicao': instituicao,
                        'mes_ano': mes_ano_str,
                        'valor': valor,
                        'variacao': variacao,
                    })

            return informacoes_processadas

        except Exception as e:
            # Registrar o erro em um arquivo de log
            logging.error(f"Erro ao processar planilha: {e}")
            # Retornar um valor vazio para indicar que a função falhou
            return []

    def calcular_variacao(self, valor_atual, valor_anterior):
        if valor_anterior is None:
            return None
        return round((valor_atual - valor_anterior) / valor_anterior * 100, 2)

    def processar_planilha_igpd(self):
        # Lógica específica para planilhas do tipo 'IGPD'
        print('IGPD')
        return {'mensagem': f'Processando planilha IGPD: {self.nome}'}


class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class ManipuladorPlanilha:
    def __init__(self, app):
        self.app = app

    def salvar_planilha(self, arquivo, nova_planilha):
        timestamp = time.time()
        caminho_arquivo = self._gerar_caminho_arquivo(nova_planilha, timestamp)
        arquivo.save(caminho_arquivo)
        return caminho_arquivo

    def ler_planilha(self, caminho_arquivo):
        return pd.read_excel(caminho_arquivo, engine='openpyxl')

    def _gerar_caminho_arquivo(self, nova_planilha, timestamp):
        nome_arquivo = f'excel{nova_planilha.id}-{timestamp}.xlsx'
        return os.path.join(self.app.config['UPLOAD_EXCEL_PATH'], nome_arquivo)


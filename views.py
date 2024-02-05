from flask import render_template, redirect, session, url_for, request, flash
from helpers import FormularioPlanilha
from models import Planilhas
from main import app, db
import time
import os
import pandas as pd
from pymongo import MongoClient

# Classe para manipulação de planilhas
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


@app.route('/nova')
def nova():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('nova')))

    form = FormularioPlanilha()

    return render_template('nova.html', titulo='Nova Planilha', form=form)


@app.route('/upload_planilha', methods=['POST',])
def upload_planilha():
    form = FormularioPlanilha(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('nova'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    planilha = Planilhas.query.filter_by(nome=nome).first()

    if planilha:
        flash('Planilha já existente!')
        return redirect(url_for('index'))

    nova_planilha = Planilhas(nome=nome, categoria=categoria, console=console)
    db.session.add(nova_planilha)
    db.session.commit()

    arquivo = request.files['arquivo']
#    upload_path = app.config['UPLOAD_EXCEL_PATH']
#    timestamp = time.time()
#    arquivo.save(f'{upload_path}/excel{nova_planilha.id}-{timestamp}.xlsx')

    manipulador_planilha = ManipuladorPlanilha(app)
    caminho_arquivo = manipulador_planilha.salvar_planilha(arquivo, nova_planilha)

    # Agora você pode ler a planilha se necessário
    dados_planilha = manipulador_planilha.ler_planilha(caminho_arquivo)
    client = MongoClient('localhost', 27017)  # Assuming MongoDB is running on the default port
    dbmg = client['planilhas']  # Replace 'your_database_name' with your actual database name
    collection = dbmg['travelex']  # Replace 'your_collection_name' with your actual collection name

    # Assuming dados_planilha is your DataFrame
    for index, row in dados_planilha.iterrows():
        login_email = row['login/email']
        cnpj_cpf = row['CNPJ/CPF']
        nome = row['NOME']
        limite = row['LIMITE']
        moedas = row['MOEDAS']
        custo_compra_d0 = row['CUSTO COMPRA = D0']
        custo_compra_d1 = row['CUSTO COMPRA = D1']
        custo_compra_d2 = row['CUSTO COMPRA = D2']
        custo_venda_d0 = row['CUSTO VENDA = D0']
        custo_venda_d1 = row['CUSTO VENDA = D1']
        custo_venda_d2 = row['CUSTO VENDA = D2']
        spread_compra_d0 = row['SPREAD COMPRA = D0']
        spread_compra_d1 = row['SPREAD COMPRA = D1']
        spread_compra_d2 = row['SPREAD COMPRA = D2']
        spread_venda_d0 = row['SPREAD VENDA = D0']
        spread_venda_d1 = row['SPREAD VENDA = D1']
        spread_venda_d2 = row['SPREAD VENDA = D2']
        data_pagamento = row['Data Pagamento']
        data_recebimento = row['Data Recebimento']
        tarifa = row['Tarifa']

        # Create a "cotação" string using the information from the row
        cotation = f"{'=' * 20} Cotação {index + 1} {'=' * 20}\n"
        cotation += f"Login/Email: {login_email}\n"
        cotation += f"CNPJ/CPF: {cnpj_cpf}\n"
        cotation += f"Nome: {nome}\n"
        cotation += f"Limite: {limite}\n"
        cotation += f"Moedas: {moedas}\n"
        cotation += f"Custo Compra (D0, D1, D2): {custo_compra_d0}, {custo_compra_d1}, {custo_compra_d2}\n"
        cotation += f"Custo Venda (D0, D1, D2): {custo_venda_d0}, {custo_venda_d1}, {custo_venda_d2}\n"
        cotation += f"Spread Compra (D0, D1, D2): {spread_compra_d0}, {spread_compra_d1}, {spread_compra_d2}\n"
        cotation += f"Spread Venda (D0, D1, D2): {spread_venda_d0}, {spread_venda_d1}, {spread_venda_d2}\n"
        cotation += f"Data Pagamento: {data_pagamento}\n"
        cotation += f"Data Recebimento: {data_recebimento}\n"
        cotation += f"Tarifa: {tarifa}\n"

        print(cotation)
        print('\n')  # Separating each "cotação" for better readability

        # Create a dictionary from the row data
        cotation_data = {
            'login_email': login_email,
            'cnpj_cpf': cnpj_cpf,
            'nome': nome,
            'limite': limite,
            'moedas': moedas,
            'custo_compra_d0': custo_compra_d0,
            'custo_compra_d1': custo_compra_d1,
            'custo_compra_d2': custo_compra_d2,
            'custo_venda_d0': custo_venda_d0,
            'custo_venda_d1': custo_venda_d1,
            'custo_venda_d2': custo_venda_d2,
            'spread_compra_d0': spread_compra_d0,
            'spread_compra_d1': spread_compra_d1,
            'spread_compra_d2': spread_compra_d2,
            'spread_venda_d0': spread_venda_d0,
            'spread_venda_d1': spread_venda_d1,
            'spread_venda_d2': spread_venda_d2,
            'data_pagamento': data_pagamento,
            'data_recebimento': data_recebimento,
            'tarifa': tarifa
        }

        # Insert the data into the MongoDB collection
        collection.insert_one(cotation_data)

    # Close the MongoDB connection
    client.close()

    return redirect(url_for('index'))

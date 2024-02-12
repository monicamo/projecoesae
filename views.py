from flask import render_template, redirect, session, url_for, request, flash
from helpers import FormularioPlanilha
from models import Planilhas, Ativo
from main import app, db
import time
import os
from pymongo import MongoClient
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'xlsx'}


@app.route('/gerar_noticia/<ativo_id>')
def gerar_noticia(ativo_id):
    ativo = Ativo.get_ativo_by_id(ativo_id)

    client = MongoClient('localhost', 27017)
    db = client['planilhas']
    collection = db['noticias']

    nova_noticia = {
        "instituicao": ativo.instituicao,
        "codigo": ativo.codigo,
        "periodo": ativo.periodo,
        "valor": ativo.valor,
        "descricao": ativo.descricao,
        "data_insercao": ativo.data_insercao,
        "hora_insercao": ativo.hora_insercao
    }
    collection.insert_one(nova_noticia)
    client.close()

    return render_template('noticia.html', ativo=ativo)


@app.route('/listar-ativos')
def listar_ativos():
    client = MongoClient('localhost', 27017)
    db = client['planilhas']
    colecao_ativos = db['ativos']

    ativos = colecao_ativos.find()

    return render_template('lista-ativos.html', titulo='Ativos', ativos=ativos)


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
    arquivo = request.files['arquivo']

    planilha = Planilhas.query.filter_by(nome=nome).first()

    if planilha:
        flash('Planilha já existente!')
        return redirect(url_for('index'))

    nova_planilha = Planilhas(nome=nome, categoria=categoria, console=console)
    db.session.add(nova_planilha)
    db.session.commit()

    upload_path = app.config['UPLOAD_EXCEL_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/excel{nova_planilha.id}-{timestamp}.xlsx')

    manipulador_planilha = ManipuladorPlanilha(app)
    caminho_arquivo = manipulador_planilha.salvar_planilha(arquivo, nova_planilha)

    # Agora você pode ler a planilha se necessário
    dados_planilha = manipulador_planilha.ler_planilha(caminho_arquivo)
    client = MongoClient('localhost', 27017)
    dbmg = client['planilhas']
    collection = dbmg['ativos']  #

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


@app.route('/upload_planilha_mongo', methods=['POST'])
def upload_planilha_mongo():
    form = FormularioPlanilha(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('nova'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    # Verifica se um arquivo foi enviado
    if 'arquivo' not in request.files:
        flash('Nenhum arquivo enviado')
        return redirect(url_for('nova'))

    arquivo = request.files['arquivo']

    # Verifica se o nome do arquivo está vazio
    if arquivo.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('nova'))

    # Verifica se o arquivo tem uma extensão permitida
    if arquivo and allowed_file(arquivo.filename):
        # Salva o arquivo no sistema de arquivos
        filename = secure_filename(arquivo.filename)
        arquivo.save(os.path.join(app.config['UPLOAD_EXCEL_PATH'], filename))

    try:
        # Inicia uma transação no banco de dados
        db.session.begin()

        # Verifica se a planilha já existe
        planilha_existente = Planilhas.query.filter_by(nome=nome).first()
        if planilha_existente:
            flash('Planilha já existente!')
            return redirect(url_for('nova'))

        # Cria uma nova instância de Planilhas
        nova_planilha = Planilhas(nome=nome, categoria=categoria, console=console, arquivo=filename)
        db.session.add(nova_planilha)
        db.session.commit()  # Commit da transação bem-sucedida

        # Lógica de processamento específica para cada tipo de planilha
        informacoes_processadas = nova_planilha.processar_planilha()

        client = MongoClient('localhost', 27017)
        dbmg = client['planilhas']
        colecao_ativos = dbmg['ativos']

        print(informacoes_processadas)

        colecao_ativos.insert_many(informacoes_processadas)

        flash('Planilha processada com sucesso!')
        return redirect(url_for('index'))

    except Exception as e:
        # Em caso de erro, realiza rollback da transação
        db.session.rollback()
        flash(f'Erro durante o upload da planilha: {str(e)}')
        return redirect(url_for('index'))

    finally:
        # Finaliza a transação
        db.session.close()

    # Close the MongoDB connection
    client.close()

    return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



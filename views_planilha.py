from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from main import app, db
from models import Planilhas, Usuarios
from helpers import recupera_imagem, deleta_arquivo, FormularioPlanilha, FormularioUsuario
import time


@app.route('/')
def index():
    lista = Planilhas.query.order_by(Planilhas.id)
    return render_template('lista.html', titulo='Planilhas', planilhas=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioPlanilha()
    return render_template('novo.html', titulo='Nova Planilha', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioPlanilha(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

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
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{nova_planilha.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    
    planilha = Planilhas.query.filter_by(id=id).first()
    form = FormularioPlanilha()
    form.nome.data = planilha.nome
    form.categoria.data = planilha.categoria
    form.console.data = planilha.console
    capa_planilha = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Planilha', id=id, capa_planilha=capa_planilha, form=form)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioPlanilha(request.form)

    if form.validate_on_submit():
        planilha = Planilhas.query.filter_by(id=request.form['id']).first()
        planilha.nome = form.nome.data
        planilha.categoria = form.categoria.data
        planilha.console = form.console.data

        db.session.add(planilha)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(id)
        arquivo.save(f'{upload_path}/capa{planilha.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Planilhas.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Planilha deletada com sucesso!')

    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
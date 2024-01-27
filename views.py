from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from main import app, db
from models import Planilhas, Usuarios
from helpers import recupera_imagem, deleta_arquivo
import time


@app.route('/')
def index():
    lista = Planilhas.query.order_by(Planilhas.id)
    return render_template('lista.html', titulo='Planilhas', planilhas=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Nova Planilha')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    planilha = Planilhas.query.filter_by(nome=nome).first()

    if planilha:
        flash('Planilha já existente!')
        return redirect(url_for('index'))

    novo_planilha = Planilhas(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_planilha)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa_{novo_planilha.id}_{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))

    planilha = Planilhas.query.filter_by(id=id).first()
    capa_planilha = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Planilha', planilha=planilha, capa_planilha=capa_planilha)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    planilha = Planilhas.query.filter_by(id=request.form['id']).first()
    planilha.nome = request.form['nome']
    planilha.categoria = request.form['categoria']
    planilha.console = request.form['console']

    db.session.add(planilha)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()

    deleta_arquivo(planilha.id)
    arquivo.save(f'{upload_path}/capa_{planilha.id}_{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    Planilhas.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Planilha deletada com sucesso')

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

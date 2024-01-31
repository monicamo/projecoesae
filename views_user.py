from flask import render_template, request, redirect, session, flash, url_for
from helpers import FormularioUsuario
from main import app
from models import Usuarios
from bcrypt import checkpw

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)

    if form.validate():  # Verifica se o formulário é válido
        usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
        senha_armazenada = usuario.senha.encode('utf-8')
        senha = checkpw(form.senha.data.encode('utf-8'), senha_armazenada)
        if usuario and senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form.get('proxima', url_for('index'))
            return redirect(proxima_pagina)

    flash('Usuário não logado.')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

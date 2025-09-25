from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/site_integrado_expresso/src/instance/expresso_itaporanga.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos do banco de dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    perfil = db.Column(db.String(20), default='operador')
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

class Entrega(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_rastreamento = db.Column(db.String(20), unique=True, nullable=False)
    
    # Dados do remetente
    remetente_nome = db.Column(db.String(100), nullable=False)
    remetente_endereco = db.Column(db.Text, nullable=False)
    remetente_cidade = db.Column(db.String(100), nullable=False)
    
    # Dados do destinatário
    destinatario_nome = db.Column(db.String(100), nullable=False)
    destinatario_endereco = db.Column(db.Text, nullable=False)
    destinatario_cidade = db.Column(db.String(100), nullable=False)
    
    # Dados da mercadoria
    tipo_produto = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.Float)
    valor_declarado = db.Column(db.Float)
    observacoes = db.Column(db.Text)
    
    # Status e controle
    status = db.Column(db.String(20), default='pendente')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

# Rotas do site institucional
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/contato', methods=['POST'])
def processar_contato():
    try:
        # Coletar dados do formulário
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone', '')
        assunto = request.form.get('assunto')
        mensagem = request.form.get('mensagem')
        
        # Criar email
        email_corpo = f"""
        Nova mensagem recebida através do site da Expresso Itaporanga:
        
        Nome: {nome}
        Email: {email}
        Telefone: {telefone}
        Assunto: {assunto}
        
        Mensagem:
        {mensagem}
        
        ---
        Mensagem enviada automaticamente pelo site da Expresso Itaporanga
        """
        
        # Simular envio de email (em produção, configurar SMTP real)
        print("=" * 50)
        print("NOVO EMAIL RECEBIDO")
        print("=" * 50)
        print(f"Para: comercial@expressoitaporanga.com.br")
        print(f"Assunto: Nova mensagem do site - {assunto}")
        print(email_corpo)
        print("=" * 50)
        
        # Retornar sucesso
        return jsonify({
            'success': True, 
            'message': 'Mensagem enviada com sucesso! Entraremos em contato em breve.'
        })
        
    except Exception as e:
        print(f"Erro ao processar contato: {e}")
        return jsonify({
            'success': False, 
            'message': 'Erro ao enviar mensagem. Tente novamente.'
        }), 500

# Rotas do sistema de gestão
@app.route('/gestao')
def gestao_login():
    return render_template('gestao/login.html')

@app.route('/gestao/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    usuario = Usuario.query.filter_by(username=username, ativo=True).first()
    
    if usuario and check_password_hash(usuario.password_hash, password):
        session['user_id'] = usuario.id
        session['username'] = usuario.username
        session['perfil'] = usuario.perfil
        return redirect(url_for('dashboard'))
    else:
        flash('Usuário ou senha inválidos', 'error')
        return redirect(url_for('gestao_login'))

@app.route('/gestao/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/gestao/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('gestao_login'))
    
    # Estatísticas
    total_entregas = Entrega.query.count()
    pendentes = Entrega.query.filter_by(status='pendente').count()
    em_transito = Entrega.query.filter_by(status='em_transito').count()
    entregues = Entrega.query.filter_by(status='entregue').count()
    
    stats = {
        'total': total_entregas,
        'pendentes': pendentes,
        'em_transito': em_transito,
        'entregues': entregues
    }
    
    return render_template('gestao/dashboard.html', stats=stats)

@app.route('/gestao/entregas')
def listar_entregas():
    if 'user_id' not in session:
        return redirect(url_for('gestao_login'))
    
    entregas = Entrega.query.order_by(Entrega.data_criacao.desc()).all()
    return render_template('gestao/entregas.html', entregas=entregas)

@app.route('/gestao/nova-entrega')
def nova_entrega():
    if 'user_id' not in session:
        return redirect(url_for('gestao_login'))
    
    return render_template('gestao/nova_entrega.html')

@app.route('/gestao/criar-entrega', methods=['POST'])
def criar_entrega():
    if 'user_id' not in session:
        return redirect(url_for('gestao_login'))
    
    # Gerar código de rastreamento
    import random
    import string
    codigo = 'EI' + ''.join(random.choices(string.digits, k=8))
    
    entrega = Entrega(
        codigo_rastreamento=codigo,
        remetente_nome=request.form['remetente_nome'],
        remetente_endereco=request.form['remetente_endereco'],
        remetente_cidade=request.form['remetente_cidade'],
        destinatario_nome=request.form['destinatario_nome'],
        destinatario_endereco=request.form['destinatario_endereco'],
        destinatario_cidade=request.form['destinatario_cidade'],
        tipo_produto=request.form['tipo_produto'],
        peso=float(request.form['peso']) if request.form['peso'] else None,
        valor_declarado=float(request.form['valor_declarado']) if request.form['valor_declarado'] else None,
        observacoes=request.form.get('observacoes', ''),
        usuario_id=session['user_id']
    )
    
    db.session.add(entrega)
    db.session.commit()
    
    flash(f'Entrega criada com sucesso! Código: {codigo}', 'success')
    return redirect(url_for('listar_entregas'))

@app.route('/gestao/relatorios')
def relatorios():
    if 'user_id' not in session:
        return redirect(url_for('gestao_login'))
    
    # Dados para relatórios
    total_entregas = Entrega.query.count()
    pendentes = Entrega.query.filter_by(status='pendente').count()
    em_transito = Entrega.query.filter_by(status='em_transito').count()
    entregues = Entrega.query.filter_by(status='entregue').count()
    devolvidas = Entrega.query.filter_by(status='devolvida').count()
    
    # Taxa de sucesso
    taxa_sucesso = (entregues / total_entregas * 100) if total_entregas > 0 else 0
    
    dados = {
        'total': total_entregas,
        'pendentes': pendentes,
        'em_transito': em_transito,
        'entregues': entregues,
        'devolvidas': devolvidas,
        'taxa_sucesso': round(taxa_sucesso, 1)
    }
    
    return render_template('gestao/relatorios.html', dados=dados)

@app.route('/rastreamento')
def rastreamento():
    return render_template('rastreamento.html')

@app.route('/api/rastrear/<codigo>')
def api_rastrear(codigo):
    entrega = Entrega.query.filter_by(codigo_rastreamento=codigo).first()
    if entrega:
        return jsonify({
            'encontrado': True,
            'codigo': entrega.codigo_rastreamento,
            'status': entrega.status,
            'destinatario': entrega.destinatario_nome,
            'cidade_destino': entrega.destinatario_cidade,
            'data_criacao': entrega.data_criacao.strftime('%d/%m/%Y %H:%M')
        })
    else:
        return jsonify({'encontrado': False})

def init_db():
    """Inicializar banco de dados"""
    db.create_all()
    
    # Criar usuário admin se não existir
    admin = Usuario.query.filter_by(username='admin').first()
    if not admin:
        admin = Usuario(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            perfil='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado com sucesso!")

if __name__ == '__main__':
    with app.app_context():
        init_db()
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


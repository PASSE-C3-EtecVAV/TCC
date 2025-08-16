from flask import Blueprint, render_template, request, redirect, session, url_for, flash, current_app, send_from_directory
from app.models.usuario import Usuario
from app import mysql, s3
import MySQLdb.cursors
from datetime import datetime
from werkzeug.security import generate_password_hash
import os
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
from urllib.parse import unquote



bp = Blueprint('auth', __name__)


def apagar_arquivo(url):
    if not url:
        return
    try:
        object_key = url.split(f"{current_app.config['S3_BUCKET_NAME']}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/")[-1]
        
        # Decodifica a chave do objeto para lidar com caracteres especiais no nome do arquivo
        decoded_key = unquote(object_key)

        s3.client.delete_object(
            Bucket=current_app.config['S3_BUCKET_NAME'],
            Key=decoded_key
        )
        print(f"Objeto {decoded_key} deletado do S3 com sucesso.")
    except ClientError as e:
        # Loga o erro se a exclusão falhar, mas não impede a atualização do perfil
        print(f"Erro ao deletar objeto do S3: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao tentar deletar o objeto do S3: {e}")
    

def salvar_arquivo(arquivo, nome_unico):
    try:
        s3.client.upload_fileobj(
            arquivo,
            current_app.config['S3_BUCKET_NAME'],
            nome_unico,
            ExtraArgs={
            'ContentType': arquivo.content_type
            }
        )
        return False, f"https://{current_app.config['S3_BUCKET_NAME']}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{nome_unico}"
    except ClientError as e:
        flash(f'Erro ao fazer upload para o S3 para {arquivo.filename}: {e}', 'danger')
        print(f"Erro S3: {e}")
    except Exception as e:
        flash(f'Erro inesperado ao processar {arquivo.filename}: {e}', 'danger')
        print(f"Erro geral: {e}")
    return False, "Erro"

# Codígo para Login

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        erro = None
        usuario = Usuario.buscar_por_email(email)
        print(f"Email encontrado? {bool(usuario)}")
        
        if usuario and usuario.verificar_senha(senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_tipo'] = usuario.tipo

            # Redireciona com base no tipo de usuário
            if usuario.tipo == 'aluno':
                return redirect(url_for('auth.dashboard_aluno'))
            elif usuario.tipo == 'professor':
                return redirect(url_for('auth.dashboard_professor'))
            elif usuario.tipo == 'coordenacao':
                return redirect(url_for('auth.dashboard_coordenacao'))
            elif usuario.tipo == 'prof_coorde':
                return redirect(url_for('auth.dashboard_prof_coorde'))
        else:
            erro = "Email ou Senha Invalidos."
            return render_template('login.html', erro=erro)
    erro = "Insira um Email e uma Senha."
    return render_template('login.html', erro=erro)

# Codígo para mandar para o Login

@bp.route('/')
def index():
    # Se já estiver logado, redireciona conforme o tipo
    if 'usuario_id' in session:
        tipo = session.get('usuario_tipo')

        if tipo == 'aluno':
            return redirect(url_for('auth.dashboard_aluno'))
        elif tipo == 'professor':
            return redirect(url_for('auth.dashboard_professor'))
        elif tipo == 'coordenacao':
            return redirect(url_for('auth.dashboard_coordenacao'))
        elif tipo == 'prof_coorde':
            return redirect(url_for('auth.dashboard_prof_coorde'))

    # Se não estiver logado, mostra a tela de login
    return render_template('login.html')

# Caminho para cordenação/professor
@bp.route('/coorde_professor')
def dashboard_prof_coorde():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('usuario_tipo') not in 'prof_coorde':
        return redirect(url_for('auth.login'))

    return render_template('coorde_professor.html')

# Caminho para Coordenação

@bp.route('/coordenacao')
def dashboard_coordenacao():
    # Verifica se o usuário está logado
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    # Verifica se é do tipo coordenação
    if session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    # Acesso autorizado
    return render_template('coordenacao.html')

# Caminho para Coordenação - Gerenciar os Funcionários

@bp.route('/geren_funcionarios')
def gerenciar_funcionarios():
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT id, nome, email, tipo FROM usuarios 
        WHERE tipo IN ('professor', 'coordenacao', 'prof_coorde')
        ORDER BY nome
    """)
    funcionarios = cursor.fetchall()
    cursor.close()

    return render_template('geren_funcionarios.html', funcionarios=funcionarios)


# Caminho para Coordenação - Gerenciar Turmas

@bp.route('/geren_turmas')
def gerenciar_turmas():
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nome FROM turmas ORDER BY nome")
    turmas = cursor.fetchall()
    cursor.close()

    return render_template('geren_turmas.html', turmas=turmas)

# Caminho para Logout

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# Caminho para Coordenação - Gerenciar Turmas -  Add Turma

@bp.route('/adicionar_turma', methods=['GET', 'POST'])
def adicionar_turma():
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    erro = None

    if request.method == 'POST':
        nome = request.form['nome'].strip()

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM turmas WHERE nome = %s", (nome,))
        existe = cursor.fetchone()[0]

        if existe:
            erro = f"A turma '{nome}' já existe."
        else:
            cursor.execute("INSERT INTO turmas (nome) VALUES (%s)", (nome,))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('auth.gerenciar_turmas'))

        cursor.close()

    return render_template('adicionar_turma.html', erro=erro)

# Caminho para Coordenação - Gerenciar Turmas - Ver turma

@bp.route('/turma/<int:turma_id>', methods=['GET', 'POST'])
def ver_turma(turma_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    # Pega o nome da turma
    cursor.execute("SELECT nome FROM turmas WHERE id = %s", (turma_id,))
    turma = cursor.fetchone()
    if not turma:
        cursor.close()
        return "Turma não encontrada", 404
    nome_turma = turma[0]

    if request.method == 'POST':
        acao = request.form.get('acao')

        # Adicionar disciplina
        if acao == 'adicionar_disciplina':
            nome_disciplina = request.form['nova_disciplina'].strip()

            if nome_disciplina:
                # Verifica se já existe a disciplina
                cursor.execute("SELECT id FROM disciplinas WHERE nome = %s", (nome_disciplina,))
                row = cursor.fetchone()
                if row:
                    disciplina_id = row[0]
                else:
                    # Cria nova disciplina
                    cursor.execute("INSERT INTO disciplinas (nome) VALUES (%s)", (nome_disciplina,))
                    disciplina_id = cursor.lastrowid

                # Verifica se já está vinculada
                cursor.execute("SELECT 1 FROM turmas_disciplinas WHERE turma_id = %s AND disciplina_id = %s", (turma_id, disciplina_id))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO turmas_disciplinas (turma_id, disciplina_id) VALUES (%s, %s)", (turma_id, disciplina_id))

                mysql.connection.commit()

        # Remover disciplina
        elif acao == 'remover_disciplina':
            disciplina_id = request.form['disciplina_id']

            cursor.execute("DELETE FROM usuarios_disciplinas WHERE disciplina_id = %s", (disciplina_id,))
            cursor.execute("DELETE FROM turmas_disciplinas WHERE turma_id = %s AND disciplina_id = %s", (turma_id, disciplina_id))
            cursor.execute("DELETE FROM disciplinas WHERE id = %s", (disciplina_id,))
            mysql.connection.commit()

        # Transferência de todos os alunos
        elif acao == 'transferir_alunos':
            nova_turma_id = request.form.get('nova_turma_id')
            if nova_turma_id:
                cursor.execute("""
                    UPDATE usuarios_turmas
                    SET turma_id = %s
                    WHERE turma_id = %s
                """, (nova_turma_id, turma_id))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('auth.ver_turma', turma_id=nova_turma_id))

        return redirect(url_for('auth.ver_turma', turma_id=turma_id))

    # Alunos da turma
    cursor.execute("""
        SELECT u.id, u.nome, u.email
        FROM usuarios u
        JOIN usuarios_turmas ut ON u.id = ut.aluno_id
        WHERE ut.turma_id = %s
    """, (turma_id,))
    alunos = cursor.fetchall()

    # Outras turmas (para transferência)
    cursor.execute("SELECT id, nome FROM turmas WHERE id != %s", (turma_id,))
    outras_turmas = cursor.fetchall()

    # Disciplinas da turma
    cursor.execute("""
        SELECT d.id, d.nome
        FROM disciplinas d
        JOIN turmas_disciplinas td ON td.disciplina_id = d.id
        WHERE td.turma_id = %s
    """, (turma_id,))
    disciplinas = cursor.fetchall()

    cursor.close()
    return render_template(
        'ver_turma.html',
        turma_id=turma_id,
        nome_turma=nome_turma,
        alunos=alunos,
        outras_turmas=outras_turmas,
        disciplinas=disciplinas
    )



@bp.route('/excluir_turma/<int:turma_id>', methods=['POST'])
def excluir_turma(turma_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    # Verifica se tem alunos vinculados
    cursor.execute("SELECT COUNT(*) FROM usuarios_turmas WHERE turma_id = %s", (turma_id,))
    total = cursor.fetchone()[0]

    if total > 0:
        cursor.close()
        return "Erro: A turma possui alunos e não pode ser excluída.", 400

    # Exclui a turma
    cursor.execute("DELETE FROM turmas WHERE id = %s", (turma_id,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('auth.gerenciar_turmas'))



# Caminho para Coordenação - Gerenciar Turmas - Ver turma - Editar Aluno

@bp.route('/editar_aluno/<int:aluno_id>', methods=['GET', 'POST'])
def editar_aluno(aluno_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    # Busca aluno
    cursor.execute("SELECT id, nome, email FROM usuarios WHERE id = %s AND tipo = 'aluno'", (aluno_id,))
    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        return "Aluno não encontrado", 404

    aluno = {
        "id": dados[0],
        "nome": dados[1],
        "email": dados[2]
    }

    # Busca turma atual do aluno
    cursor.execute("SELECT turma_id FROM usuarios_turmas WHERE aluno_id = %s", (aluno_id,))
    turma = cursor.fetchone()
    turma_id = turma[0] if turma else None

    # Busca todas as turmas
    cursor.execute("SELECT id, nome FROM turmas ORDER BY nome")
    turmas = cursor.fetchall()

    erro = None
    sucesso = None

    if request.method == 'POST':
        acao = request.form.get('acao')

        if acao == 'salvar':
            novo_nome = request.form['nome'].strip()
            nova_turma_id = request.form['turma_id']

            cursor.execute("UPDATE usuarios SET nome = %s WHERE id = %s", (novo_nome, aluno_id))

            # Atualiza turma
            cursor.execute("""
                UPDATE usuarios_turmas SET turma_id = %s WHERE aluno_id = %s
            """, (nova_turma_id, aluno_id))

            mysql.connection.commit()
            sucesso = "Dados atualizados com sucesso."
            aluno['nome'] = novo_nome
            turma_id = int(nova_turma_id)

        elif acao == 'redefinir':
            nova_senha = generate_password_hash('mudar123')
            cursor.execute("UPDATE usuarios SET senha = %s WHERE id = %s", (nova_senha, aluno_id))
            mysql.connection.commit()
            sucesso = "Senha redefinida para 'mudar123'."

    cursor.close()
    return render_template('editar_aluno.html', aluno=aluno, turma_id=turma_id, turmas=turmas, erro=erro, sucesso=sucesso)


@bp.route('/excluir_aluno/<int:aluno_id>', methods=['POST'])
def excluir_aluno(aluno_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    # Descobre a turma antes de excluir
    cursor.execute("SELECT turma_id FROM usuarios_turmas WHERE aluno_id = %s", (aluno_id,))
    turma = cursor.fetchone()
    turma_id = turma[0] if turma else None

    # Exclui o vínculo com a turma
    cursor.execute("DELETE FROM usuarios_turmas WHERE aluno_id = %s", (aluno_id,))
    # Exclui o usuário
    cursor.execute("DELETE FROM usuarios WHERE id = %s AND tipo = 'aluno'", (aluno_id,))
    mysql.connection.commit()
    cursor.close()

    flash("Aluno excluído com sucesso.", "success")

    # Redireciona para a página da turma
    if turma_id:
        return redirect(url_for('auth.ver_turma', turma_id=turma_id))
    else:
        return redirect(url_for('auth.dashboard_coordenacao'))  # rota alternativa, se necessário



# Caminho para Coordenação - Gerenciar Turmas - Ver turma - Add Aluno

@bp.route('/adicionar_aluno/<int:turma_id>', methods=['GET', 'POST'])
def adicionar_aluno(turma_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    erro = None

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nome FROM turmas WHERE id = %s", (turma_id,))
    turma = cursor.fetchone()
    if not turma:
        cursor.close()
        return "Turma não encontrada", 404
    nome_turma = turma[0]

    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        senha = generate_password_hash('mudar123')

        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            erro = "Este e-mail já está cadastrado."
        else:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, 'aluno')",
                (nome, email, senha)
            )
            aluno_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO usuarios_turmas (aluno_id, turma_id) VALUES (%s, %s)",
                (aluno_id, turma_id)
            )
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('auth.ver_turma', turma_id=turma_id))

    cursor.close()
    return render_template('adicionar_aluno.html', turma_id=turma_id, nome_turma=nome_turma, erro=erro)


# Caminho para Coordenação - Gerenciar Funcionarios - Editar Funcionário

@bp.route('/editar_funcionario/<int:funcionario_id>', methods=['GET', 'POST'])
def editar_funcionario(funcionario_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde', 'professor']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()
    next_page = request.args.get('next')
    # Buscar dados do funcionário
    cursor.execute("SELECT id, nome, email, tipo FROM usuarios WHERE id = %s AND tipo IN ('professor', 'coordenacao', 'prof_coorde')", (funcionario_id,))
    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        return "Funcionário não encontrado", 404

    funcionario = {
        'id': dados[0],
        'nome': dados[1],
        'email': dados[2],
        'tipo': dados[3]
    }

    erro = None
    sucesso = None

    if request.method == 'POST':
        acao = request.form.get('acao')

        if acao == 'salvar':
            nome = request.form['nome'].strip()
            tipo = request.form['tipo']
            if tipo not in ['professor', 'coordenacao', 'prof_coorde']:
                erro = "Tipo inválido."
            else:
                cursor.execute("UPDATE usuarios SET nome = %s, tipo = %s WHERE id = %s", (nome, tipo, funcionario_id))
                mysql.connection.commit()
                funcionario['nome'] = nome
                funcionario['tipo'] = tipo
                sucesso = "Dados atualizados com sucesso."

        elif acao == 'redefinir':
            nova_senha = generate_password_hash("funcionario123")
            cursor.execute("UPDATE usuarios SET senha = %s WHERE id = %s", (nova_senha, funcionario_id))
            mysql.connection.commit()
            sucesso = "Senha redefinida com sucesso para 'funcionario123'."
        elif acao == 'trocar_senha':
            if funcionario_id == session['usuario_id']:
                nova_senha = request.form['nova_senha'].strip()
                if nova_senha:
                    senha_hash = generate_password_hash(nova_senha)
                    cursor.execute("UPDATE usuarios SET senha = %s WHERE id = %s", (senha_hash, funcionario_id))
                    mysql.connection.commit()
                    sucesso = "Senha atualizada com sucesso."
                else:
                    erro = "A nova senha não pode estar vazia."
            else:
                erro = "Você só pode alterar sua própria senha."

    cursor.close()
    return render_template('editar_funcionario.html', funcionario=funcionario, erro=erro, sucesso=sucesso, next_page=next_page)


@bp.route('/excluir_funcionario/<int:funcionario_id>', methods=['POST'])
def excluir_funcionario(funcionario_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    if funcionario_id == session['usuario_id']:
        flash("Você não pode excluir a si mesmo.", "danger")
        return redirect(url_for('auth.editar_funcionario', funcionario_id=funcionario_id))

    cursor = mysql.connection.cursor()

    # Remove vínculos com disciplinas e turmas
    cursor.execute("DELETE FROM usuarios_disciplinas WHERE professor_id = %s", (funcionario_id,))
    
    # Remove o próprio usuário
    cursor.execute("DELETE FROM usuarios WHERE id = %s AND tipo IN ('professor', 'coordenacao', 'prof_coorde')", (funcionario_id,))

    mysql.connection.commit()
    cursor.close()

    flash("Funcionário excluído com sucesso.", "success")
    return redirect(url_for('auth.gerenciar_funcionarios'))


@bp.route('/vincular_prof_disciplinas/<int:funcionario_id>', methods=['GET', 'POST'])
def vincular_prof_disciplinas(funcionario_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    # Buscar funcionário
    cursor.execute("SELECT id, nome FROM usuarios WHERE id = %s AND tipo IN ('professor', 'prof_coorde')", (funcionario_id,))
    funcionario = cursor.fetchone()
    if not funcionario:
        cursor.close()
        return "Funcionário não encontrado", 404

    # Buscar turmas e disciplinas
    cursor.execute("SELECT id, nome FROM turmas ORDER BY nome")
    turmas = cursor.fetchall()

    # Buscar vínculos atuais
    cursor.execute("""
    SELECT t.nome AS turma_nome, d.nome AS disciplina_nome, t.id AS turma_id, d.id AS disciplina_id
    FROM usuarios_disciplinas ud
    JOIN turmas t ON ud.turma_id = t.id
    JOIN disciplinas d ON ud.disciplina_id = d.id
    WHERE ud.professor_id = %s
    ORDER BY t.nome, d.nome
    """, (funcionario_id,))
    vinculos = cursor.fetchall()


    if request.method == 'POST':
        turma_id = request.form.get('turma_id')
        disciplina_id = request.form.get('disciplina_id')
        acao = request.form.get('acao')

        if acao == 'adicionar' and turma_id and disciplina_id:
            cursor.execute("""
                INSERT INTO usuarios_disciplinas (professor_id, turma_id, disciplina_id)
                SELECT %s, %s, %s FROM dual
                WHERE NOT EXISTS (
                    SELECT 1 FROM usuarios_disciplinas 
                    WHERE professor_id = %s AND turma_id = %s AND disciplina_id = %s
                )
            """, (funcionario_id, turma_id, disciplina_id, funcionario_id, turma_id, disciplina_id))
            mysql.connection.commit()

        elif acao == 'remover':
            cursor.execute("""
                DELETE FROM usuarios_disciplinas
                WHERE professor_id = %s AND turma_id = %s AND disciplina_id = %s
            """, (funcionario_id, turma_id, disciplina_id))
            mysql.connection.commit()

        return redirect(url_for('auth.vincular_prof_disciplinas', funcionario_id=funcionario_id))

    cursor.close()
    return render_template(
        'vincular_prof_disciplinas.html',
        funcionario={"id": funcionario[0], "nome": funcionario[1]},
        turmas=turmas,
        vinculos=vinculos
    )

@bp.route('/api/disciplinas_da_turma/<int:turma_id>')
def api_disciplinas_da_turma(turma_id):
    if 'usuario_id' not in session:
        return {"erro": "Não autorizado"}, 401

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT d.id, d.nome
        FROM disciplinas d
        JOIN turmas_disciplinas td ON td.disciplina_id = d.id
        WHERE td.turma_id = %s
    """, (turma_id,))
    disciplinas = cursor.fetchall()
    cursor.close()

    return [{"id": d[0], "nome": d[1]} for d in disciplinas]

# Caminho para Coordenação - Gerenciar Funcionarios - Add Funcionário

@bp.route('/adicionar_funcionario', methods=['GET', 'POST'])
def adicionar_funcionario():
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['coordenacao', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    erro = None

    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        tipo = request.form['tipo']

        if not nome or not email or tipo not in ['professor', 'coordenacao', 'prof_coorde']:
            erro = "Preencha todos os campos corretamente."
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                erro = "Este e-mail já está cadastrado."
            else:
                senha_hash = generate_password_hash("funcionario123")
                cursor.execute(
                    "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, %s)",
                    (nome, email, senha_hash, tipo)
                )
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('auth.gerenciar_funcionarios'))

            cursor.close()

    return render_template('adicionar_funcionario.html', erro=erro)


#consertafelix: tudo abaixo


@bp.route('/professor')
def dashboard_professor():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    return render_template('professor.html')

@bp.route('/turmas')
def turmas():
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    usuario_id = session['usuario_id']
    cursor = mysql.connection.cursor()

    # Buscar turmas vinculadas ao professor logado
    cursor.execute("""
        SELECT DISTINCT t.id, t.nome
        FROM turmas t
        JOIN usuarios_disciplinas ud ON t.id = ud.turma_id
        WHERE ud.professor_id = %s
        ORDER BY t.nome
    """, (usuario_id,))
    turmas = cursor.fetchall()
    cursor.close()
    
    return render_template('turmas.html', turmas=turmas)


@bp.route('/postagens_prof/<int:turma_id>/<int:disciplina_id>')
def postagens_prof(turma_id, disciplina_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    # Exemplo fictício de busca de postagens (substitua com sua lógica real)
    cursor = mysql.connection.cursor()
    cursor.execute("""
    SELECT id, titulo, conteudo, data, arquivo FROM postagens
    WHERE turma_id = %s AND disciplina_id = %s
    ORDER BY data DESC
""", (turma_id, disciplina_id))
    postagens = cursor.fetchall()
    # Buscar nome da disciplina
    cursor.execute("SELECT nome FROM disciplinas WHERE id = %s", (disciplina_id,))
    disciplina = cursor.fetchone()
    nome_disciplina = disciplina[0] if disciplina else "Desconhecida"

    cursor.close()

    return render_template(
        'postagens_prof.html',
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina,
        postagens=postagens
    )

@bp.route('/atividades_prof')
def atividades_prof():
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))
    
    return render_template('atividades_prof.html')


@bp.route('/materias_prof/<int:turma_id>', endpoint='materias_prof')
def materias_prof(turma_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    professor_id = session['usuario_id']
    cursor = mysql.connection.cursor()

    # Verifica se o professor está vinculado à turma
    cursor.execute("""
        SELECT DISTINCT d.id, d.nome
        FROM disciplinas d
        INNER JOIN usuarios_disciplinas ud ON ud.disciplina_id = d.id
        WHERE ud.turma_id = %s AND ud.professor_id = %s
    """, (turma_id, professor_id))
    
    disciplinas = cursor.fetchall()

    # Nome da turma
    cursor.execute("SELECT nome FROM turmas WHERE id = %s", (turma_id,))
    turma = cursor.fetchone()

    cursor.close()

    if not turma:
        return "Turma não encontrada", 404

    return render_template('materias_prof.html', disciplinas=disciplinas, turma_nome=turma[0], turma_id=turma_id)

@bp.route('/adicionar_post/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>', methods=['GET', 'POST'])
def adicionar_post(turma_id, disciplina_id, nome_disciplina):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    erro = None

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        conteudo = request.form.get('conteudo')
        arquivo = request.files.get('arquivo')
        nome_arquivo = None

        if not titulo or not conteudo:
            erro = "Preencha todos os campos."
        else:
            if arquivo and arquivo.filename:
                nome_original = secure_filename(arquivo.filename.rsplit('.', 1)[0])
                extensao = arquivo.filename.rsplit('.', 1)[-1]
                data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                nome_disciplina_seguro = secure_filename(nome_disciplina)

                nome_formatado = f"{nome_original}_{nome_disciplina_seguro}_{data_atual}.{extensao}"
                nome_arquivo = salvar_arquivo(arquivo, nome_formatado)[1]
                
                

            cursor = mysql.connection.cursor()
            professor_id = session['usuario_id']
            cursor.execute("""
                INSERT INTO postagens (titulo, conteudo, data, turma_id, disciplina_id, professor_id, arquivo)
                VALUES (%s, %s, NOW(), %s, %s, %s, %s)
            """, (titulo, conteudo, turma_id, disciplina_id, professor_id, nome_arquivo))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('auth.postagens_prof', turma_id=turma_id, disciplina_id=disciplina_id, nome_disciplina=nome_disciplina))

    return render_template('adicionar_post.html', turma_id=turma_id, disciplina_id=disciplina_id, nome_disciplina=nome_disciplina, erro=erro)

@bp.route('/excluir_post/<int:post_id>', methods=['POST'])
def excluir_post(post_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor()

    # Buscar nome do arquivo e ids da turma e disciplina
    cursor.execute("""
        SELECT arquivo, turma_id, disciplina_id
        FROM postagens
        WHERE id = %s
    """, (post_id,))
    dados = cursor.fetchone()

    if not dados:
        cursor.close()
        return "Postagem não encontrada", 404

    arquivo, turma_id, disciplina_id = dados

    # Excluir do banco
    cursor.execute("DELETE FROM postagens WHERE id = %s", (post_id,))
    mysql.connection.commit()
    cursor.close()

    # Remover arquivo se existir
    if arquivo:
        apagar_arquivo(arquivo)

    return redirect(url_for('auth.postagens_prof', turma_id=turma_id, disciplina_id=disciplina_id))



@bp.route('/adicionar_atividade/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>', methods=['GET', 'POST'])
def adicionar_atividade(turma_id, disciplina_id, nome_disciplina):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    erro = None

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        data_atraso = request.form.get('data_atraso')
        data_encerramento = request.form.get('data_encerramento')
        arquivo = request.files.get('arquivo')
        nome_arquivo = None

        if not titulo or not descricao or not data_atraso or not data_encerramento:
            erro = "Preencha todos os campos obrigatórios."
        else:
            if arquivo and arquivo.filename:
                nome_original = secure_filename(arquivo.filename.rsplit('.', 1)[0])
                extensao = arquivo.filename.rsplit('.', 1)[-1]
                data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                nome_disciplina_seguro = secure_filename(nome_disciplina)

                nome_formatado = f"{nome_original}_{nome_disciplina_seguro}_{data_atual}.{extensao}"
                nome_arquivo = salvar_arquivo(arquivo, nome_formatado)[1]
                print(nome_arquivo)
            professor_id = session['usuario_id']

            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO atividades 
                (professor_id, disciplina_id, turma_id, titulo, descricao, arquivo, data_criacao, data_atraso, data_encerramento)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s)
            """, (professor_id, disciplina_id, turma_id, titulo, descricao, nome_arquivo, data_atraso, data_encerramento))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('auth.atividade_prof', turma_id=turma_id, disciplina_id=disciplina_id, nome_disciplina=nome_disciplina))

    return render_template('adicionar_atividade.html', turma_id=turma_id, disciplina_id=disciplina_id, erro=erro, nome_disciplina=nome_disciplina)



@bp.route('/aluno')
def dashboard_aluno():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('usuario_tipo') not in 'aluno':
        return redirect(url_for('auth.login'))

    return render_template('aluno.html')


@bp.route('/atividade_prof/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>')
def atividade_prof(turma_id, disciplina_id, nome_disciplina):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT id, titulo, descricao, arquivo, data_criacao, data_atraso, data_encerramento 
        FROM atividades
        WHERE turma_id = %s AND disciplina_id = %s
        ORDER BY data_criacao DESC
    """, (turma_id, disciplina_id))
    atividades = cursor.fetchall()
    cursor.close()

    return render_template(
        'atividade_prof.html',
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina,
        atividades=atividades
    )

@bp.route('/excluir_atividade/<int:atividade_id>', methods=['POST'])
def excluir_atividade(atividade_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Buscar atividade e arquivo
    cursor.execute("SELECT arquivo FROM atividades WHERE id = %s", (atividade_id,))
    atividade = cursor.fetchone()

    if atividade:
        arquivo = atividade['arquivo']

        # Apagar atividade do banco
        cursor.execute("DELETE FROM atividades WHERE id = %s", (atividade_id,))
        mysql.connection.commit()
        cursor.close()

        # Se existe arquivo, remover da pasta uploads
        if arquivo:
            apagar_arquivo(arquivo)

        flash("Atividade excluída com sucesso!", "success")
    else:
        flash("Atividade não encontrada.", "danger")
        cursor.close()

    # Redirecionar para a página anterior
    return redirect(request.referrer or url_for('auth.dashboard'))


@bp.route('/arquivos_prof/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>')
def arquivos_prof(turma_id, disciplina_id, nome_disciplina):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT id, nome_original, nome_arquivo, data_upload, professor_id
        FROM arquivos
        WHERE turma_id = %s AND disciplina_id = %s
        ORDER BY data_upload DESC
    """, (turma_id, disciplina_id))
    arquivos = cursor.fetchall()
    cursor.close()

    return render_template(
        'arquivos_prof.html',
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina,
        arquivos=arquivos
    )




@bp.route('/upload_arquivo/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>', methods=['POST'])
def upload_arquivo(turma_id, disciplina_id, nome_disciplina):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    arquivo = request.files.get('file')
    if not arquivo or arquivo.filename == '':
        flash("Nenhum arquivo selecionado.", "danger")
        return redirect(request.referrer)

    # Extrair informações
    nome_original = secure_filename(arquivo.filename.rsplit('.', 1)[0])
    extensao = arquivo.filename.rsplit('.', 1)[-1]
    data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_disciplina_seguro = secure_filename(nome_disciplina)

    # Nome final
    nome_arquivo = f"{nome_original}_{nome_disciplina_seguro}_{data_atual}.{extensao}"
    nome_arquivo = salvar_arquivo(arquivo, nome_arquivo)[1]
    # Inserir no banco
    professor_id = session['usuario_id']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO arquivos (professor_id, turma_id, disciplina_id, nome_original, nome_arquivo)
        VALUES (%s, %s, %s, %s, %s)
    """, (professor_id, turma_id, disciplina_id, arquivo.filename, nome_arquivo))
    mysql.connection.commit()
    cursor.close()

    flash("Arquivo enviado com sucesso!", "success")
    return redirect(request.referrer)

@bp.route('/excluir_arquivo/<int:arquivo_id>', methods=['POST'])
def excluir_arquivo(arquivo_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT nome_arquivo, turma_id, disciplina_id, nome_original
        FROM arquivos
        WHERE id = %s
    """, (arquivo_id,))
    arquivo = cursor.fetchone()

    if not arquivo:
        flash("Arquivo não encontrado.", "danger")
        cursor.close()
        return redirect(request.referrer)

    # Excluir do banco
    cursor.execute("DELETE FROM arquivos WHERE id = %s", (arquivo_id,))
    mysql.connection.commit()
    cursor.close()

    # Excluir do sistema de arquivos
    apagar_arquivo(arquivo['nome_arquivo'])

    flash(f"Arquivo '{arquivo['nome_original']}' excluído com sucesso!", "success")

    return redirect(url_for(
        'auth.arquivos_prof',
        turma_id=arquivo['turma_id'],
        disciplina_id=arquivo['disciplina_id'],
        nome_disciplina=os.path.splitext(arquivo['nome_arquivo'])[0].split('_')[1]  # extrai nome da disciplina do nome do arquivo
    ))


@bp.route('/materias')
def materias():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('usuario_tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    aluno_id = session['usuario_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
        SELECT DISTINCT d.id AS disciplina_id, d.nome AS disciplina_nome, t.id AS turma_id, t.nome AS turma_nome
        FROM usuarios_turmas ut
        INNER JOIN turmas t ON ut.turma_id = t.id
        INNER JOIN turmas_disciplinas td ON td.turma_id = t.id
        INNER JOIN disciplinas d ON td.disciplina_id = d.id
        WHERE ut.aluno_id = %s
        ORDER BY t.nome, d.nome
    """, (aluno_id,))
    
    materias = cursor.fetchall()
    cursor.close()

    return render_template('materias.html', materias=materias)


@bp.route('/postagens/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>')
def postagens(turma_id, disciplina_id, nome_disciplina):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('usuario_tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
            SELECT p.titulo, p.conteudo, p.data, p.arquivo, u.nome AS professor_nome
            FROM postagens p
            INNER JOIN usuarios u ON p.professor_id = u.id
            WHERE p.turma_id = %s AND p.disciplina_id = %s
            ORDER BY p.data DESC
        """, (turma_id, disciplina_id))
    
    postagens = cursor.fetchall()
    cursor.close()

    return render_template(
        'postagens.html',
        postagens=postagens,
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina
    )



@bp.route('/atividades/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>')
def atividades(turma_id, disciplina_id, nome_disciplina):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session.get('usuario_tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT a.id, a.titulo, a.descricao, a.data_criacao, a.data_atraso, 
               a.data_encerramento, a.arquivo
        FROM atividades a
        WHERE a.turma_id = %s AND a.disciplina_id = %s
        ORDER BY a.data_criacao DESC
    """, (turma_id, disciplina_id))
    
    atividades = cursor.fetchall()
    cursor.close()

    return render_template(
        'atividades.html',
        atividades=atividades,
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina
    )



@bp.route('/arquivos/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>')
def arquivos(turma_id, disciplina_id, nome_disciplina):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    if session.get('usuario_tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT id, nome_original, nome_arquivo, data_upload
        FROM arquivos
        WHERE turma_id = %s AND disciplina_id = %s
        ORDER BY data_upload DESC
    """, (turma_id, disciplina_id))
    
    arquivos = cursor.fetchall()
    cursor.close()

    return render_template(
        'arquivos.html',
        arquivos=arquivos,
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina
    )


@bp.route('/todas_atividades/<int:turma_id>/<string:nome_turma>')
def todas_atividades(turma_id, nome_turma):
    if 'usuario_id' not in session or session.get('usuario_tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    aluno_id = session['usuario_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Buscar atividades de TODAS as disciplinas da turma
    cursor.execute("""
        SELECT a.id, a.titulo, a.descricao, a.data_criacao, a.data_atraso, a.data_encerramento,
            a.disciplina_id,
            d.nome AS disciplina_nome, 
            e.id AS entrega_id
        FROM atividades a
        INNER JOIN disciplinas d ON a.disciplina_id = d.id
        LEFT JOIN entregas e ON e.atividade_id = a.id AND e.aluno_id = %s
        WHERE a.turma_id = %s
        ORDER BY a.data_criacao DESC
    """, (aluno_id, turma_id))


    atividades = cursor.fetchall()
    cursor.close()

    disponiveis, atrasadas, concluidas = [], [], []
    agora = datetime.now()

    for atividade in atividades:
        if atividade['entrega_id']:  # Já entregue
            concluidas.append(atividade)
        elif agora > atividade['data_atraso'] and agora <= atividade['data_encerramento']:
            atrasadas.append(atividade)
        elif agora <= atividade['data_encerramento']:
            disponiveis.append(atividade)

    return render_template(
        'todas_atividades.html',
        disponiveis=disponiveis,
        atrasadas=atrasadas,
        concluidas=concluidas,
        turma_id=turma_id,
        nome_turma=nome_turma
    )



@bp.route('/entrega_atividade/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>/<int:atividade_id>', methods=['GET', 'POST'])
def entrega_atividade(turma_id, disciplina_id, nome_disciplina, atividade_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    aluno_id = session['usuario_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Buscar dados da atividade
    cursor.execute("""
        SELECT id, titulo, descricao, arquivo, data_atraso, data_encerramento
        FROM atividades
        WHERE id = %s
    """, (atividade_id,))
    atividade = cursor.fetchone()

    if not atividade:
        flash("Atividade não encontrada.", "danger")
        cursor.close()
        return redirect(url_for('auth.atividades', turma_id=turma_id, disciplina_id=disciplina_id, nome_disciplina=nome_disciplina))

    # Verificar se o aluno já entregou a atividade
    cursor.execute("""
        SELECT id, arquivo, nome_arquivo, texto, data_entrega, anotacao
        FROM entregas
        WHERE atividade_id = %s AND aluno_id = %s
    """, (atividade_id, aluno_id))
    entrega = cursor.fetchone()

    cache_texto = ""
    cache_arquivo = None

    if request.method == 'POST':
        if 'desfazer' in request.form and entrega:
            # Guardar dados antes de excluir
            cache_texto = entrega['texto']
            cache_arquivo = entrega['arquivo']

            # Excluir arquivo físico
            if entrega['nome_arquivo']:
                apagar_arquivo(entrega['nome_arquivo'])

            # Excluir do banco
            cursor.execute("DELETE FROM entregas WHERE id = %s", (entrega['id'],))
            mysql.connection.commit()
            flash("Entrega desfeita. Você pode editar e reenviar.", "info")
            entrega = None  # Remover para o template não desabilitar campos

        else:
            texto = request.form.get('texto')
            arquivo = request.files.get('arquivo')
            nome_arquivo_salvo = None
            nome_arquivo_original = None

            if arquivo and arquivo.filename:
                nome_arquivo_original = secure_filename(arquivo.filename)
                extensao = arquivo.filename.rsplit('.', 1)[-1]
                nome_arquivo_salvo = f"{atividade_id}_{aluno_id}.{extensao}"
                nome_arquivo_salvo = salvar_arquivo(arquivo,  nome_arquivo_salvo)[1]

            cursor.execute("""
                INSERT INTO entregas (atividade_id, aluno_id, arquivo, nome_arquivo, texto, data_entrega)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (atividade_id, aluno_id, nome_arquivo_original, nome_arquivo_salvo, texto))
            mysql.connection.commit()
            flash("Atividade entregue com sucesso.", "success")

            # Buscar entrega novamente para exibir botão "Desfazer"
            cursor.execute("""
            SELECT id, arquivo, nome_arquivo, texto, data_entrega, anotacao
            FROM entregas
            WHERE atividade_id = %s AND aluno_id = %s
        """, (atividade_id, aluno_id))
        entrega = cursor.fetchone()

    cursor.close()
    hoje = datetime.now()
    com_atraso = hoje > atividade['data_atraso']
    atividade_fechada = hoje > atividade['data_encerramento']

    return render_template(
        'entrega_atividade.html',
        atividade=atividade,
        entrega=entrega,
        com_atraso=com_atraso,
        atividade_fechada=atividade_fechada,
        cache_texto=cache_texto,
        cache_arquivo=cache_arquivo,
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina
    )


@bp.route('/download_entrega/<int:entrega_id>')
def download_entrega(entrega_id):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    aluno_id = session['usuario_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT nome_arquivo, arquivo
        FROM entregas
        WHERE id = %s AND aluno_id = %s
    """, (entrega_id, aluno_id))
    entrega = cursor.fetchone()
    cursor.close()

    if not entrega:
        flash("Entrega não encontrada.", "danger")
        return redirect(request.referrer)

    caminho_uploads = os.path.join(current_app.static_folder, 'uploads')
    return send_from_directory(
        caminho_uploads,
        entrega['nome_arquivo'],
        as_attachment=True,
        download_name=entrega['arquivo']  # Nome original
    )

@bp.route('/redirecionar_todas_atividades')
def redirecionar_todas_atividades():
    if 'usuario_id' not in session or session.get('usuario_tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    aluno_id = session['usuario_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Descobre a turma do aluno
    cursor.execute("""
        SELECT t.id AS turma_id, t.nome AS turma_nome
        FROM usuarios_turmas ut
        INNER JOIN turmas t ON ut.turma_id = t.id
        WHERE ut.aluno_id = %s
        LIMIT 1
    """, (aluno_id,))
    
    turma = cursor.fetchone()
    cursor.close()

    if not turma:
        flash("Você não está vinculado a nenhuma turma.", "warning")
        return redirect(url_for('auth.dashboard_aluno'))

    return redirect(url_for('auth.todas_atividades', turma_id=turma['turma_id'], nome_turma=turma['turma_nome']))

@bp.route('/ver_quem_entregou/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>/<int:atividade_id>')
def ver_quem_entregou(turma_id, disciplina_id, nome_disciplina, atividade_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Buscar todos os alunos da turma
    cursor.execute("""
        SELECT u.id AS aluno_id, u.nome AS aluno_nome, e.id AS entrega_id
        FROM usuarios u
        INNER JOIN usuarios_turmas ut ON ut.aluno_id = u.id
        LEFT JOIN entregas e ON e.aluno_id = u.id AND e.atividade_id = %s
        WHERE ut.turma_id = %s AND u.tipo = 'aluno'
        ORDER BY u.nome
    """, (atividade_id, turma_id))
    
    alunos = cursor.fetchall()
    cursor.close()

    return render_template(
        'ver_quem_entregou.html',
        alunos=alunos,
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina,
        atividade_id=atividade_id
    )

@bp.route('/ver_entrega_individual/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>/<int:atividade_id>/<int:aluno_id>', methods=['GET', 'POST'])
def ver_entrega_individual(turma_id, disciplina_id, nome_disciplina, atividade_id, aluno_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Buscar dados da atividade
    cursor.execute("""
        SELECT id, titulo, descricao, arquivo, data_atraso, data_encerramento
        FROM atividades
        WHERE id = %s
    """, (atividade_id,))
    atividade = cursor.fetchone()

    # Buscar entrega do aluno
    cursor.execute("""
        SELECT id, texto, arquivo, nome_arquivo, data_entrega, anotacao
        FROM entregas
        WHERE atividade_id = %s AND aluno_id = %s
    """, (atividade_id, aluno_id))
    entrega = cursor.fetchone()

    if request.method == 'POST' and entrega:
        anotacao = request.form.get('anotacao')
        cursor.execute("""
            UPDATE entregas SET anotacao = %s WHERE id = %s
        """, (anotacao, entrega['id']))
        mysql.connection.commit()
        cursor.close()
        
        flash("Anotação salva com sucesso!", "success")
        
        # Redireciona para ver todas as entregas dessa atividade
        return redirect(url_for('auth.ver_quem_entregou',
                                turma_id=turma_id,
                                disciplina_id=disciplina_id,
                                nome_disciplina=nome_disciplina,
                                atividade_id=atividade_id))

    cursor.close()

    return render_template(
        'ver_entrega_individual.html',
        atividade=atividade,
        entrega=entrega,
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina
    )

@bp.route('/editar_tarefa/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>/<int:atividade_id>', methods=['GET', 'POST'])
def editar_tarefa(turma_id, disciplina_id, nome_disciplina, atividade_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Buscar dados da atividade
    cursor.execute("""
        SELECT id, titulo, descricao, arquivo, data_atraso, data_encerramento
        FROM atividades
        WHERE id = %s
    """, (atividade_id,))
    atividade = cursor.fetchone()

    if not atividade:
        flash("Atividade não encontrada.", "danger")
        cursor.close()
        return redirect(url_for('auth.atividade_prof',
                                turma_id=turma_id,
                                disciplina_id=disciplina_id,
                                nome_disciplina=nome_disciplina))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        data_atraso = request.form.get('data_atraso')
        data_encerramento = request.form.get('data_encerramento')
        arquivo = request.files.get('arquivo')

        nome_arquivo = atividade['arquivo']  # Mantém o atual se não trocar

        # Se enviou novo arquivo, substitui
        if arquivo and arquivo.filename:
            nome_original = secure_filename(arquivo.filename.rsplit('.', 1)[0])
            extensao = arquivo.filename.rsplit('.', 1)[-1]
            data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Novo padrão de nome
            nome_arquivo = f"{nome_original}_{nome_disciplina}_{data_atual}.{extensao}"

            # Exclui arquivo anterior se existir
            if atividade['arquivo']:
                apagar_arquivo(atividade['arquivo'])
            salvar_arquivo(arquivo, nome_arquivo)[1]
            nome_arquivo = salvar_arquivo


        cursor.execute("""
            UPDATE atividades
            SET titulo = %s, descricao = %s, arquivo = %s, 
                data_atraso = %s, data_encerramento = %s
            WHERE id = %s
        """, (titulo, descricao, nome_arquivo,
              data_atraso, data_encerramento, atividade_id))
        mysql.connection.commit()
        cursor.close()

        flash("Atividade atualizada com sucesso!", "success")
        return redirect(url_for('auth.atividade_prof',
                                turma_id=turma_id,
                                disciplina_id=disciplina_id,
                                nome_disciplina=nome_disciplina))

    cursor.close()
    return render_template(
        'editar_tarefa.html',
        atividade=atividade,
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina
    )

@bp.route('/editar_postagem/<int:turma_id>/<int:disciplina_id>/<string:nome_disciplina>/<int:post_id>', methods=['GET', 'POST'])
def editar_postagem(turma_id, disciplina_id, nome_disciplina, post_id):
    if 'usuario_id' not in session or session.get('usuario_tipo') not in ['professor', 'prof_coorde']:
        return redirect(url_for('auth.login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Buscar dados da postagem
    cursor.execute("""
        SELECT id, titulo, conteudo, arquivo
        FROM postagens
        WHERE id = %s
    """, (post_id,))
    postagem = cursor.fetchone()

    if not postagem:
        flash("Postagem não encontrada.", "danger")
        cursor.close()
        return redirect(url_for('auth.postagens_prof', turma_id=turma_id, disciplina_id=disciplina_id, nome_disciplina=nome_disciplina))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        conteudo = request.form.get('conteudo')
        arquivo = request.files.get('arquivo')
        nome_arquivo = postagem['arquivo']  # mantém o atual caso não troque

        if arquivo and arquivo.filename:
            nome_original = secure_filename(arquivo.filename.rsplit('.', 1)[0])
            extensao = arquivo.filename.rsplit('.', 1)[-1]
            data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_disciplina_seguro = secure_filename(nome_disciplina)

            novo_arquivo = f"{nome_original}_{nome_disciplina_seguro}_{data_atual}.{extensao}"

            # Exclui arquivo anterior
            if postagem['arquivo']:
                apagar_arquivo(postagem['arquivo'])

            nome_arquivo = salvar_arquivo(arquivo, novo_arquivo)[1]

        cursor.execute("""
            UPDATE postagens
            SET titulo = %s, conteudo = %s, arquivo = %s
            WHERE id = %s
        """, (titulo, conteudo, nome_arquivo, post_id))
        mysql.connection.commit()
        cursor.close()

        flash("Postagem atualizada com sucesso!", "success")
        return redirect(url_for('auth.postagens_prof', turma_id=turma_id, disciplina_id=disciplina_id, nome_disciplina=nome_disciplina))

    cursor.close()
    return render_template(
        'editar_postagem.html',
        postagem=postagem,
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        nome_disciplina=nome_disciplina
    )

@bp.route('/editar_informacoes_aluno', methods=['GET', 'POST'])
def editar_informacoes_aluno():
    if 'usuario_id' not in session or session.get('usuario_tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    aluno_id = session['usuario_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Buscar informações atuais do aluno
    cursor.execute("SELECT nome, email FROM usuarios WHERE id = %s", (aluno_id,))
    aluno = cursor.fetchone()

    if not aluno:
        flash("Aluno não encontrado.", "danger")
        return redirect(url_for('auth.dashboard_aluno'))

    if request.method == 'POST':
        nova_senha = request.form.get('senha')

        if not nova_senha:
            flash("Por favor, insira uma nova senha.", "warning")
        else:
            senha_hash = generate_password_hash(nova_senha)
            cursor.execute("UPDATE usuarios SET senha = %s WHERE id = %s", (senha_hash, aluno_id))
            mysql.connection.commit()
            flash("Senha atualizada com sucesso!", "success")
            return redirect(url_for('auth.editar_informacoes_aluno'))

    return render_template('editar_informacoes_aluno.html', aluno=aluno)
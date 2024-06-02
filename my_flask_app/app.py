from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.db'  # Caminho para o arquivo do banco de dados
db = SQLAlchemy(app)

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    imagem = db.Column(db.String(100))

# Código para criar o banco de dados (executar uma vez para criar o banco de dados)
with app.app_context():
    db.create_all()

# Rota para renderizar a página inicial
@app.route('/')
def index():
    cursos = Curso.query.all()
    return render_template('index.html', cursos=cursos)

# Rota para adicionar um novo curso
@app.route('/adicionar_curso', methods=['POST'])
def adicionar_curso():
    if request.method == 'POST':
        nome_curso = request.form['nome_curso']
        imagem_curso = request.files['imagem_curso']

        # Salvar a imagem em algum diretório e obter o caminho dela
        # Por exemplo, você pode salvar em 'static/images' e armazenar o caminho no banco de dados

        # Criar um novo curso com os dados fornecidos
        novo_curso = Curso(nome=nome_curso, imagem=imagem_curso.filename)

        # Adicionar o novo curso ao banco de dados
        db.session.add(novo_curso)
        db.session.commit()

    return redirect(url_for('index'))

# Rota para excluir um curso
@app.route('/excluir-curso/<int:curso_id>', methods=['POST'])
def excluir_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

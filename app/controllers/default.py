from pickle import TRUE
from app import app, db, mail, Message
from flask import render_template, request, redirect, url_for, make_response, session
from flask_login import login_user, logout_user
from datetime import datetime
from werkzeug.security import generate_password_hash
import secrets, sqlite3, csv, io

from app.models.tables import Clientes, Produtos, User, Pedidos

@app.route("/PaginaInicial")
def PaginaInicial():
    return render_template("PaginaInicial.html")

@app.route("/RegistrarLogin", methods=["GET", "POST"])
def RegistrarLogin():
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        pwd = request.form.get("password")
        user = User(name, email, pwd)
        valida_email = db.session.query(db.session.query(User).filter_by(email=email).exists()).scalar()

        if valida_email == True:
            return """
                <script>
                    alert('E-mail já registrado no banco de dados')
                    window.open("http://127.0.0.1:5000/RegistrarLogin", "_self")
                </script>
            """
            
        else:
            db.session.add(user)
            db.session.commit()
            return """
                <script>
                    alert('Seus dados de login foram registrados com sucesso!')
                    window.open("http://127.0.0.1:5000/Login", "_self")
                </script>
            """
        
    return render_template("RegistrarLogin.html")

@app.route("/", methods=["GET", "POST"])
@app.route("/Login", methods=["GET", "POST"])
def Login():

    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(pwd):

            return """
                <script>
                    alert('E-mail ou senha inseridos incorretamente, tente novamente.')
                    window.open("http://127.0.0.1:5000/Login", "_self")
                </script>
            """
        
        login_user(user)
        return redirect(url_for("PaginaInicial"))

    return render_template("Login.html")

@app.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for("Login"))

@app.route("/RecuperarSenha", methods=["GET", "POST"])
def RecuperarSenha():

    if request.method == "POST":
        email = request.form.get("email")
        session['email'] = email
        valida_email = db.session.query(db.session.query(User).filter_by(email=email).exists()).scalar()

        if valida_email == True:
            lenght = 12
            caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:<>,.?/~`"
            codigo = ''.join(secrets.choice(caracteres) for i in range(lenght))
            session['codigo'] = codigo
            msg = Message("Software-Product", sender='software.product.bot@gmail.com', 
                      recipients=[email])
            msg.html = f"Olá!<br><br>Você informou este e-mail como endereço de recuperação de senha, aqui está seu código de confirmação:<br><br><center><p><strong style='font-size: 24px'>{codigo}</strong></p></center>"
            mail.send(msg)

            return """
                <script>
                    alert('Código de confirmação enviado com Sucesso!')
                    window.open("http://127.0.0.1:5000/ConfirmarCodigo", "_self")
                </script>
                """

        else:

            return """
                <script>
                    alert('E-mail referenciado não encontrado no banco de dados')
                    window.open("http://127.0.0.1:5000/RecuperarSenha", "_self")
                </script>
                """
        
    return render_template("RecuperarSenha.html")

@app.route("/ConfirmarCodigo", methods=["GET", "POST"])
def ConfirmarCodigo():

    if request.method == "POST":
        verifica_codigo = request.form.get("codigo")
        codigo = session.get("codigo")
        
        if verifica_codigo == codigo:
            return """
                <script>
                    alert('Código de confirmação inserido corretamente!')
                    window.open("http://127.0.0.1:5000/RedefinirSenha", "_self")
                </script>
                """
        
        else:
            return """
                <script>
                    alert('Código de confirmação inserido incorretamente, tente novamente.')
                    window.open("http://127.0.0.1:5000/ConfirmarCodigo", "_self")
                </script>
                """

    return render_template("ConfirmarCodigo.html")

@app.route("/RedefinirSenha", methods=["GET", "POST"])
def RedefinirSenha():

    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        
        if confirm_password == password:
            email = session.get("email")
            user = User.query.filter_by(email=email).first()
            user.password = generate_password_hash(password)
            db.session.commit()
            return """
                <script>
                    alert('Sua senha foi atualizada com sucesso!')
                    window.open("http://127.0.0.1:5000/Login", "_self")
                </script>
                """
        
        else:
            return """
                <script>
                    alert('As senhas digitadas não coincidem. Por favor, digite novamente.')
                    window.open("http://127.0.0.1:5000/RedefinirSenha", "_self")
                </script>
                """

    return render_template("RedefinirSenha.html")

@app.route("/ClientesCRUD")
def ClientesCRUD():
    return render_template("ClientesCRUD.html")

@app.route("/CadastrarCliente", methods=["GET", "POST"])
def CadastrarCliente():

    if request.method == "POST":
        cliente = request.form.get("cliente")
        email = request.form.get("email")
        fone = request.form.get("fone")
        genero = request.form.get("genero")
        nascimento_date = datetime.strptime(request.form.get("nascimento"), "%Y-%m-%d").date()
        nascimento = nascimento_date.strftime("%d-%m-%Y")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")
        endereco = request.form.get("endereco")
        cadastrar_cliente = Clientes(cliente, email, fone, genero, 
                nascimento, cidade, estado, endereco)
        valida_email = db.session.query(db.session.query(Clientes).filter_by(email=email).exists()).scalar()

        if valida_email == True:
            return """
                <script>
                    alert('E-mail de usuário referenciado já registrado no banco de dados')
                    window.open("http://127.0.0.1:5000/CadastrarCliente", "_self")
                </script>
            """

        else:
            db.session.add(cadastrar_cliente)
            db.session.commit()
            return """
                <script>
                    alert('Os dados do(a) cliente foram registrados com sucesso!')
                    window.open("http://127.0.0.1:5000/ClientesCRUD", "_self")
                </script>
            """

    return render_template("CadastrarCliente.html")

@app.route("/EditarCliente", methods=["GET", "POST"])
def EditarCliente():

    if request.method == "POST":
        id = request.form.get("id_cliente")
        valida_id = db.session.query(db.session.query(Clientes).filter_by(id=id).exists()).scalar()

        if valida_id == True:
            cliente = Clientes.query.get(id)
            cliente.cliente = request.form.get("cliente")
            email = request.form.get("email")
            cliente.fone = request.form.get("fone")
            cliente.genero = request.form.get("genero")
            nascimento_date = datetime.strptime(request.form.get("nascimento"), "%Y-%m-%d").date()
            nascimento = nascimento_date.strftime("%d-%m-%Y")
            cliente.nascimento = nascimento
            cliente.cidade = request.form.get("cidade")
            cliente.estado = request.form.get("estado")
            cliente.endereco = request.form.get("endereco")

            if cliente.email == email:
                db.session.commit()
                return """
                    <script>
                        alert('Registro do Cliente atualizado com sucesso!')
                        window.open("http://127.0.0.1:5000/ClientesCRUD", "_self")
                    </script>
                """

            else:
                valida_email = db.session.query(db.session.query(Clientes).filter_by(email=email).exists()).scalar()

                if valida_email == True:
                    return """
                        <script>
                            alert('E-mail de usuário referenciado já registrado no banco de dados')
                            window.open("http://127.0.0.1:5000/EditarCliente", "_self")
                        </script>
                    """

                else:
                    cliente.email = request.form.get("email")
                    db.session.commit()
                    return """
                        <script>
                            alert('Registro do Cliente atualizado com sucesso!')
                            window.open("http://127.0.0.1:5000/ClientesCRUD", "_self")
                        </script>
                    """

        else:
            return """
                    <script>
                        alert('Cliente com ID referenciado não encontrado dentro do banco de dados')
                        window.open("http://127.0.0.1:5000/EditarCliente", "_self")
                    </script>
            """

    return render_template("EditarCliente.html")

@app.route("/DeletarCliente", methods=["GET", "POST"])
def DeletarCliente():
    
    if request.method == "POST":
        id = request.form.get("id_cliente")
        valida_id = db.session.query(db.session.query(Clientes).filter_by(id=id).exists()).scalar()

        if valida_id == True:
            cliente = Clientes.query.filter_by(id=id).first()
            db.session.delete(cliente)
            db.session.commit()
            return """
                    <script>
                        alert('Registro do Cliente deletado com sucesso!')
                        window.open("http://127.0.0.1:5000/ClientesCRUD", "_self")
                    </script>
            """
        
        else:
            return """
                    <script>
                        alert('Cliente com ID referenciado não encontrado dentro do banco de dados')
                        window.open("http://127.0.0.1:5000/DeletarCliente", "_self")
                    </script>
            """

    return render_template("DeletarCliente.html")

@app.route("/ProdutosCRUD")
def ProdutosCRUD():
    return render_template("ProdutosCRUD.html")

@app.route("/CadastrarProduto", methods=["GET", "POST"])
def CadastrarProduto():
    
    if request.method == "POST":
        nome_produto = request.form.get("nome_produto")
        codigo_produto = request.form.get("codigo_produto")
        quantidade = request.form.get("quantidade")
        produto = request.form.get("produto")
        data_cadastro = datetime.now().strftime('%d/%m/%Y %H:%M')
        cadastrar_produto = Produtos(nome_produto, codigo_produto, quantidade, 
                                     produto, data_cadastro)
        valida_codigo_produto = db.session.query(db.session.query(Produtos).filter_by(codigo_produto=codigo_produto).exists()).scalar()

        if valida_codigo_produto == True:
            return """
                    <script>
                        alert('Código do Produto já registrado no Banco de Dados')
                        window.open("http://127.0.0.1:5000/CadastrarProduto", "_self")
                    </script>
            """

        else:
            db.session.add(cadastrar_produto)
            db.session.commit()
            return """
                        <script>
                            alert('Dados do Produto cadastrado com sucesso!')
                            window.open("http://127.0.0.1:5000/ProdutosCRUD", "_self")
                        </script>
                """
    
    return render_template("CadastrarProduto.html")

@app.route("/EditarProduto", methods=["GET", "POST"])
def EditarProduto():

    if request.method == "POST":
        id = request.form.get("id_produto")
        valida_id = db.session.query(db.session.query(Produtos).filter_by(id=id).exists()).scalar()

        if valida_id == True:
            produto = Produtos.query.get(id)
            produto.nome_produto = request.form.get("nome_produto")
            codigo_produto = request.form.get("codigo_produto")
            produto.quantidade = request.form.get("quantidade")
            produto.produto = request.form.get("produto")

            if produto.codigo_produto == int(codigo_produto):
                db.session.commit()
                return """
                    <script>
                        alert('Registro do Produto atualizado com sucesso!')
                        window.open("http://127.0.0.1:5000/ProdutosCRUD", "_self")
                    </script>
                """

            else:
                valida_codigo_produto = db.session.query(db.session.query(Produtos).filter_by(codigo_produto=codigo_produto).exists()).scalar()

                if valida_codigo_produto == True:
                    return """
                        <script>
                            alert('Código do Produto já registrado no Banco de Dados')
                        window.open("http://127.0.0.1:5000/EditarProduto", "_self")
                        </script>
                    """

                else:
                    produto.codigo_produto = request.form.get("codigo_produto")
                    db.session.commit()
                    return """
                        <script>
                            alert('Registro do Produto atualizado com sucesso!')
                        window.open("http://127.0.0.1:5000/ProdutosCRUD", "_self")
                        </script>
                    """

        else:
            return """
                    <script>
                        alert('Produto com ID referenciado não encontrado dentro do banco de dados')
                        window.open("http://127.0.0.1:5000/EditarProduto", "_self")
                    </script>
            """
                
    return render_template("EditarProduto.html")

@app.route("/DeletarProduto", methods=["GET", "POST"])
def DeletarProduto():
    
    if request.method == "POST":
        id = request.form.get("id_produto")
        valida_id = db.session.query(db.session.query(Produtos).filter_by(id=id).exists()).scalar()

        if valida_id == True:
            produto = Produtos.query.filter_by(id=id).first()
            db.session.delete(produto)
            db.session.commit()
            return """
                    <script>
                        alert('Registro do Produto deletado com sucesso!')
                        window.open("http://127.0.0.1:5000/ProdutosCRUD", "_self")
                    </script>
            """
        
        else:
            return """
                    <script>
                        alert('Produto com ID referenciado não encontrado dentro do banco de dados')
                        window.open("http://127.0.0.1:5000/DeletarProduto", "_self")
                    </script>
            """

    return render_template("DeletarProduto.html")

@app.route("/PedidosCRUD")
def PedidosCRUD():
    return render_template("PedidosCRUD.html")

@app.route("/RegistrarPedido", methods=["GET", "POST"])
def RegistrarPedido():

    if request.method == "POST":
        email_cliente = request.form.get("email_cliente")
        codigo_produto = request.form.get("codigo_produto")
        quantidade = request.form.get("quantidade")
        status = "Aprovado"
        valida_email_cliente = db.session.query(db.session.query(Clientes).filter_by(email=email_cliente).exists()).scalar()
        valida_codigo_produto = db.session.query(db.session.query(Produtos).filter_by(codigo_produto=codigo_produto).exists()).scalar()
        produto = Produtos.query.get(codigo_produto)
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
        registrar_pedido = Pedidos(email_cliente, codigo_produto, quantidade, status, data_hora)

        if valida_email_cliente == True:

            if valida_codigo_produto == True:
                    
                if produto.quantidade >= int(quantidade):
                    produto.quantidade = produto.quantidade - int(quantidade)
                    db.session.add(registrar_pedido)
                    db.session.commit()
                    return """
                            <script>
                                alert('Seu pedido foi registrado com sucesso!')
                                window.open("http://127.0.0.1:5000/PedidosCRUD", "_self")
                            </script>
                    """
                
                else:
                    return """
                        <script>
                            alert('Quantidade solicitada do produto indisponível!')
                            window.open("http://127.0.0.1:5000/RegistrarPedido", "_self")
                        </script>
                        """
            else:
                return """
                <script>
                    alert('Código do produto referenciado não encontrado dentro do banco de dados')
                    window.open("http://127.0.0.1:5000/RegistrarPedido", "_self")
                </script>
                """

        else:
            return """
                <script>
                    alert('Cliente com e-mail referenciado não encontrado dentro do banco de dados')
                    window.open("http://127.0.0.1:5000/RegistrarPedido", "_self")
                </script>
                """

    return render_template("RegistrarPedido.html")

@app.route("/EditarPedido", methods=["GET", "POST"])
def EditarPedido():

    if request.method == "POST":
        id = request.form.get("id_pedido")
        valida_id = db.session.query(db.session.query(Pedidos).filter_by(id=id).exists()).scalar()

        if valida_id == True:
            pedido = Pedidos.query.get(id)
            produto = Produtos.query.get(pedido.codigo_produto)
            quantidade = request.form.get("quantidade")

            if produto.quantidade + pedido.quantidade >= int(quantidade):
                produto.quantidade = produto.quantidade + int(pedido.quantidade) - int(quantidade)
                pedido.quantidade = quantidade
                db.session.commit()
                return """
                    <script>
                        alert('Registro de Pedido atualizado com sucesso!')
                    window.open("http://127.0.0.1:5000/PedidosCRUD", "_self")
                    </script>
                """
            
            else:
                return """
                    <script>
                        alert('Quantidade solicitada do produto indisponível!')
                    window.open("http://127.0.0.1:5000/EditarPedido", "_self")
                    </script>
                """
            
        else:
            return """
                    <script>
                        alert('Pedido com ID referenciado não encontrado dentro do banco de dados')
                        window.open("http://127.0.0.1:5000/EditarPedido", "_self")
                    </script>
            """

    return render_template("EditarPedido.html")

@app.route("/CancelarPedido", methods=["GET", "POST"])
def CancelarPedido():

    if request.method == "POST":
        id = request.form.get("id_pedido")
        valida_id = db.session.query(db.session.query(Pedidos).filter_by(id=id).exists()).scalar()

        if valida_id == True:
            pedido = Pedidos.query.get(id)
            produto = Produtos.query.get(pedido.codigo_produto)
            produto.quantidade = produto.quantidade + pedido.quantidade
            pedido.status = "Cancelado"
            db.session.commit()
            return """
                    <script>
                        alert('Solicitação de cancelamento do Pedido realizada com sucesso!')
                        window.open("http://127.0.0.1:5000/PedidosCRUD", "_self")
                    </script>
            """
        
        else:
             return """
                    <script>
                        alert('Pedido com ID referenciado não encontrado dentro do banco de dados')
                        window.open("http://127.0.0.1:5000/CancelarPedido", "_self")
                    </script>
            """
        
    return render_template("CancelarPedido.html")

@app.route("/GerarRelatorio", methods=["GET", "POST"])
def GerarRelatorio():

    if request.method == "POST":
        periodo_de_date = datetime.strptime(request.form.get("periodo-de"), "%Y-%m-%dT%H:%M")
        periodo_de = periodo_de_date.strftime("%d/%m/%Y %H:%M")
        periodo_ate_date = datetime.strptime(request.form.get("periodo-ate"), "%Y-%m-%dT%H:%M")
        periodo_ate = periodo_ate_date.strftime("%d/%m/%Y %H:%M")
        date_now = datetime.now().strftime("%d/%m/%Y %H:%M")

        if periodo_de > periodo_ate:
            return """
                    <script>
                        alert('Periodo final não pode ser anterior ao periodo inicial')
                        window.open("http://127.0.0.1:5000/GerarRelatorio", "_self")
                    </script>
            """
        
        if periodo_ate > date_now:
            periodo_ate = date_now
        
        conn = sqlite3.connect('storage.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Pedidos WHERE data_hora BETWEEN ? AND ?", (periodo_de, periodo_ate))
        Pedidos = cursor.fetchall()

        if Pedidos == []:
            return """
                    <script>
                        alert('Nenhum Pedido realizado no período selecionado')
                        window.open("http://127.0.0.1:5000/GerarRelatorio", "_self")
                    </script>
            """

        conn.close()
        cabeçalho = [['Id', 'E-mail do Cliente', 'Codigo do Produto', 'Quantidade', 'Data e Hora de Pedido', 'Status do Pedido']]

        for pedido in Pedidos:
            cabeçalho.append([
                pedido[0], 
                pedido[1], 
                pedido[2], 
                pedido[3], 
                pedido[4],
                pedido[5]
            ])

        output = io.StringIO()
        writer = csv.writer(output, delimiter=';')
        writer.writerows(cabeçalho)
        response = make_response(output.getvalue())
        response.headers.set('Content-Disposition', 'attachment', filename='report.csv')
        response.headers.set('Content-Type', 'text/csv')

        return response

    return render_template("GerarRelatorio.html")

@app.route("/DeletarDados")
def DeletarDados():
    clientes = Clientes.query.all()
    produtos = Produtos.query.all()
    pedidos = Pedidos.query.all()

    for cliente in clientes:
        db.session.delete(cliente)
    for produto in produtos:
        db.session.delete(produto)
    for pedido in pedidos:
        db.session.delete(pedido)

    db.session.commit()

    return render_template("Login.html")
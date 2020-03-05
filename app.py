"""
Capa de presentación
"""

# Imports
from flask import Flask, render_template, url_for, request, flash, redirect
import negocio

#Configuración de flask
app = Flask(__name__)

user_logged = False
current_stock_info = [[]]
@app.route('/')
def index():
    if user_logged:
        print(user_logged)
        return render_template('index.html', user_stocks= user_logged["stocks"], stock_info = current_stock_info, news = negocio.get_news())
    else: return login()


@app.route('/login', methods=["POST","GET"])
def login():
    global user_logged
    
    if request.method  == "GET" and request.args != {}:
        username = request.args['username'][:-13]
        password = request.args['pass']
        action = request.args['username'][-10:]
        print(username," ",password, " ", action)
        if action == "Logging in":
            user_logged = negocio.login(username,password)
            if user_logged:
                print('Inicio de sesión exitoso')
                update_stock_data()
                return redirect('/')
            else:
                print('Error en inicio de sesión')

        elif action == "Signing up":
            if negocio.add_user(username,password):
                user_logged = negocio.login(username,password)
                print('Registro exitoso')
                update_stock_data()
                return redirect('/')
            else:
                print('Error de registro')
        else:
            print(action)
            raise Exception("Acción no reconocida")
    return render_template('login.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    global user_logged
    stocks = request.form['stocks']
    update_one_stock_data(stocks,user_logged["stocks"])
    user_logged = negocio.update_user(stocks,user_logged)
    return redirect('/')


def update_stock_data():
    global current_stock_info
    current_stock_info = negocio.update_stock_data(user_logged["stocks"])

def update_one_stock_data(new_stocks,old_stocks):
    global current_stock_info
    current_stock_info = negocio.update_one_stock_data(new_stocks,old_stocks,current_stock_info)

if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
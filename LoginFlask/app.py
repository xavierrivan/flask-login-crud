from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secreto123'

datos = [
    {'id': 1, 'nombre': 'Elemento 1'},
    {'id': 2, 'nombre': 'Elemento 2'}
]
contador_id = 3 

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == '1234':
        session['user'] = username
        return redirect(url_for('dashboard'))
    else:
        return 'Credenciales incorrectas'

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/crud')
def crud():
    if 'user' in session:
        return render_template('crud.html', datos=datos)
    return redirect(url_for('home'))

@app.route('/create', methods=['POST'])
def create():
    global contador_id
    nombre = request.form['nombre']
    datos.append({'id': contador_id, 'nombre': nombre})
    contador_id += 1
    return redirect(url_for('crud'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nombre = request.form['nombre']
    for d in datos:
        if d['id'] == id:
            d['nombre'] = nombre
            break
    return redirect(url_for('crud'))

@app.route('/delete/<int:id>')
def delete(id):
    global datos
    datos = [d for d in datos if d['id'] != id]
    return redirect(url_for('crud'))

if __name__ == '__main__':
    app.run(debug=True)

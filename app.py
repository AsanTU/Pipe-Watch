from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import datetime
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('pipes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    pipes = conn.execute('SELECT * FROM pipes').fetchall()
    conn.close()
    return render_template('main_screen.html', pipes=pipes)

@app.route('/add', methods=['POST'])
def add_pipe():
    if request.method == 'POST':
        pipe_name = request.form.get('pipe-name')
        if pipe_name[0].isdigit():
            return "Название трубы не должно начинаться с цифры!", 400
        
        diameter = request.form['diameter']
        state = request.form['state']
        date_added = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f"Inserting: {pipe_name}, {diameter}, {state}, {date_added}")

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO pipes (name, diameter, state, date_added) VALUES (?, ?, ?, ?)',
                     (pipe_name, diameter, state, date_added))
            conn.commit()
            print("Data inserted successfully")
        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()

        return redirect('/')

@app.route('/details/<int:id>')
def pipe_details(id):
    conn = get_db_connection()
    pipe = conn.execute('SELECT * FROM pipes WHERE id = ?', (id, )).fetchone()
    conn.close()
    if pipe is None:
        return "Труба не найдена", 404
    
    return render_template('pipe_details.html', pipe=pipe)

if __name__ == '__main__':
    app.run(debug=True)

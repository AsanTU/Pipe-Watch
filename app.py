from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('pipes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    page = int(request.args.get('page', 1))  
    per_page = 10                            
    offset = (page - 1) * per_page           

    conn = get_db_connection()

    total_pipes = conn.execute('SELECT COUNT(*) FROM pipes').fetchone()[0]

    pipes = conn.execute('SELECT * FROM pipes LIMIT ? OFFSET ?', (per_page, offset)).fetchall()
    conn.close()

    total_pages = (total_pipes + per_page - 1) // per_page

    return render_template('main_screen.html', pipes=pipes, page=page, total_pages=total_pages)


@app.route('/add', methods=['POST'])
def add_pipe():
    page = request.args.get('page', 1)  
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
            print(f"Error inserting data: {e}", 500)
        finally:
            conn.close()

        return redirect(url_for('home', page=page))

@app.route('/details/<int:id>')
def pipe_details(id):
    page = request.args.get('page', 1)  
    conn = get_db_connection()
    pipe = conn.execute('SELECT * FROM pipes WHERE id = ?', (id, )).fetchone()
    conn.close()
    if pipe is None:
        return "Труба не найдена", 404
    
    return render_template('pipe_details.html', pipe=pipe, page=page)

if __name__ == '__main__':
    app.run(debug=True)

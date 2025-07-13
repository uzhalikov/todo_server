from flask import request, jsonify, session
from main import app
from db import get_db


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    page = int(request.args.get('page', 1))
    limit = 3
    offset = (page - 1) * limit

    conn = get_db()
    cur = conn.cursor()
    cur.execute(f'''
        SELECT * FROM tasks
        ORDER BY {sort_by} {order}
        LIMIT ? OFFSET ?
    ''', (limit, offset))
    tasks = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(tasks)


@app.route('/api/tasks/count', methods=['GET'])
def get_tasks_count():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) as total FROM tasks')
    total = cur.fetchone()['total']
    conn.close()
    return jsonify({'total': total})


@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    text = data.get('text')

    if not username or not email or not text:
        return jsonify({'error': 'All fields are required'}), 400
    if '@' not in email:
        return jsonify({'error': 'Invalid email'}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO tasks (username, email, text) VALUES (?, ?, ?)',
                (username, email, text))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get('username') == 'admin' and data.get('password') == '123':
        session['admin'] = True
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('admin', None)
    return jsonify({'success': True})


@app.route('/api/is_admin', methods=['GET'])
def is_admin():
    return jsonify({'is_admin': session.get('admin', False)})


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    text = data.get('text')
    completed = data.get('completed')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT text FROM tasks WHERE id = ?', (task_id,))
    original = cur.fetchone()

    edited = False
    if original and original['text'] != text:
        edited = True

    cur.execute('''
        UPDATE tasks SET text = ?, completed = ?, edited_by_admin = ?
        WHERE id = ?
    ''', (text, completed, edited, task_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = jsonify()
    response.headers.add('Access-Control-Allow-Origin', 'https://todo-client-seven-psi.vercel.app')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
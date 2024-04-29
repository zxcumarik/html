from flask import Flask, render_template, url_for, redirect, abort

app = Flask(__name__)

test_name = 'Flask'
max_score = 20
students = [
    {'id': 1, 'name': 'Artem', 'score': 10, 'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt utqwerty labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'},
    {'id': 2, 'name': 'Martin', 'score': 20, 'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'},
    {'id': 3, 'name': 'Masha', 'score': 5, 'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'},
    {'id': 4, 'name': 'Karina', 'score': 15, 'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'},
]


@app.route('/')
def home_page():
    return render_template('home.html', owner='John')


@app.route('/max')
def max_score():
    return render_template('max.html', students=students)


@app.route('/sorted')
def sorted_score():
    return render_template('sorted_score.html', students=students)


@app.route('/students')
def home():
    context = {
        'title': 'Students',
        'students': students,
        'max_score': max_score,
        'test': test_name
    }
    return render_template('index.html', **context)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/student/<int:id>')
def student(id):
    if id > len(students):
        return redirect(url_for('home'))
    elif id == 4:
        abort(403)
    return render_template('detail.html', student=students[id-1])


@app.errorhandler(404)
def error404(error):
    return render_template('error404.html'),  404


if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('about'))
        print(url_for('home'))
    app.run(debug=True)
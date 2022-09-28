from flask import Flask, render_template, request, escape
import mysql.connector

app = Flask(__name__)


@app.route('/search', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    title = 'Here are your results:'
    log_request(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_letters=letters,
                           the_phrase=phrase,
                           the_results=results, )


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('vsearchlogs.txt') as logs:
        for line in logs:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('logs.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents, )


def search4letters(vowels, word):
    return set(vowels).intersection(set(word))


def log_request(req: 'flask_request', res: str) -> None:
    dbconfig = {'host': '127.0.0.1',
                'user': 'root',
                'password': 'Slavik2477766',
                'database': 'vsearchlogDB', }
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert into log 
     (phrase, letters, ip, browser_string, results) 
     values 
     (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          'NULL',
                          res,))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)

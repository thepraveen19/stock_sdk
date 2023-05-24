from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    # Perform search logic here or customize it according to your requirements
    return render_template('search_results.html', query=query)

if __name__ == '__main__':
    app.run(debug=True)

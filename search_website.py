from flask import Flask, request, jsonify, render_template
import os
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    os.system(f"python3 search.py {query}")
    
    f = open(".results_"+".".join(query.split(" ")), "rb")
    data = pickle.loads(f.read())
    f.close()

    output = {
        "urls": data["res"],
        "summary": f"Query : {query} | Total Results : {len(data['res'])} | Time Taken : {data['time']}"
        }

    return jsonify(output)

if __name__ == '__main__':
    app.run(port="8080")


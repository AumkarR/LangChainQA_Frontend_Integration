from flask import Flask, request, jsonify #Importing Flask to setup the backend; Importing request and jsonify to send a response when a post query is called
from main import query #Importing the query() function defined in main.py for returning a response
from flask_cors import CORS #Importing CORS to ensure that cross-origin requests are handled

app = Flask(__name__) #Creating a flask app, and allowing CORS to allow all connections
CORS(app)

@app.route('/') #Ensuring the running of the server when navigating to the homepage on localhost
def home():
    return 'Server is running!'

@app.route('/query', methods=['POST']) #Handling the post request set at /query
def handle_query():
    try: #Ensuring that the prompt is recieved on the backend
        prompt = request.json['prompt']
    except KeyError:
        return jsonify({'error': 'prompt is missing'}), 400

    try: #Storing the response of the chatbot
        response = query(prompt)
    except Exception as e:
        print(f'Error in query: {e}')
        return jsonify({'error': 'something went wrong'}), 500

    if response is None: #Checking for potential errors in the backend logic if the response was not returned correctly
        return jsonify({'error': 'no response found'}), 404

    return jsonify({'bot': response}), 201 #Returning the bot's response as a JSON object after the post query is called

if __name__ == '__main__':
    app.run(port = 2784, host='0.0.0.0') #Ensuring that the Flask server is running at port 2784 on local host. Also allowing all IPs to connect (had to include due to CORS errors)

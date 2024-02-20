import pickle
from neo4j import GraphDatabase

# Function to pickle the authentication values
def pickle_auth(uri, username, password):
    auth_info = {'uri': uri, 'username': username, 'password': password}
    with open('auth_info.pickle', 'wb') as f:
        pickle.dump(auth_info, f)
    print("Authentication values pickled successfully.")

# Function to load the authentication values from the pickle file
def load_auth():
    with open('auth_info.pickle', 'rb') as f:
        auth_info = pickle.load(f)
    return auth_info['uri'], auth_info['username'], auth_info['password']

# Pickle the authentication values
pickle_auth("neo4j+s://7c439dc5.databases.neo4j.io", "neo4j", "wcsN2PuSPnMKgAIJL_NTlPY8HJ6lkFCz0AcRuvy630I")

# Load the authentication values
uri, username, password = load_auth()

# Connect to Neo4j using the loaded authentication values
driver = GraphDatabase.driver(uri, auth=(username, password))
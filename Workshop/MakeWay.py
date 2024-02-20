from neo4j import GraphDatabase
import pickle

def loadAuth():
    with open('auth.pickle', 'rb') as f:
        auth_info = pickle.load(f)
    return auth_info['uri'], auth_info['username'], auth_info['password']

uri, username, password = loadAuth()

driver = GraphDatabase.driver(uri, auth=(username, password))

def run_query(query, session):
    result = session.run(query)
    return result

def create_nodes_and_relationships():
    with driver.session() as session:
        query = """
        CREATE (s1:State {name: 'desktop'})-
        [:CONNECTED]->(a1:Action {name: 'mouse', action:'move', value: [15,1059]})-
        [:CONNECTED]->(a2:Action {name: 'mouse', action:'click', value: 'left'})-
        [:CONNECTED]->(a3:Action {name: 'keyboardstroke', action:'type', value:'powerpoint'})-
        [:CONNECTED]->(a4:Action {name: 'keyboardstroke', action:'press', value:'enter'})-
        [:CONNECTED]->(a5:State {name: 'powerpoint'}),
        (s1)-[:CONNECTED]->(a6:Action {name: 'keyboardstroke', action:'press', value:'win'})-
        [:CONNECTED]->(a3)
        """
        run_query(query, session)

create_nodes_and_relationships()

driver.close()

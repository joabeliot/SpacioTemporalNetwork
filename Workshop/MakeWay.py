from neo4j import GraphDatabase

uri = "neo4j+s://7c439dc5.databases.neo4j.io"
username = "neo4j"
password = "<apiKey>"

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

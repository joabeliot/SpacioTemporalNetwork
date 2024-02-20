from neo4j import GraphDatabase
import pyautogui
import pickle

def loadAuth():
    with open('auth.pickle', 'rb') as f:
        auth_info = pickle.load(f)
    return auth_info['uri'], auth_info['username'], auth_info['password']

uri, username, password = loadAuth()

driver = GraphDatabase.driver(uri, auth=(username, password))

def mouseMove(x,y):
    pyautogui.moveTo(x,y)

def mouseClick(butt):
    if butt == "left":
        pyautogui.click(button='left')
    elif butt == "right":
        pyautogui.click(button='right')
    else:
        print(f"{butt} not found")

def keyboardPress(press):
    pyautogui.press(press)

def keyboardType(text):
    pyautogui.write(text,interval="0.25")

def run_query(query, session):
    result = session.run(query)
    return result

def find_path():
    with driver.session() as session:
        query = """
        MATCH shortestPath((start:State {name: 'desktop'})-[:CONNECTED*]->(end:State {name: 'powerpoint'}))
        RETURN nodes(shortestPath((start)-[:CONNECTED*]->(end))) AS path
        """
        result = run_query(query, session)
        for record in result:
            path=record["path"]

            for node in path:
                if next(iter(node.labels)) == "State":
                    pass
                elif next(iter(node.labels)) == "Action":
                    if node._properties['name'] == "mouse" and node._properties['action'] == "move":
                        mouseMove(node._properties['value'][0],node._properties['value'][1])
                    elif node._properties['name'] == "mouse" and node._properties['action'] == "click":
                        mouseClick(node._properties["value"])
                    elif node._properties['name'] == "keyboardstroke" and node._properties['action'] == "press":
                        keyboardPress(node._properties['value'])
                    elif node._properties['name'] == "keyboardstroke" and node._properties['action'] == "type":
                        keyboardType(node._properties['value'])

find_path()

driver.close()
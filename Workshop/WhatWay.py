from neo4j import GraphDatabase
import pyautogui

uri = "neo4j+s://7c439dc5.databases.neo4j.io"
username = "neo4j"
password = "<apikey>"

driver = GraphDatabase.driver(uri, auth=(username, password))

intermediate_nodes=[]

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

def find_intermediate_nodes():
    global intermediate_nodes
    with driver.session() as session:
        query = """
        MATCH shortestPath((start:State {name: 'desktop'})-[:CONNECTED*]->(end:State {name: 'powerpoint'}))
        RETURN nodes(shortestPath((start)-[:CONNECTED*]->(end))) AS intermediate_nodes
        """
        result = run_query(query, session)
        for record in result:
            intermediate_nodes=record["intermediate_nodes"]
            # print("###",intermediate_nodes)

            for node in intermediate_nodes:
                if next(iter(node.labels)) == "State":
                    pass
                elif next(iter(node.labels)) == "Action":
                    if node._properties['name'] == "mouse" and node._properties['action'] == "move":
                        mouseMove(node._properties['value'][0],node._properties['value'][1])
                    elif node._properties['name'] == "mouse" and node._properties['action'] == "click":
                        # print(type(node._properties["value"]),node._properties["value"])
                        mouseClick(node._properties["value"])
                    elif node._properties['name'] == "keyboardstroke" and node._properties['action'] == "press":
                        keyboardPress(node._properties['value'])
                    elif node._properties['name'] == "keyboardstroke" and node._properties['action'] == "type":
                        keyboardType(node._properties['value'])

find_intermediate_nodes()

driver.close()
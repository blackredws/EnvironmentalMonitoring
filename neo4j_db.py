from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "Sura@1221"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)
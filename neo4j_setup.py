from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "Sura@1221")
)

with driver.session() as session:

    session.run("""
        MERGE (t:Sensor {name:'temp1'})
        MERGE (h:Sensor {name:'hum1'})
        MERGE (g:Gateway {name:'gateway1'})
        MERGE (r:Room {name:'room101'})

        MERGE (t)-[:CONNECTED_TO]->(g)
        MERGE (h)-[:CONNECTED_TO]->(g)
        MERGE (g)-[:LOCATED_IN]->(r)
    """)

print("Graph created successfully!")

driver.close()
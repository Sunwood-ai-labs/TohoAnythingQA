from neo4j import GraphDatabase
from typing import List, Dict

class Neo4jManager:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label: str, properties: Dict):
        with self.driver.session() as session:
            session.write_transaction(self._create_node, label, properties)

    @staticmethod
    def _create_node(tx, label: str, properties: Dict):
        query = (
            f"CREATE (n:{label} $properties)"
        )
        tx.run(query, properties=properties)

    def create_relationship(self, start_node: Dict, end_node: Dict, relationship_type: str):
        with self.driver.session() as session:
            session.write_transaction(self._create_relationship, start_node, end_node, relationship_type)

    @staticmethod
    def _create_relationship(tx, start_node: Dict, end_node: Dict, relationship_type: str):
        query = (
            f"MATCH (a:{start_node['label']} {{title: $start_title}}), "
            f"(b:{end_node['label']} {{title: $end_title}}) "
            f"CREATE (a)-[r:{relationship_type}]->(b)"
        )
        tx.run(query, start_title=start_node['title'], end_title=end_node['title'])

if __name__ == "__main__":
    # テスト用のコード
    neo4j_manager = Neo4jManager("bolt://localhost:7687", "neo4j", "your_password")
    
    # ノードの作成
    neo4j_manager.create_node("Character", {"title": "霧雨魔理沙", "description": "東方Projectの主要キャラクター"})
    neo4j_manager.create_node("Game", {"title": "東方紅魔郷", "release_year": 2002})
    
    # リレーションシップの作成
    neo4j_manager.create_relationship(
        {"label": "Character", "title": "霧雨魔理沙"},
        {"label": "Game", "title": "東方紅魔郷"},
        "APPEARS_IN"
    )
    
    neo4j_manager.close()
    print("テストデータをNeo4jに追加しました。")

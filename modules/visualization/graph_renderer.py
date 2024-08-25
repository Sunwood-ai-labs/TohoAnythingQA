from modules.graph_rag.neo4j_manager import Neo4jManager
import json
import os

def prepare_graph_data(neo4j_manager: Neo4jManager):
    """
    Neo4jからデータを取得し、react-force-graphで使用可能な形式に変換します。

    :param neo4j_manager: Neo4jManagerのインスタンス
    :return: react-force-graphで使用可能なJSON文字列
    """
    with neo4j_manager.driver.session() as session:
        result = session.run("""
        MATCH (n)
        OPTIONAL MATCH (n)-[r]->(m)
        RETURN collect(distinct {id: id(n), label: labels(n)[0], title: n.title}) as nodes,
               collect(distinct {source: id(n), target: id(m), type: type(r)}) as links
        """)
        
        graph_data = result.single()
        
        return json.dumps({
            "nodes": graph_data["nodes"],
            "links": graph_data["links"]
        })

def save_graph_data(graph_data: str, filename: str):
    """
    グラフデータをJSONファイルとして保存します。

    :param graph_data: 保存するグラフデータ（JSON文字列）
    :param filename: 保存するファイル名
    """
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(graph_data)

if __name__ == "__main__":
    neo4j_manager = Neo4jManager("bolt://localhost:7687", "neo4j", "your_password")
    graph_json = prepare_graph_data(neo4j_manager)
    save_graph_data(graph_json, "graph_data.json")
    neo4j_manager.close()
    print("グラフデータを保存しました。")

from modules.graph_rag.neo4j_manager import Neo4jManager
from typing import List, Dict
import json
import os

def load_processed_data(filename: str) -> List[Dict]:
    """
    処理済みデータをJSONファイルから読み込みます。

    :param filename: 読み込むファイル名
    :return: 処理済みデータのリスト
    """
    input_path = os.path.join("data/processed", filename)
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_graph(neo4j_manager: Neo4jManager, data: List[Dict]):
    """
    クリーンアップされたデータを使用してNeo4jにグラフを構築します。

    :param neo4j_manager: Neo4jManagerのインスタンス
    :param data: クリーンアップされたデータのリスト
    """
    for item in data:
        # 'Article'ノードの作成
        neo4j_manager.create_node("Article", {
            "title": item["title"],
            "content": item["content"],
            "source": item["source"],
            "lang": item["lang"]
        })

        # 簡単な関係性の例（実際のプロジェクトではより複雑になる可能性があります）
        if "東方Project" in item["content"]:
            neo4j_manager.create_relationship(
                {"label": "Article", "title": item["title"]},
                {"label": "Article", "title": "東方Project"},
                "RELATED_TO"
            )

if __name__ == "__main__":
    neo4j_manager = Neo4jManager("bolt://localhost:7687", "neo4j", "your_password")
    processed_data = load_processed_data("processed_toho_data.json")
    build_graph(neo4j_manager, processed_data)
    neo4j_manager.close()
    print("グラフをNeo4jに構築しました。")

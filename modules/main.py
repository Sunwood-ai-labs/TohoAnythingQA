from data_extraction.wiki_scraper import fetch_wiki_data
from data_extraction.data_cleaner import clean_wiki_data, save_processed_data
from graph_rag.neo4j_manager import Neo4jManager
from graph_rag.graph_builder import build_graph
from visualization.graph_renderer import prepare_graph_data, save_graph_data

def main():
    # Wikipediaからデータを取得
    topic = "東方Project"
    wiki_docs = fetch_wiki_data(topic)
    print(f"{topic}に関する{len(wiki_docs)}件のドキュメントを取得しました。")

    # データをクリーンアップし、保存
    cleaned_data = clean_wiki_data(wiki_docs)
    save_processed_data(cleaned_data, "processed_toho_data.json")
    print("処理済みデータを保存しました。")

    # Neo4jにグラフを構築
    neo4j_manager = Neo4jManager("bolt://localhost:7687", "neo4j", "your_password")
    build_graph(neo4j_manager, cleaned_data)
    print("グラフをNeo4jに構築しました。")

    # 可視化用のデータを準備し、保存
    graph_json = prepare_graph_data(neo4j_manager)
    save_graph_data(graph_json, "graph_data.json")
    print("グラフデータを保存しました。")

    neo4j_manager.close()

if __name__ == "__main__":
    main()

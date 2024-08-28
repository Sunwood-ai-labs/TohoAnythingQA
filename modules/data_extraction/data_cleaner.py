from langchain.schema import Document
from typing import List, Dict
import json
import os

def clean_wiki_data(documents: List[Document]) -> List[Dict]:
    """
    Wikipediaから取得したドキュメントをクリーンアップし、
    Neo4jに適した形式に変換します。

    :param documents: WikipediaLoaderから取得したDocumentオブジェクトのリスト
    :return: Neo4jに挿入可能な辞書のリスト
    """
    cleaned_data = []
    for doc in documents:
        cleaned_doc = {
            "title": doc.metadata["title"],
            "content": doc.page_content,
            "source": doc.metadata.get("source", ""),
            "lang": doc.metadata.get("language", "ja")
        }
        cleaned_data.append(cleaned_doc)
    return cleaned_data

def save_processed_data(data: List[Dict], filename: str):
    """
    処理済みデータをJSONファイルとして保存します。

    :param data: 保存するデータ
    :param filename: 保存するファイル名
    """
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # テスト用のダミーデータ
    dummy_docs = [
        Document(page_content="東方Projectの内容...", metadata={"title": "東方Project", "source": "Wikipedia"}),
        Document(page_content="霧雨魔理沙の説明...", metadata={"title": "霧雨魔理沙", "source": "Wikipedia"})
    ]
    cleaned = clean_wiki_data(dummy_docs)
    save_processed_data(cleaned, "processed_toho_data.json")
    print("処理済みデータを保存しました。")

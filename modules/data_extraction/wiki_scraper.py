from langchain.document_loaders import WikipediaLoader
from typing import List
from langchain.schema import Document

def fetch_wiki_data(topic: str, lang: str = "ja") -> List[Document]:
    """
    指定されたトピックに関するWikipediaの情報を取得します。

    :param topic: 検索するトピック
    :param lang: 言語コード（デフォルトは日本語）
    :return: Documentオブジェクトのリスト
    """
    loader = WikipediaLoader(topic, lang=lang)
    documents = loader.load()
    return documents

if __name__ == "__main__":
    topic = "東方Project"
    docs = fetch_wiki_data(topic)
    print(f"{topic}に関する{len(docs)}件のドキュメントを取得しました。")
    for doc in docs:
        print(f"タイトル: {doc.metadata['title']}")
        print(f"内容の一部: {doc.page_content[:100]}...")
        print("-" * 50)

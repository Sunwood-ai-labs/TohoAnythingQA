import os
from langchain_community.document_loaders import WikipediaLoader
from typing import List
from langchain.schema import Document
from loguru import logger
import wikipedia

def fetch_wiki_data(topic: str, lang: str = "ja") -> List[Document]:
    """
    指定されたトピックに関するWikipediaの情報を取得します。

    :param topic: 検索するトピック
    :param lang: 言語コード（デフォルトは日本語）
    :return: Documentオブジェクトのリスト
    """
    logger.info(f"トピック '{topic}' の Wikipedia データを取得中...")
    wikipedia.set_lang(lang)
    
    loader = WikipediaLoader(
        query=topic,
        lang=lang,
        load_max_docs=2,
        doc_content_chars_max=100000  # Noneの代わりに大きな整数値を使用
    )
    
    try:
        documents = loader.load()
    except Exception as e:
        logger.error(f"WikipediaLoaderでエラーが発生しました: {e}")
        documents = []

    if not documents:
        try:
            page = wikipedia.page(topic)
            documents = [Document(page_content=page.content, metadata={"title": page.title})]
        except wikipedia.exceptions.DisambiguationError as e:
            logger.warning(f"曖昧さ回避ページです。候補: {e.options}")
            return []
        except wikipedia.exceptions.PageError:
            logger.warning(f"ページが見つかりません: {topic}")
            return []
    
    logger.info(f"{len(documents)} 件のドキュメントを取得しました。")
    return documents

def save_documents(documents: List[Document], topic: str):
    """
    取得したドキュメントを個別のテキストファイルとして保存します。

    :param documents: 保存するドキュメントのリスト
    :param topic: トピック名（ファイル名の一部として使用）
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_dir = os.path.join(root_dir, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    
    for i, doc in enumerate(documents):
        safe_topic = topic.replace(" ", "_").replace("/", "_")
        safe_title = doc.metadata['title'].replace(" ", "_").replace("/", "_")
        file_name = f"{safe_topic}_{safe_title}.txt"
        file_path = os.path.join(raw_dir, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"タイトル: {doc.metadata['title']}\n\n")
            f.write(doc.page_content)
        logger.info(f"ドキュメントを保存しました: {file_path}")

if __name__ == "__main__":
    
    topic = "東方地霊殿"
    # topic = "東方紅魔館"
    logger.info(f"プログラムを開始: トピック '{topic}'")
    
    docs = fetch_wiki_data(topic)
    
    if docs:
        logger.info(f"{topic}に関する{len(docs)}件のドキュメントを取得しました。")
        save_documents(docs, topic)
        
        for i, doc in enumerate(docs):
            logger.info(f"ドキュメント {i+1}:")
            logger.info(f"  タイトル: {doc.metadata['title']}")
            logger.info(f"  内容の一部: {doc.page_content[:100]}...")
            logger.info("-" * 50)
    else:
        logger.warning(f"{topic}に関するドキュメントを取得できませんでした。")
    
    logger.info("プログラムが正常に終了しました。")

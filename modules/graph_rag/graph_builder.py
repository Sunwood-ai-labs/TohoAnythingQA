import os
from typing import List
from dotenv import load_dotenv
from loguru import logger
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_community.graphs import Neo4jGraph

# .envファイルを読み込む
load_dotenv()

# loguruの基本設定
logger.add("graph_builder.log", rotation="10 MB")

def process_txt_file(filename: str) -> List[Document]:
    """
    指定されたtxtファイルを処理し、Documentオブジェクトのリストに変換します。
    """
    logger.info(f"Processing txt file: {filename}")
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)

    documents = [Document(page_content=chunk, metadata={"source": filename, "chunk_id": i})
                 for i, chunk in enumerate(chunks, start=1)]
    
    logger.info(f"Processed {len(documents)} chunks from {filename}")
    return documents

def build_graph(documents: List[Document]):
    """
    DocumentオブジェクトのリストからNeo4jにグラフを構築します。
    """
    logger.info("Starting graph building process")

    model_name = "gpt-4o-2024-08-06"
    # model_name = "gpt-4o-mini"
    llm = ChatOpenAI(temperature=0, model_name=model_name)
    llm_transformer = LLMGraphTransformer(
        llm=llm,
        allowed_nodes=[
            "Character", "Location", "Item", "Ability", "Game", "Event", "Species", "Organization"
        ],
        allowed_relationships=[
            "APPEARS_IN", "LIVES_IN", "OWNS", "HAS_ABILITY", "RELATED_TO", "PART_OF",
            "OCCURS_IN", "BELONGS_TO", "CREATED_BY", "FRIENDS_WITH", "ENEMIES_WITH"
        ],
        node_properties=[
            "name", "description", "first_appearance", "species", "occupation", "abilities"
        ]
    )

    graph = Neo4jGraph()

    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    graph.add_graph_documents(graph_documents)

    logger.info(f"Processed {len(graph_documents)} documents and added to Neo4j")
    logger.info("Graph building completed successfully")

if __name__ == "__main__":
    # 環境変数の設定（.envファイルから読み込まれる）
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_username = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # 環境変数が正しく設定されているか確認
    if not all([neo4j_uri, neo4j_username, neo4j_password, openai_api_key]):
        logger.error("必要な環境変数が設定されていません。.envファイルを確認してください。")
        exit(1)

    # OpenAI APIキーの設定
    os.environ['OPENAI_API_KEY'] = openai_api_key

    # data\rawディレクトリ内の全てのtxtファイルを取得
    raw_data_dir = r"data\raw"
    txt_files = [f for f in os.listdir(raw_data_dir) if f.endswith('.txt')]

    all_documents = []

    # 各txtファイルを処理
    for txt_file in txt_files:
        file_path = os.path.join(raw_data_dir, txt_file)
        logger.info(f"Starting process with file: {file_path}")
        
        documents = process_txt_file(file_path)
        all_documents.extend(documents)
    
    # 全てのドキュメントを使ってグラフを構築
    build_graph(all_documents)
    
    logger.info("Graph building process completed successfully for all files.")

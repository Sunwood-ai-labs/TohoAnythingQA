from loguru import logger
import json
import sys

def convert_neo4j_to_react_force_graph(input_file, output_file):
    logger.info("変換処理を開始します")
    new_data = {"nodes": [], "links": []}
    node_id_map = {}  # Neo4j IDと連番IDの対応表

    logger.info(f"{input_file} を読み込みます")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        json_objects = content.split('}\n{')
        logger.info(f"{len(json_objects)}個のJSONオブジェクトを検出しました")

        for i, obj in enumerate(json_objects):
            if i > 0:
                obj = '{' + obj
            if i < len(json_objects) - 1:
                obj = obj + '}'

            try:
                item = json.loads(obj)
                logger.debug(f"オブジェクト {i+1} を処理中")
                process_item(item, new_data, node_id_map)
            except json.JSONDecodeError as e:
                logger.warning(f"JSONオブジェクトの解析エラー: {e}")
                logger.warning(f"問題のあるオブジェクト: {obj[:100]}...")

    logger.info(f"変換結果を {output_file} に書き込みます")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)

def process_item(item, new_data, node_id_map):
    if isinstance(item, dict):
        if item.get("type") == "node":
            logger.debug("ノードを処理中")
            neo4j_id = item["properties"].get("id", item.get("id"))
            if neo4j_id not in node_id_map:
                node_id_map[neo4j_id] = len(node_id_map)
            new_node = {
                "id": str(node_id_map[neo4j_id]),
                "user": item.get("labels", [""])[0],
                "description": item.get("properties", {}).get("name", "")
            }
            new_data["nodes"].append(new_node)
            logger.debug(f"新しいノードを追加: {new_node['id']}")
        elif item.get("type") == "relationship":
            logger.debug("リレーションシップを処理中")
            start_neo4j_id = item.get("start").get("properties").get("id", item.get("start").get("id"))
            end_neo4j_id = item.get("end").get("properties").get("id", item.get("end").get("id"))
            if start_neo4j_id in node_id_map and end_neo4j_id in node_id_map:
                new_link = {
                    "source": str(node_id_map[start_neo4j_id]),
                    "target": str(node_id_map[end_neo4j_id]),
                }
                new_data["links"].append(new_link)
                logger.debug(f"新しいリンクを追加: {new_link['source']} -> {new_link['target']}")

if __name__ == "__main__":
    input_file = "neo4j_import/all.json"
    output_file = "neo4j_import/neo4j_blocks.json"
    
    logger.info("プログラムを開始します")
    convert_neo4j_to_react_force_graph(input_file, output_file)
    logger.success(f"変換が完了しました。出力は {output_file} に書き込まれました")

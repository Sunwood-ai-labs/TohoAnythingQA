<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/TohoAnythingQA.png" width="100%">
<br>
<h1 align="center">TohoAnythingQA</h1>
<h2 align="center">
  ～ 東方Projectの知識グラフを探索する ～
<br>
  <img alt="GitHub" src="https://img.shields.io/github/license/Sunwood-ai-labs/TohoAnythingQA">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Sunwood-ai-labs/TohoAnythingQA">
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/Sunwood-ai-labs/TohoAnythingQA">
  <img alt="GitHub stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/TohoAnythingQA">
</h2>
</p>

## 🌟 はじめに

**TohoAnythingQA**は、東方Project専用の質問応答システムです。このプロジェクトは、東方ProjectのWiki情報を基に、Graph RAGとLLMを用いて構築された知識グラフを活用し、ユーザーの質問に答えることを目的としています。

## 🚀 特徴

- 東方Project関連の広範な知識を網羅
- Neo4jを使用した効率的な知識グラフ
- 美しい3Dグラフ可視化
- LLMを活用した高度な質問応答機能

## 📦 インストール

1. リポジトリをクローンします：
```bash
git clone https://github.com/Sunwood-ai-labs/TohoAnythingQA.git
```

2. 必要な依存関係をインストールします：
```bash
poetry install
```

3. Neo4jをセットアップします：
```bash
docker-compose up -d
```

4. 環境変数を設定します：
`.env`ファイルを作成し、必要な環境変数を設定してください。

## 🖥 使用方法

1. データの抽出と前処理：
```bash
python -m modules.data_extraction.wiki_scraper
```

2. グラフの構築：
```bash
python -m modules.graph_rag.graph_builder
```

3. サーバーの起動：
```bash
python server.py
```

4. ブラウザで`http://localhost:8000/visual/index_neo4j.html`を開いて、グラフを可視化します。

## 🛠 プロジェクト構造

```bash
TohoAnythingQA/
├─ modules/
│  ├─ data_extraction/
│  ├─ graph_rag/
│  ├─ visualization/
│  └─ main.py
├─ visual/
├─ docker-compose.yml
├─ pyproject.toml
├─ README.md
└─ server.py
```

## 🤝 コントリビューション

プロジェクトへの貢献を歓迎します！以下の方法で貢献できます：

1. Issueを作成して、バグの報告や新機能の提案をする
2. プルリクエストを送信して、コードの改善や新機能の追加を行う

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 🙏 謝辞

- 東方Projectの作者である[ZUN](https://thwiki.cc/ZUN)氏に感謝します。
- このプロジェクトは[ウィキペディア](https://ja.wikipedia.org/wiki/)の情報を活用しています。
- グラフ可視化には[ForceGraph3D](https://github.com/vasturiano/3d-force-graph)を使用しています。

## 📞 お問い合わせ

質問や提案がある場合は、[Issueを作成](https://github.com/Sunwood-ai-labs/TohoAnythingQA/issues/new)してください。

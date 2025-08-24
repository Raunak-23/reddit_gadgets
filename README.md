[README.md](https://github.com/user-attachments/files/21915765/README.md)
# Reddit r/gadgets Discussion Analytics

This project provides an **end-to-end analytics pipeline** for high-engagement discussions in [r/gadgets](https://www.reddit.com/r/gadgets). It collects Reddit threads (20+ comments), processes them into structured CSVs, and generates **insights at both the thread and global level**—including sentiment, topic modeling, n-grams, entities, and participation stats.

---

## 🚀 Features

- **Reddit Data Collection**  
  Fetches r/gadgets threads with **20+ comments** via the Reddit API.
  
- **Context-Aware Discussion Text**  
  Rebuilds comments with parent text for better sentiment/topic accuracy.
  
- **Sentiment Analysis**  
  Batched Transformers pipeline with safe truncation (512 tokens).
  
- **Topic Modeling**  
  LDA with short **human-readable labels** (tiny T5/heuristic).
  
- **N-grams**  
  Frequent bigrams & trigrams per discussion.
  
- **Named Entity Recognition (NER)** *(optional)*  
  Extracts and aggregates named entities (brands, products, places, etc.).
  
- **Thread Stats**  
  Posts vs. comments, unique authors, depth, word counts.
  
- **Outputs**
  - Per-thread enhanced CSVs  
  - Global summary rollup  
  - Compact dashboard-ready CSV  

---

## 📂 Repository Structure

```
notebooks/
  01_pre_processing.ipynb
  02_absa_inference.ipynb
  03_finetune_stub.ipynb
  feature_extraction1.ipynb
  sentiment_analysis.ipynb

Scripts/
  enhanced_thread_insights.py   # Main analysis pipeline
  reddit_fetcher.py             # Data collection (Reddit API)

data/
  processed/
    clean_csv/                  # Input: one CSV per thread
    senti_output/               # Output: per-thread + global summary

notebooks/checkpoints, notebooks/data, notebooks/src  # aux files
.gitignore
pyvenv.cfg
README.md
```

---

## 📝 Example Outputs

- **Per-thread insights**  
  e.g. `1ggjfl9_enhanced_insights.csv`  
  Includes sentiment %, topics, n-grams, and entities for one discussion.

- **Global rollup**  
  `global_summary.csv` → thread-level summary with sentiment distribution, topic snippets, and one-line summaries.

- **Dashboard summary**  
  `enhanced_summary.csv` → compact CSV for visualization tools.

---

## ⚡ Quick Start

### 1) Prerequisites
- Python **3.10+** (3.11 recommended)
- A Reddit API app (for fetching data)  
  - Requires `client_id`, `client_secret`, and `user_agent`

### 2) Install

```bash
pip install -U pip
pip install pandas numpy scikit-learn nltk tqdm transformers
```

On first run, the script will download:
- NLTK stopwords  
- Transformer models (cached after first use)

### 3) Fetch Data (optional)

If you don’t already have CSVs:

1. Add Reddit credentials via `.env` or environment variables  
2. Run:

```bash
python Scripts/reddit_fetcher.py
```

Writes one CSV per thread to:

```
data/processed/clean_csv/
```

Schema (flexible, typical columns):  
`id, parent_id, type (post/comment), body, author, depth, title, created_utc, score`

### 4) Run Analysis

Edit paths in `Scripts/enhanced_thread_insights.py` if needed:

```python
INPUT_FOLDER = "data/processed/clean_csv"
OUTPUT_FOLDER = "data/processed/senti_output"
```

Then:

```bash
python Scripts/enhanced_thread_insights.py
```

Outputs:
- Per-thread CSVs → `{thread_id}_enhanced_insights.csv`  
- Global rollup → `global_summary.csv`

---

## ⚙️ Configuration

Key knobs in `enhanced_thread_insights.py`:

| Parameter          | Default | Description |
|--------------------|---------|-------------|
| `NUM_TOPICS`       | 6       | # of LDA topics per thread |
| `NUM_TOPIC_WORDS`  | 8       | Keywords per topic |
| `USE_NER`          | True    | Enable/disable NER |
| `BATCH_SIZE`       | 32      | Sentiment batch size |
| `MIN_DOC_FOR_LDA`  | 2       | Minimum docs to run LDA |
| `INPUT_FOLDER`     | ...     | CSV input path |
| `OUTPUT_FOLDER`    | ...     | Output path |

---

## 🧩 Roadmap

- Aspect-Based Sentiment Analysis (ABSA) for brands/products  
- Cross-thread rollups & leaderboards  
- Time-series trend tracking  
- Streamlit/Gradio dashboard  
- CLI/config loader  
- SQLite/Parquet outputs  

---

## 🛠 Troubleshooting

- **UnicodeDecodeError on CSV**  
  Script retries with `utf-8` and `latin-1`. If it fails, the file may be malformed.

- **“after pruning, no terms remain” in LDA**  
  Text set too small. Lower `min_df` or skip topics.

- **CUDA/Torch warnings**  
  Runs on CPU if no GPU is available.

- **Long texts crash pipeline**  
  Already truncated to **512 tokens** for stability.

---

## 👥 Contributors

This project was developed collaboratively as part of a two-member team:

- [Raunak-23](https://github.com/Raunak-23)  
  *-Led the project with responsibilities including end-to-end Reddit data collection (via Reddit API), repository organization, and overall pipeline management.*  
  *-Implemented the core sentiment analysis workflow using Transformers and conducted extensive model training/experimentation.*  
  *-Developed topic modeling (LDA with labeling), participation statistics, and utilities for per-thread/global rollups.*  
  *-Extracted n-grams and entities (brands, products) to enhance downstream insights.*  

- [Swayam-Swaroop-Sahu](https://github.com/Swayam-Swaroop-Sahu)  
  *-Contributed in designing and implementing sentiment classification (positive/negative/neutral) and topic modeling (LDA) to uncover key discussion themes.*  
  *-Engineered preprocessing pipelines, conducted model experimentation, and generated structured, dashboard-ready CSVs for downstream analysis.*  
  *-Extracted n-grams and entities (brands, products) as part of the opinion-mining process.*  
  *-Contributed in finalizing sentiment modeling and opinion analysis workflows, delivering actionable, product-specific insights.*

Contributions welcome! Ideas:  
- Better cleaning/tokenization  
- Improved topic labeling  
- Entity normalization  
- Dashboard integrations
---

## 🙌 Credits
Reddit API  
pandas, scikit-learn, NLTK, tqdm  
Hugging Face Transformers

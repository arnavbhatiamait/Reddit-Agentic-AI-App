# 📊 Reddit Profile Analyzer 🧠

A **Streamlit-powered web application** that extracts a Reddit user's profile, posts, and comments, and generates a **detailed persona** analysis using **Groq's LLaMA 3.3 70B Versatile LLM**.

It provides a markdown report (~2000 words) analyzing their behavior, interests, personality, subreddit activity, and more.

[Demo Video](https://youtu.be/XSev2oUbmpc)

![Reddit](https://upload.wikimedia.org/wikipedia/en/thumb/b/bd/Reddit_Logo_Icon.svg/1024px-Reddit_Logo_Icon.svg.png)

---

## 🚀 Features

- 🔍 Scrapes Reddit profile info, recent posts, and comments using **PRAW**
- 🧠 Uses **Groq's LLaMA-3.3-70B** model via `langchain_groq` for persona generation
- 📄 Outputs results in **markdown format** including:
  - Personality traits
  - Daily routine
  - Work preferences
  - Top skills and weaknesses
- 💾 Saves both `.md` and `.txt` reports locally
- 🎨 User-friendly UI with **Streamlit**

---

## 🔧 Environment Variables

Create a `.env` file in the root directory and define the following:

```env
REDDIT_1=your_reddit_client_id
REDDIT_2=your_reddit_client_secret
GROQ_API_KEY=your_groq_api_key
````

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/reddit-profile-analyzer.git
cd reddit-profile-analyzer
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```txt
streamlit
praw
langchain
langchain-groq
langchain-core
langchain-community
python-dotenv
```

> ✅ You can also use `pip install -U -r requirements.txt` to upgrade packages.

### 3. Add `.env` File

```bash
touch .env
```

Paste your credentials:

```env
REDDIT_1=your_reddit_client_id
REDDIT_2=your_reddit_client_secret
GROQ_API_KEY=your_groq_api_key
```

> 🔐 Never share your `.env` file publicly.

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Then open your browser at:
[http://localhost:8501](http://localhost:8501)

---

## 🛠 How It Works

1. **Input**: You paste a Reddit profile URL (e.g., `https://www.reddit.com/user/Hungry-Move-6603/`)
2. **Scraping**: App uses `PRAW` to fetch:

   * Profile data
   * Latest 20 posts
   * Latest 20 comments
3. **Prompting**: A structured markdown-style prompt is generated using the scraped data
4. **LLM Call**: `langchain_groq` calls the LLaMA 3.3 70B Versatile model
5. **Output**: Detailed markdown is displayed and saved as `.md` and `.txt`

---

## 📂 Output Example

* `response_Hungry-Move-6603.md`
* `response_Hungry-Move-6603.txt`

Each report includes:

* Profile summary
* Personality analysis
* Tech affinity
* Routine and habits
* Subreddit activity
* Skills and weaknesses

---

## 🧠 Model Info

Using **Groq’s ultra-fast LLaMA 3.3 70B Versatile** via `langchain_groq`:

```python
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq)
```

You can optionally switch to:

```python
# ChatGroq(model="llama-3.1-8b-instant", api_key=groq)
```

---

## 💡 Example Reddit URLs

Try these:

```txt
https://www.reddit.com/user/kojied/
https://www.reddit.com/user/Hungry-Move-6603/
```


---

## 🧑‍💻 Author

**Arnav Bhatia**
🔗 [GitHub](https://github.com/arnavbhatia) | 🌐 [Hugging Face Space](https://huggingface.co/spaces/Arnavbhatia)

---



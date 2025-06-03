# 🕷️ Product URL Crawler

This Python project crawls multiple e-commerce websites (e.g., Virgio, Nykaa Fashion, Westside, TataCliq) to extract **product page URLs** and save them into **Excel files**. It uses **Selenium** (headless Chrome) and **BeautifulSoup** for scraping and includes a rotating logging system.

---

## 📌 Features

- Headless Chrome browser automation using Selenium
- Product URL identification using keyword-based heuristics
- Recursively crawls internal links up to a page limit
- Saves results to `.xlsx` Excel files
- Logs activity to both the terminal and `logs/crawler.log`

---

## ⚙️ Setup Instructions

Follow these steps to install and run the crawler on your machine.

### 1. Clone the repository

```bash
git clone https://github.com/mihir26061/Web_Crawler.git
```


### 2. Create a virtual environment

```bash
python -m venv my_env
```

### 3. Activate the virtual environment
- On Windows:

    ```bash
    my_env\Scripts\activate
    ```
- On macOS/Linux:

    ```bash
    source my_env/bin/activate
    ```

### 4. Install required dependencies

```bash
pip install -r requirements.txt
```

# 🚀 Run the Crawler
```bash
python crawler.py
```
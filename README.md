🚀 AI-Powered Web Scraper and Parser
🔍 A dynamic web scraping and parsing framework using Streamlit, Selenium, BeautifulSoup, and LangChain with Ollama.

✨ Features
🌐 Scrape Websites: Enter any URL to scrape and extract meaningful body content automatically.

🧹 Clean Content: Strips out unnecessary scripts and styles to focus only on the relevant information.

✨ Parse with AI (Ollama): Describe what you want to extract, and the AI model intelligently parses the content accordingly.

📄 Smart Chunking: Large content is automatically split into manageable pieces before parsing to ensure performance and accuracy.

⚙️ Tech Stack
Streamlit

Selenium

BeautifulSoup

LangChain

Ollama LLM

🚀 How to Run
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/ai-web-scraper.git
cd ai-web-scraper
2. Install Dependencies
Make sure you have Python 3.10+ installed.
Then install the required libraries:

bash
Copy
Edit
pip install -r requirements.txt
(You might need to install chromedriver separately. Download here).

3. Set Up ChromeDriver
Download the compatible version of ChromeDriver.

Update the path in scrape.py if needed:

python
Copy
Edit
service = Service('path/to/your/chromedriver')
4. Install Ollama and Models
Install Ollama from here.

Make sure to have a model like llama3 running locally or via API.

5. Start the Streamlit App
bash
Copy
Edit
streamlit run main.py
🛠 Usage
Open the app (Streamlit will automatically open it in your browser).

Enter the website URL you want to scrape.

Click Scrape Website.

View the extracted DOM content.

Write a prompt/description to define what you want to parse.

Click Parse Content — AI will extract and present only the relevant data.

📈 Future Enhancements
Handle multi-page website scraping

Add export options (CSV, JSON)

Build-in proxy support for restricted websites

Support multiple LLMs


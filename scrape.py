from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

def scrape_website(url):
    print("Launching Chrome browser...")
    service = Service('/Users/akanksha/Downloads/AI-Web-Scraper-main/chromedriver')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    try:
        print("Navigating to the website...")
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        html = driver.page_source
        print("Page content scraped successfully.")
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]

def extract_links(html_content, base_url):
    """Extract all links from the HTML content and convert to absolute URLs"""
    soup = BeautifulSoup(html_content, "html.parser")
    parsed_base = urlparse(base_url)
    base_domain = parsed_base.netloc
    
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Convert relative URLs to absolute
        absolute_url = urljoin(base_url, href)
        parsed_url = urlparse(absolute_url)
        
        # Only include links from the same domain and skip anchors
        if parsed_url.netloc == base_domain and not parsed_url.path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip')):
            if '#' in absolute_url:
                absolute_url = absolute_url.split('#')[0]
            if absolute_url not in links and absolute_url != base_url:
                links.append(absolute_url)
    
    return links

def scrape_with_subpages(main_url, max_depth=1):
    """Scrape main page and its subpages up to a certain depth with no page limit"""
    visited = set()
    to_visit = [(main_url, 0)]  # (url, depth)
    results = {}
    page_count = 0
    
    service = Service('/Users/akanksha/Downloads/AI-Web-Scraper-main/chromedriver')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        while to_visit:
            current_url, depth = to_visit.pop(0)
            
            if current_url in visited:
                continue
                
            visited.add(current_url)
            page_count += 1
            print(f"Scraping page #{page_count}: {current_url}")
            
            try:
                driver.get(current_url)
                time.sleep(2)  # Allow time for JavaScript to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                html = driver.page_source
                
                # Process the current page
                body_content = extract_body_content(html)
                cleaned_content = clean_body_content(body_content)
                results[current_url] = cleaned_content
                
                # Find subpage links if we haven't reached max depth
                if depth < max_depth:
                    subpage_links = extract_links(html, current_url)
                    for link in subpage_links:
                        if link not in visited:
                            to_visit.append((link, depth + 1))
            
            except Exception as e:
                print(f"Error scraping {current_url}: {e}")
                
    finally:
        driver.quit()
        
    return results

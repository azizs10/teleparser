import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_target_site(url: str, keyword_string: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    parsed_items = []
    
    keywords = [k.strip().lower() for k in keyword_string.split(",") if k.strip()]
    
    articles = soup.find_all("article", class_="product_pod")
    if not articles:
        articles = soup.find_all(["div", "section"], class_=["product", "item", "card"])

    for article in articles:
        text_content = article.get_text().lower()
        
        match_found = any(keyword in text_content for keyword in keywords)
        
        if match_found:
            title_el = article.find(["h3", "h4", "h2", "span", "a"])
            title = title_el.get_text(strip=True) if title_el else "Unknown Product"
            
            price_el = article.find(class_=["price_color", "price", "amount"])
            price = price_el.get_text(strip=True) if price_el else "Price not found"
            
            link_el = article.find("a")
            link = urljoin(url, link_el["href"]) if link_el and link_el.has_attr("href") else url
            
            item_key = f"{link}_{price}"
            
            parsed_items.append({
                "key": item_key,
                "title": title,
                "price": price,
                "link": link
            })
            
    return parsed_items
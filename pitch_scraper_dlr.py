"""
DLR Pitches Scraper
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timezone

def scrape_dlr_pitches():
    url = "https://www.dlrcoco.ie/pitches"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; DLR-PitchScraper/2.0)'}
    
    response = requests.get(url, headers=headers, timeout=15)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pitches = []
    
    popup_elements = soup.find_all('div', class_='map-popup')
    
    for popup in popup_elements:
        name_elem = popup.find('div', class_='map-popup-rhs-name')
        name = name_elem.get_text().strip() if name_elem else "Unknown Pitch"
        
        status_elem = popup.find('div', class_='map-popup-rhs-type')
        status_text = status_elem.get_text().strip().lower() if status_elem else "unknown"
        is_playable = status_text == "playable"
        
        pitches.append({
            "name": name,
            "status": status_text,
            "playable": is_playable,
            "Council": "DLR"
        })
    
    data = {
        "scrape_time": datetime.now(timezone.utc).isoformat(),
        "council": "DLR",
        "pitches": pitches
    }
    
    playable_count = len([p for p in pitches if p["playable"]])
    total_count = len(pitches)
    print(f"Exported {playable_count}/{total_count} playable DLR pitches")
    return data

def main():
    result = scrape_dlr_pitches()
    
    os.makedirs('data', exist_ok=True)
    
    with open('data/dlr_pitches.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("✓ Exported to data/dlr_pitches.json")

if __name__ == "__main__":
    main()

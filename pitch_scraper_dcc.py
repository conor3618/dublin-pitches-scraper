"""
Dublin City Council Pitch Playability Scraper
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import os

DCC_URL = "https://www.dublincity.ie/residential/parks/dublin-city-parks/pitch-playability"

def scrape_dcc_pitches():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    r = requests.get(DCC_URL, headers=headers, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Extract date from <p><strong>Latest updated ...</strong></p>
    date_paras = soup.find_all('p')
    last_updated = "Unknown"
    for para in date_paras:
        para_text = para.get_text(strip=True)
        if 'Latest updated' in para_text or 'Last updated' in para_text:
            last_updated = para_text
            break
    
    pitches = []
    table = soup.find("table")
    
    for row in table.find_all("tr")[1:]:  # Skip header
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols and cols[0]:  # Has park name
            name = cols[0]
            status_on = cols[1] if len(cols) > 1 else ""
            status_off = cols[2] if len(cols) > 2 else ""
            status = status_on if status_on else status_off
            playable = "ON" in status_on
            
            pitches.append({
                "name": name,
                "status": status,
                "playable": playable,
                "Council": "DCC"
            })
    
    data = {
        "scrape_time": datetime.now(timezone.utc).isoformat(),
        "council": "DCC",
        "pitches": pitches
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/dcc_pitches.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return pitches

def print_dcc_statuses(pitches):
    playable = sum(1 for p in pitches if p["playable"])
    print("DUBLIN CITY COUNCIL PITCHES:")
    print(f"PLAYABLE: {playable}/{len(pitches)}\n")
    
    for p in pitches:
        status = "Playable" if p["playable"] else "Unplayable"
        print(f"{p['name']} : {status}")

if __name__ == "__main__":
    pitches = scrape_dcc_pitches()
    print_dcc_statuses(pitches)
    print("\n✓ Data exported to data/dcc_pitches.json")

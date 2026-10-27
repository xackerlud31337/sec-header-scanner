import sys
import requests
import json

def main():
    if len(sys.argv) != 2:
            sys.exit("Usage: python project.py urls.txt")
    
    try:
        with open(sys.argv[1]) as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        sys.exit("File not found")
    
    results = []
    for url in urls:
        response = fetch(url)
        results.append({
            "url": url,
            "status": response.status_code,
            "headers": dict(response.headers),
            **checkheaders(response.headers)
        })    
    
    with open("report.json", "w") as file:
        json.dump(results, file, indent=4)
          
    print(f"Saved {len(results)} results to report.json!")
    
    
def fetch(url):
    return requests.get(url, timeout=5)


def checkheaders(headers):
    important = ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options", "X-Content-Type-Options"]
    leaky = ["Server", "X-Powered-By"]
    
    missing = []
    for name in important:
        if name not in headers:
            missing.append(name)
            
    leaks = []
    for name in leaky:
        if name in headers:
            leaks.append(f"{name}: {headers[name]}")
            
    return {"missing": missing, "leaks": leaks}
    
    
        
    
if __name__ == "__main__":
    main()
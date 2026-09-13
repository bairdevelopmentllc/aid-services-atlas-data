import os
import json

def generate_html():
    base_urls = {
        'https://www.usa.gov',
        'https://www.benefits.gov',
        'https://www.fema.gov',
        'https://www.virginia.gov'
    }
    extracted_urls = set(base_urls)
    
    target_folder = 'us' 
    files_processed = 0
    urls_found = 0

    print("--- Starting JSON Scan ---")

    for root, dirs, files in os.walk(target_folder):
        for file in files:
            if file.lower().endswith('.json'):
                filepath = os.path.join(root, file)
                
                # Skip 0-byte placeholder files
                if os.path.getsize(filepath) == 0:
                    continue
                    
                files_processed += 1
                try:
                    with open(filepath, 'r', encoding='utf-8-sig') as f:
                        data = json.load(f)
                        
                        # Look for the 'providers' array based on your schema
                        if isinstance(data, dict):
                            items = data.get('providers', [])
                        elif isinstance(data, list):
                            items = data
                        else:
                            items = []
                            
                        for item in items:
                            # Look for the 'website' key
                            if isinstance(item, dict) and 'website' in item and item['website']:
                                extracted_urls.add(item['website'])
                                urls_found += 1
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    print(f"Scan Complete: Processed {files_processed} JSON files and found {urls_found} local URLs.")

    sorted_urls = sorted(list(extracted_urls))

    list_items = ""
    for url in sorted_urls:
        list_items += f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a></li>\n'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Information Sources - Aid & Services Atlas</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; color: #333; }}
        h1 {{ color: #2c3e50; }}
        .disclaimer {{ background: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin-bottom: 20px; font-size: 0.95em; }}
        ul {{ word-wrap: break-word; line-height: 1.8; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Official Information Sources</h1>
    <div class="disclaimer">
        <strong>Disclaimer:</strong> Aid & Services Atlas is an independent, non-governmental directory. The links below represent the official government and nonprofit websites where our informational data is sourced. We are not affiliated with, endorsed by, or representing any government entity.
    </div>
    <p>The government-related information displayed in the Aid & Services Atlas application is derived directly from the following official public directories and municipal domains:</p>
    <ul>
{list_items}    </ul>
</body>
</html>"""

    with open('sources.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_html()

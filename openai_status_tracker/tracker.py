import urllib.request
import urllib.error
import json
import time
import sys
from datetime import datetime, timezone

STATUS_URL = "https://status.openai.com/api/v2/incidents.json"
CHECK_INTERVAL = 60  # Checks every 60 seconds

def fetch_incidents(last_etag=None, last_modified=None):
    """
    Fetches the incidents JSON efficiently using conditional GET headers.
    Returns: (data, new_etag, new_last_modified, status_code)
    """
    req = urllib.request.Request(STATUS_URL)
    req.add_header("User-Agent", "OpenAI-Status-Tracker/1.0")
    
    if last_etag:
        req.add_header("If-None-Match", last_etag)
    if last_modified:
        req.add_header("If-Modified-Since", last_modified)

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            new_etag = response.getheader("ETag")
            new_last_modified = response.getheader("Last-Modified")
            return data, new_etag, new_last_modified, 200
    except urllib.error.HTTPError as e:
        if e.code == 304:
            return None, last_etag, last_modified, 304
        else:
            print(f"Error fetching status: {e.code} {e.reason}", file=sys.stderr)
            return None, last_etag, last_modified, e.code
    except Exception as e:
        print(f"Connection error: {e}", file=sys.stderr)
        return None, last_etag, last_modified, 0

def parse_iso_time(iso_str):
    """Parses ISO 8601 time string to datetime object (UTC)."""
    if iso_str.endswith('Z'):
        iso_str = iso_str[:-1] + '+00:00'
    return datetime.fromisoformat(iso_str)

def main():
    print(f"Starting OpenAI Status Tracker...")
    print(f"Tracking: {STATUS_URL}")
    print("Press Ctrl+C to stop.\n")

    last_etag = None
    last_modified = None
    
    started_at = datetime.now(timezone.utc)
    processed_update_ids = set()

    data, last_etag, last_modified, code = fetch_incidents()
    
    if data:
        for incident in data.get("incidents", []):
            for update in incident.get("incident_updates", []):
                processed_update_ids.add(update["id"])
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Tracker Initialized. Waiting for updates...")
    
    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            
            data, new_etag, new_last_modified, code = fetch_incidents(last_etag, last_modified)
            
            if code == 304:
                continue
                
            if code == 200 and data:
                last_etag = new_etag
                last_modified = new_last_modified
                
                incidents = data.get("incidents", [])
                
                for incident in incidents:
                    incident_name = incident.get("name", "Unknown Issue")
                    
                    updates = incident.get("incident_updates", [])
                    for update in updates:
                        update_id = update.get("id")
                        if update_id not in processed_update_ids:
                            processed_update_ids.add(update_id)
                            
                            created_at_str = update.get("created_at")
                            created_at_dt = parse_iso_time(created_at_str)
                            
                            if created_at_dt > started_at:
                                status_text = update.get("status", "updated")
                                body = update.get("body", "")
                                
                                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                print(f"[{timestamp}] Product: {incident_name}")
                                print(f"Status: {status_text} - {body}")
                                print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nStopping tracker.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()

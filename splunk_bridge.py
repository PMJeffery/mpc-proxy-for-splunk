import sys
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
###
# Enter your Splunk IP or FQDN and Token within the Double-Quotes 
### 
URL = "https://YOUR-SPLUNK-IP-OR-FQDN:8089/services/mcp"
TOKEN = "YOUR-SPLUNK-TOKEN"

def main():
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    })

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            mcp_request = json.loads(line)
            response = session.post(URL, json=mcp_request, verify=False)

            if response.status_code == 200:
                resp_json = response.json()
                # Splunk MCP returns {"payload": ...} wrapper, unwrap it
                if isinstance(resp_json, dict) and "payload" in resp_json:
                    payload = resp_json["payload"]
                    if isinstance(payload, str):
                        print(payload, flush=True)
                    else:
                        print(json.dumps(payload), flush=True)
                else:
                    print(json.dumps(resp_json), flush=True)
            else:
                print(f"Error from Splunk: {response.status_code} - {response.text}", file=sys.stderr)
                # Return JSON-RPC error response with same id as request
                error_resp = {
                    "jsonrpc": "2.0",
                    "id": mcp_request.get("id"),
                    "error": {
                        "code": -32603,
                        "message": f"Splunk returned HTTP {response.status_code}: {response.text}"
                    }
                }
                print(json.dumps(error_resp), flush=True)
        except json.JSONDecodeError:
            continue
        except Exception as e:
            print(f"Bridge error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
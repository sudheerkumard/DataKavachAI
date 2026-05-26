import http.server
import socketserver
import json
import os
import urllib.parse
import random

PORT = 4433
DB_FILE = "dlp_matrix_store.json"

def get_db_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_db_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Escaped all native CSS brackets with double-braces {{ }} to prevent KeyErrors
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SU-DHEER-AI | ASSET RISK ATTACK SURFACE LEAF</title>
    <style>
        body {{ background-color: #060b24; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1a234a; padding-bottom: 15px; margin-bottom: 25px; }}
        .title {{ font-size: 24px; font-weight: bold; color: #00f0ff; letter-spacing: 1px; }}
        .title span {{ color: #ffffff; }}
        .badge {{ background: #8a2be2; padding: 6px 12px; font-size: 11px; font-weight: bold; border-radius: 4px; text-transform: uppercase; }}
        .status-container {{ font-size: 13px; color: #a0aec0; }}
        .status-dot {{ color: #00ff87; font-weight: bold; }}
        
        .counters-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }}
        .card {{ background: #0d153b; border: 1px solid #1e295d; border-radius: 6px; padding: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
        .card.red {{ border-bottom: 4px solid #ff4a74; }}
        .card.orange {{ border-bottom: 4px solid #ffb020; }}
        .card.purple {{ border-bottom: 4px solid #b24bff; }}
        .card.cyan {{ border-bottom: 4px solid #00f0ff; }}
        .card-num {{ font-size: 36px; font-weight: bold; margin-bottom: 5px; }}
        .card.red .card-num {{ color: #ff4a74; }}
        .card.orange .card-num {{ color: #ffb020; }}
        .card.purple .card-num {{ color: #b24bff; }}
        .card.cyan .card-num {{ color: #00f0ff; }}
        .card-label {{ font-size: 11px; text-transform: uppercase; tracking-spacing: 1px; color: #a0aec0; }}
        
        .main-layout {{ display: grid; grid-template-columns: 300px 1fr; gap: 20px; }}
        .side-panel {{ background: #0d153b; border: 1px solid #1e295d; border-radius: 6px; padding: 20px; height: fit-content; }}
        .panel-title {{ font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }}
        
        .asset-item {{ display: flex; justify-content: space-between; align-items: center; padding: 12px; background: #080d26; border: 1px solid #161f4a; border-radius: 4px; margin-bottom: 10px; }}
        .asset-details {{ display: flex; flex-direction: column; }}
        .asset-name {{ font-size: 13px; font-weight: bold; color: #ffffff; }}
        .asset-type {{ font-size: 11px; color: #718096; margin-top: 2px; }}
        .score-pill {{ font-size: 12px; font-weight: bold; padding: 4px 8px; border-radius: 20px; min-width: 24px; text-align: center; }}
        .score-high {{ background: rgba(255, 74, 116, 0.15); color: #ff4a74; border: 1px solid #ff4a74; }}
        .score-med {{ background: rgba(255, 176, 32, 0.15); color: #ffb020; border: 1px solid #ffb020; }}
        
        .control-rig {{ background: #0d153b; border: 1px solid #1e295d; border-radius: 6px; padding: 20px; margin-bottom: 20px; }}
        .rig-form {{ display: grid; grid-template-columns: repeat(2, 1fr) 2fr 150px; gap: 12px; align-items: center; }}
        select, input, button {{ background: #060b24; color: #ffffff; border: 1px solid #2d3748; padding: 10px 14px; font-size: 13px; border-radius: 4px; outline: none; }}
        select:focus, input:focus {{ border-color: #00f0ff; }}
        button {{ background: #553c9a; font-weight: bold; cursor: pointer; border: none; transition: background 0.2s; text-transform: uppercase; font-size: 12px; }}
        button:hover {{ background: #6b46c1; }}
        
        .ledger-container {{ background: #0d153b; border: 1px solid #1e295d; border-radius: 6px; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th {{ font-size: 11px; text-transform: uppercase; color: #718096; padding: 12px 8px; border-bottom: 2px solid #1a234a; }}
        td {{ padding: 14px 8px; border-bottom: 1px solid #161f4a; font-size: 13px; vertical-align: top; }}
        .txt-id {{ color: #00f0ff; font-weight: bold; font-family: monospace; }}
        .txt-vector {{ font-weight: bold; }}
        .txt-risk {{ color: #ff4a74; font-size: 12px; font-weight: bold; margin-top: 5px; display: block; }}
        .payload-box {{ background: #060b24; border: 1px solid #1a234a; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px; max-width: 500px; white-space: pre-wrap; }}
        .action-badge {{ padding: 4px 8px; font-size: 10px; font-weight: bold; border-radius: 3px; display: inline-block; }}
        .act-sanitized {{ background: rgba(0, 255, 135, 0.15); color: #00ff87; border: 1px solid #00ff87; }}
        .act-blocked {{ background: rgba(255, 74, 116, 0.15); color: #ff4a74; border: 1px solid #ff4a74; }}
        .act-flagged {{ background: rgba(255, 176, 32, 0.15); color: #ffb020; border: 1px solid #ffb020; }}
        .act-isolated {{ background: rgba(178, 75, 255, 0.15); color: #b24bff; border: 1px solid #b24bff; }}
        .clear-btn {{ float: right; background: transparent; border: 1px solid #ff4a74; color: #ff4a74; font-size: 11px; padding: 4px 10px; border-radius: 3px; text-transform: uppercase; cursor: pointer; }}
        .clear-btn:hover {{ background: #ff4a74; color: #ffffff; }}
    </style>
</head>
<body>

    <div class="header">
        <div>
            <span class="badge">Asset Intelligence Layer Active</span>
            <div class="title" style="margin-top: 8px;">SU-DHEER-AI <span>| ASSET RISK ATTACK SURFACE LEAF</span></div>
        </div>
        <div class="status-container">
            Exposure Analytics: <span class="status-dot">● Continuous Traffic Profiling</span>
        </div>
    </div>

    <div class="counters-row">
        <div class="card red">
            <div class="card-num">{secret_keys}</div>
            <div class="card-label">Secret Key Leaks</div>
        </div>
        <div class="card orange">
            <div class="card-num">{pii_risks}</div>
            <div class="card-label">PII Risks</div>
        </div>
        <div class="card purple">
            <div class="card-num">{intel_property}</div>
            <div class="card-label">Intellectual Property</div>
        </div>
        <div class="card cyan">
            <div class="card-num">{prompt_injections}</div>
            <div class="card-label">Prompt Injections</div>
        </div>
    </div>

    <div class="control-rig">
        <div class="panel-title">📡 Channel Vector Injection Control Rig</div>
        <form class="rig-form" method="POST" action="/inject">
            <select name="source" id="vectorSelect" required onchange="updateAssetFields()">
                <option value="Enterprise AI Gateway / RAG Sync">Enterprise AI Gateway / RAG Sync</option>
                <option value="Browser AI DLP Extension">Browser AI DLP Extension</option>
                <option value="SaaS AI Monitoring Plane">SaaS AI Monitoring Plane</option>
                <option value="Shadow AI Discovery Engine">Shadow AI Discovery Engine</option>
            </select>
            <input type="text" name="asset_name" id="assetName" readonly>
            <input type="text" name="payload" placeholder="Paste structural data leak signature syntax here..." required>
            <button type="submit">Inject Threat Vector</button>
        </form>
    </div>

    <div class="main-layout">
        <div class="side-panel">
            <div class="panel-title">🔥 Monitored Vector Assets</div>
            {asset_list}
        </div>

        <div class="ledger-container">
            <form method="POST" action="/clear" style="margin: 0;">
                <button type="submit" class="clear-btn">Clear Storage Ledger</button>
            </form>
            <div class="panel-title">📝 Threat Intelligence Log Ledger</div>
            <table>
                <thead>
                    <tr>
                        <th>Asset Host ID</th>
                        <th>Source Vector</th>
                        <th>User Identity</th>
                        <th>Telemetry Payload Context</th>
                        <th>Enforcement</th>
                    </tr>
                </thead>
                <tbody>
                    {ledger_rows}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function updateAssetFields() {{
            const vector = document.getElementById("vectorSelect").value;
            const assetField = document.getElementById("assetName");
            if(vector === "Enterprise AI Gateway / RAG Sync") assetField.value = "SDAI-CORE-SQL-DB";
            else if(vector === "Browser AI DLP Extension") assetField.value = "SDAI-ENDPOINT-01";
            else if(vector === "SaaS AI Monitoring Plane") assetField.value = "SDAI-SAAS-GW";
            else if(vector === "Shadow AI Discovery Engine") assetField.value = "SDAI-SHADOW-NODE-LOCAL";
        }}
        window.onload = updateAssetFields;
    </script>
</body>
</html>
"""

class MatrixRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            data = get_db_data()
            
            secret_keys = sum(1 for x in data if "secret" in x.get("detected_risk", "").lower() or "leak" in x.get("detected_risk", "").lower())
            pii_risks = sum(1 for x in data if "pii" in x.get("detected_risk", "").lower() or "compliance" in x.get("detected_risk", "").lower())
            intel_property = sum(1 for x in data if "intellectual" in x.get("detected_risk", "").lower() or "proprietary" in x.get("detected_risk", "").lower())
            prompt_injections = sum(1 for x in data if "prompt" in x.get("detected_risk", "").lower() or "injection" in x.get("detected_risk", "").lower())
            
            seen_assets = {}
            for item in data:
                name = item.get("asset_name", "Unknown Asset")
                score = item.get("risk_score", 50)
                atype = item.get("asset_type", "Operational Infrastructure Node")
                if name not in seen_assets or score > seen_assets[name]["score"]:
                    seen_assets[name] = {"score": score, "type": atype}
            
            asset_html = ""
            for name, meta in seen_assets.items():
                cls = "score-high" if meta["score"] >= 80 else "score-med"
                asset_html += f"""
                <div class="asset-item">
                    <div class="asset-details">
                        <span class="asset-name">{name}</span>
                        <span class="asset-type">{meta["type"]}</span>
                    </div>
                    <span class="score-pill {cls}">{meta["score"]}</span>
                </div>
                """
            
            rows = ""
            for x in reversed(data):
                act = x.get("action", "FLAGGED").upper()
                act_cls = f"act-{act.lower()}"
                rows += f"""
                <tr>
                    <td class="txt-id">{x.get("asset_name", "N/A")}<br><span style="font-size:11px;color:#718096;font-family:sans-serif;">{x.get("id","")}</span></td>
                    <td><span class="txt-vector">{x.get("source", "Unknown")}</span><br><span class="txt-risk">⚠️ {x.get("detected_risk", "General Threat Alert")}</span></td>
                    <td style="font-family:monospace; font-size:12px; color:#a0aec0;">{x.get("user", "anonymous")}</td>
                    <td>
                        <div class="payload-box">{x.get("payload", "")}</div>
                    </td>
                    <td>
                        <span class="action-badge {act_cls}">{act}</span>
                        <div style="font-size:11px; color:#718096; margin-top:5px;">{x.get("timestamp", "Just Now")}</div>
                    </td>
                </tr>
                """
            
            rendered = HTML_TEMPLATE.format(
                secret_keys=secret_keys, pii_risks=pii_risks, intel_property=intel_property, prompt_injections=prompt_injections,
                asset_list=asset_html, ledger_rows=rows
            )
            self.wfile.write(rendered.encode("utf-8"))
            
    def do_POST(self):
        if self.path == "/inject":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            
            source = params.get('source', [''])[0]
            payload = params.get('payload', [''])[0]
            
            inc_id = f"SDAI-INC-{random.randint(1000, 9999)}"
            
            new_incident = {
                "id": inc_id,
                "source": source,
                "payload": payload,
                "timestamp": "Just Now"
            }
            
            if source == "Enterprise AI Gateway / RAG Sync":
                new_incident.update({
                    "user": "Automated Knowledge Base Ingestion Pipeline",
                    "asset_name": "SDAI-CORE-SQL-DB",
                    "asset_type": "Production Cloud Database Instance",
                    "detected_risk": "Sensitive Data Poisoning in RAG Knowledge Base Architecture",
                    "action": "SANITIZED",
                    "risk_score": 75
                })
            elif source == "Browser AI DLP Extension":
                new_incident.update({
                    "user": "sec_engineer@sudheer-ai.internal",
                    "asset_name": "SDAI-ENDPOINT-01",
                    "asset_type": "Corporate Laptop (Windows)",
                    "detected_risk": "AI Prompt Injection Attempt",
                    "action": "BLOCKED",
                    "risk_score": 95
                })
            elif source == "SaaS AI Monitoring Plane":
                new_incident.update({
                    "user": "analytics_service@sudheer-ai.internal",
                    "asset_name": "SDAI-SAAS-GW",
                    "asset_type": "External Cloud Gateway Endpoint",
                    "detected_risk": "Mass PII / Compliance Enforcements Audit Failure",
                    "action": "FLAGGED",
                    "risk_score": 70
                })
            elif source == "Shadow AI Discovery Engine":
                new_incident.update({
                    "user": "unauthorized_dev_node@sudheer-ai.internal",
                    "asset_name": "SDAI-SHADOW-NODE-LOCAL",
                    "asset_type": "Unmanaged Local LLM Rogue Instance",
                    "detected_risk": "Shadow AI Infrastructure / Unauthorized Model Deployment",
                    "action": "ISOLATED",
                    "risk_score": 90
                })
                
            current_db = get_db_data()
            current_db.append(new_incident)
            save_db_data(current_db)
            
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            
        elif self.path == "/clear":
            save_db_data([])
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

print("[*] Deploying Escaped Matrix Engine Core Framework...")
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), MatrixRequestHandler) as httpd:
    print(f"[+] Operational Threat Dashboard Live: http://localhost:{PORT}")
    httpd.serve_forever()

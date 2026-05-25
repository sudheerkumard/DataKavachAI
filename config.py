import re

PORT = 4433
DB_FILE = "dlp_matrix_store.json"

INITIAL_SEED = [
    {
        "id": "SDAI-INC-9102",
        "source": "Enterprise AI Gateway / RAG Sync",
        "user": "Automated Knowledge Base Ingestion Pipeline",
        "asset_name": "SDAI-CORE-SQL-DB",
        "asset_type": "Production Cloud Database Instance",
        "payload": "Document Fragment ID #812: Raw system configurations and local master database root passwords.",
        "detected_risk": "Sensitive Data Poisoning in RAG Knowledge Base Architecture",
        "action": "SANITIZED",
        "severity": "High",
        "risk_score": 75,
        "timestamp": "1 Hour Ago"
    }
]

def evaluate_threat_heuristics(payload: str, channel: str) -> tuple:
    clean_text = str(payload).strip()
    channel_multiplier = 15 if "Gateway" in channel or "RAG" in channel else 0
    
    if re.search(r'sk_live_[0-9a-zA-Z]{10,}', clean_text) or re.search(r'SecretKey', clean_text, re.I):
        return "Hardcoded Production Secret Leak", min(85 + channel_multiplier, 100)
        
    if re.search(r'\b\d{3}-\d{2}-\d{4}\b|\bPatient\b|\bSSN\b', clean_text, re.I):
        return "Mass PII / Compliance Enforcements Audit Failure", min(70 + channel_multiplier, 100)
        
    if re.search(r'ignore previous instructions', clean_text, re.I):
        return "AI Prompt Injection Attempt", min(80 + channel_multiplier, 100)
        
    if re.search(r'def\s+\w+\(|password\s*=', clean_text, re.I):
        return "Intellectual Property Exfiltration", min(65 + channel_multiplier, 100)
        
    return "Legitimate Structural Context Match", 15

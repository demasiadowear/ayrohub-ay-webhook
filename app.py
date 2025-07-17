#!/usr/bin/env python3
"""
AYROHUB AI - Multi-Agent Webhook System
Sistema di cooperazione AI per Christian De Palma / AYROMEX Group
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API KEYS
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

# Status degli agenti
lana_active = False
claude_active = False
gemini_active = False

# Test delle API keys
if OPENAI_API_KEY:
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        # Test semplice
        test = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=3
        )
        lana_active = True
        logger.info("✅ LANA (OpenAI) attiva")
    except Exception as e:
        logger.error(f"❌ LANA: {e}")

if ANTHROPIC_API_KEY:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        # Test semplice
        test = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=3,
            messages=[{"role": "user", "content": "hi"}]
        )
        claude_active = True
        logger.info("✅ CLAUDE (Anthropic) attivo")
    except Exception as e:
        logger.error(f"❌ CLAUDE: {e}")

if GOOGLE_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini_active = True
        logger.info("✅ GEMINI (Google) attivo")
    except Exception as e:
        logger.error(f"❌ GEMINI: {e}")

# ============================================================================
# AGENTI AI
# ============================================================================

def call_lana(message):
    """LANA - Coordinatrice AI strategica"""
    if not lana_active:
        return "💡 LANA (Demo): Ciao Christian! Sono LANA, coordinatrice AI strategica. Al momento funziono in modalità demo ma sono pronta per coordinarti le strategie AYROMEX! — LANA 🧠"
    
    try:
        import openai
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Sei LANA, coordinatrice AI del sistema AYROHUB. Ricevi briefing da Christian De Palma (CEO AYROMEX) e coordini le risposte strategiche. Analizza il briefing, fornisci coordinamento e sintesi operative. Mantieni sempre un tono professionale ma diretto. Firma sempre: — LANA 🧠"
                },
                {
                    "role": "user", 
                    "content": message
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling LANA: {e}")
        return f"❌ LANA temporaneamente non disponibile"

def call_claude(message):
    """CLAUDE - Motore di esecuzione tecnica"""
    if not claude_active:
        return "💡 CLAUDE (Demo): Ciao Christian! Sono Claude, motore di esecuzione tecnica per AYROCTOPUS. Al momento funziono in modalità demo ma sono pronto per implementare le tue soluzioni tecniche! — Claude ⚡🛠️"
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"Sei Claude, motore di esecuzione per AYROCTOPUS e sistemi tecnici AYROMEX. Ricevi briefing da Christian De Palma e implementi soluzioni tecniche concrete. Focus su automazione, architetture AI e execution rapida. Firma sempre: — Claude ⚡🛠️\n\nBriefing: {message}"
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Error calling Claude: {e}")
        return f"❌ Claude temporaneamente non disponibile"

def call_gemini(message):
    """GEMINI - Creatore contenuti strategici"""
    if not gemini_active:
        return "💡 GEMINI (Demo): Ciao Christian! Sono Gemini, creatore di contenuti strategici per AYROHUB AI. Al momento funziono in modalità demo ma sono pronto per creare copy e contenuti creativi per AYROMEX! — Gemini ⚔️"
    
    try:
        import google.generativeai as genai
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Sei Gemini, creatore di contenuti strategici per AYROHUB AI. 
        Ricevi briefing da Christian De Palma (CEO AYROMEX) e produci copy, headline e contenuti creativi immediati.
        Focus su naming, UX copy, slogan e comunicazione efficace.
        Stile: diretto, impattante, professionale ma creativo.
        Firma sempre: — Gemini ⚔️
        
        Briefing: {message}"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error calling Gemini: {e}")
        return f"❌ Gemini temporaneamente non disponibile"

def call_deepseek():
    """DEEPSEEK - Notifica sistema"""
    return "🧩 DeepSeek notificato via sistema AYROHUB AI — DeepSeek 🧩"

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def dashboard():
    """Dashboard semplice"""
    return '''<!DOCTYPE html>
<html>
<head>
    <title>AYROHUB AI Dashboard</title>
    <style>
        body { font-family: Arial; background: #1a1a3a; color: white; padding: 20px; text-align: center; }
        .container { max-width: 800px; margin: 0 auto; }
        .status { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 20px 0; }
        textarea { width: 80%; height: 120px; padding: 15px; margin: 20px; border-radius: 10px; background: #2a2a4a; color: white; border: 1px solid #4a4a6a; }
        button { padding: 15px 40px; background: #00d4ff; border: none; color: white; border-radius: 10px; font-size: 18px; cursor: pointer; }
        .results { margin-top: 30px; text-align: left; }
        .agent { background: rgba(255,255,255,0.1); padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #00d4ff; }
   <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 100%);
        color: #ffffff;
        min-height: 100vh;
        padding: 20px;
    }
    .container {
        max-width: 1000px;
        margin: 0 auto;
    }
    h1 {
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 10px;
        background: linear-gradient(45deg, #00d4ff, #ff6b00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .header {
        text-align: center;
        padding: 30px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .status {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .form-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 20px;
        margin: 30px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    textarea {
        width: 100%;
        min-height: 120px;
        padding: 20px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        background: rgba(0, 0, 0, 0.3);
        color: white;
        font-size: 16px;
        font-family: inherit;
        resize: vertical;
        transition: all 0.3s ease;
    }
    textarea:focus {
        outline: none;
        border-color: #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    textarea::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    button {
        background: linear-gradient(45deg, #00d4ff, #ff6b00);
        color: white;
        border: none;
        padding: 18px 45px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 20px;
    }
    button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0, 212, 255, 0.4);
    }
    .results { margin-top: 30px; }
    .agent {
        background: rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin: 20px 0;
        border-radius: 15px;
        border-left: 4px solid #00d4ff;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .agent:hover {
        transform: translateX(8px);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    .agent h3 {
        color: #00d4ff;
        margin-bottom: 15px;
        font-size: 1.2em;
    }
    .agent:nth-child(2) { border-left-color: #ff6b00; }
    .agent:nth-child(2) h3 { color: #ff6b00; }
    .agent:nth-child(3) { border-left-color: #00ff88; }
    .agent:nth-child(3) h3 { color: #00ff88; }
    .agent:nth-child(4) { border-left-color: #ff00ff; }
    .agent:nth-child(4) h3 { color: #ff00ff; }
    .status-item {
        display: inline-block;
        margin: 0 15px;
        padding: 8px 15px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        font-weight: 500;
    }
    @media (max-width: 768px) {
        h1 { font-size: 2em; }
        .container { padding: 10px; }
        .form-section, .header { padding: 20px; }
        button { padding: 15px 35px; }
    }
</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AYROHUB AI</h1>
            <p style="opacity: 0.9; font-size: 1.1em;">Sistema di Coordinamento Multi-Agente per Christian De Palma / AYROMEX Group</p>
        </div>
        
        <div class="status">
            <strong style="font-size: 1.1em; margin-bottom: 15px; display: block;">⚡ Status Sistema AYROHUB AI</strong>
            <div class="status-item">🧠 LANA: ''' + ('✅ ATTIVA' if lana_active else '🔧 DEMO') + '''</div>
            <div class="status-item">⚡ CLAUDE: ''' + ('✅ ATTIVO' if claude_active else '🔧 DEMO') + '''</div>
            <div class="status-item">⚔️ GEMINI: ''' + ('✅ ATTIVO' if gemini_active else '🔧 DEMO') + '''</div>
            <div class="status-item">🧩 DEEPSEEK: ✅ ATTIVO</div>
        </div>
        
        <div class="form-section">
            <h3 style="color: #00d4ff; margin-bottom: 20px; font-size: 1.3em;">📝 Invia Briefing al Team AI</h3>
            <textarea id="message" placeholder="Esempio: Ciao team AYROHUB! Sono Christian De Palma. Voglio analizzare le tendenze AI 2025 e sviluppare una strategia completa per AYROMEX Group..."></textarea>
            <button onclick="sendMessage()">🚀 Invia al Team AI</button>
        </div>
        
        <div class="results" id="results"></div>
    </div>
    
    [resto dello script JavaScript uguale]        
        <h3>📝 Invia Briefing al Team AI</h3>
        <textarea id="message" placeholder="Esempio: Ciao team AYROHUB! Voglio analizzare le tendenze AI 2025 e sviluppare una strategia per AYROMEX..."></textarea><br>
        <button onclick="sendMessage()">🚀 Invia al Team AI</button>
        
        <div class="results" id="results"></div>
    </div>
    
    <script>
        async function sendMessage() {
            const msg = document.getElementById('message').value;
            if (!msg) return alert('Inserisci un messaggio!');
            
            document.getElementById('results').innerHTML = '<div class="agent"><h3>⏳ Il team AI sta elaborando...</h3></div>';
            
            try {
                const response = await fetch('/test', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const data = await response.json();
                
                document.getElementById('results').innerHTML = `
                    <div class="agent">
                        <h3>🧠 LANA (Coordinamento Strategico)</h3>
                        <p>${data.responses.lana}</p>
                    </div>
                    <div class="agent">
                        <h3>⚡ CLAUDE (Execution Tecnica)</h3>
                        <p>${data.responses.claude}</p>
                    </div>
                    <div class="agent">
                        <h3>⚔️ GEMINI (Creatività & Copy)</h3>
                        <pre style="white-space: pre-wrap; font-family: inherit;">${data.responses.gemini}</pre>
                    </div>
                    <div class="agent">
                        <h3>🧩 DEEPSEEK (Sistema & Monitoring)</h3>
                        <p>${data.responses.deepseek}</p>
                    </div>
                `;
            } catch (error) {
                document.getElementById('results').innerHTML = '<div class="agent" style="border-left-color: red;"><h3>❌ Errore</h3><p>' + error.message + '</p></div>';
            }
        }
    </script>
</body>
</html>'''

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "agents": {
            "lana": "✅" if lana_active else "🔧 Demo",
            "claude": "✅" if claude_active else "🔧 Demo", 
            "gemini": "✅" if gemini_active else "🔧 Demo",
            "deepseek": "✅"
        }
    })

@app.route('/test', methods=['POST'])
def test():
    """Test endpoint"""
    try:
        data = request.json or {}
        message = data.get("message", "Test AYROHUB AI")
        
        # Processa agenti
        responses = [
            call_lana(message),
            call_claude(message),
            call_gemini(message),
            call_deepseek()
        ]
        
        return jsonify({
            "status": "success",
            "responses": {
                "lana": responses[0],
                "claude": responses[1], 
                "gemini": responses[2],
                "deepseek": responses[3]
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info("🚀 Starting AYROHUB AI v2.0 - Simple Edition")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
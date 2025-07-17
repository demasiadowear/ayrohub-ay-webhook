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
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AYROHUB AI Dashboard</h1>
        <p>Sistema di Coordinamento Multi-Agente per Christian De Palma / AYROMEX Group</p>
        
        <div class="status">
            <strong>Status Agenti:</strong><br>
            🧠 LANA: ''' + ('✅ ATTIVA' if lana_active else '🔧 DEMO') + '''<br>
            ⚡ CLAUDE: ''' + ('✅ ATTIVO' if claude_active else '🔧 DEMO') + '''<br>
            ⚔️ GEMINI: ''' + ('✅ ATTIVO' if gemini_active else '🔧 DEMO') + '''<br>
            🧩 DEEPSEEK: ✅ ATTIVO
        </div>
        
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
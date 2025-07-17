#!/usr/bin/env python3
"""
AYROHUB AI - Multi-Agent Webhook System
Sistema di cooperazione AI per Christian De Palma / AYROMEX Group
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify

# Carica variabili d'ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API KEYS - DA VARIABILI D'AMBIENTE
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

# Configurazione Clients
openai_client = None
anthropic_client = None
slack_client = None

# Inizializzazione sicura dei client
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info("OpenAI client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")

if ANTHROPIC_API_KEY:
    try:
        import anthropic
        anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        logger.info("Anthropic client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Anthropic client: {e}")

if GOOGLE_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        logger.info("Google AI configured successfully")
    except Exception as e:
        logger.error(f"Failed to configure Google AI: {e}")

if SLACK_BOT_TOKEN:
    try:
        from slack_sdk import WebClient
        slack_client = WebClient(token=SLACK_BOT_TOKEN)
        logger.info("Slack client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Slack client: {e}")

# ============================================================================
# AGENTI AI
# ============================================================================

def call_lana(message):
    """LANA - Coordinatrice AI strategica"""
    if not openai_client:
        return "💡 LANA (Demo): Ciao Christian! Sono LANA, coordinatrice AI strategica. Al momento funziono in modalità demo ma sono pronta per coordinarti le strategie AYROMEX! — LANA 🧠"
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
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
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling LANA: {e}")
        return f"❌ LANA temporaneamente non disponibile: {str(e)}"

def call_claude(message):
    """CLAUDE - Motore di esecuzione tecnica"""
    if not anthropic_client:
        return "💡 CLAUDE (Demo): Ciao Christian! Sono Claude, motore di esecuzione tecnica per AYROCTOPUS. Al momento funziono in modalità demo ma sono pronto per implementare le tue soluzioni tecniche! — Claude ⚡🛠️"
    
    try:
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
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
        return f"❌ Claude temporaneamente non disponibile: {str(e)}"

def call_gemini(message):
    """GEMINI - Creatore contenuti strategici"""
    if not GOOGLE_API_KEY:
        return "💡 GEMINI (Demo): Ciao Christian! Sono Gemini, creatore di contenuti strategici per AYROHUB AI. Al momento funziono in modalità demo ma sono pronto per creare copy e contenuti creativi per AYROMEX! — Gemini ⚔️"
    
    try:
        import google.generativeai as genai
        model = genai.GenerativeModel('gemini-1.5-pro')
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
        return f"❌ Gemini temporaneamente non disponibile: {str(e)}"

def call_deepseek():
    """DEEPSEEK - Notifica sistema"""
    return "🧩 DeepSeek notificato via sistema AYROHUB AI — DeepSeek 🧩"

# ============================================================================
# SISTEMA DI COORDINAMENTO
# ============================================================================

def process_agents_parallel(message):
    """Processa tutti gli agenti"""
    results = []
    
    # Esegui agenti in sequenza per semplicità
    results.append(call_lana(message))
    results.append(call_claude(message))
    results.append(call_gemini(message))
    results.append(call_deepseek())
    
    return results

def format_response(message, responses):
    """Formatta la risposta finale"""
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    formatted = f"""🤖 **AYROHUB AI - Risposte del Team**

📝 **Briefing**: {message}
⏰ **Timestamp**: {timestamp}

---

🧠 **LANA (Coordinamento):**
{responses[0] or "❌ Non disponibile"}

---

⚡ **CLAUDE (Execution):**
{responses[1] or "❌ Non disponibile"}

---

⚔️ **GEMINI (Creatività):**
{responses[2] or "❌ Non disponibile"}

---

🧩 **DEEPSEEK (Sistema):**
{responses[3] or "❌ Non disponibile"}

---
✅ **Processo AYROHUB AI completato**"""
    
    return formatted

# ============================================================================
# WEBHOOK ENDPOINTS
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Serve the dashboard"""
    try:
        with open('dashboard.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return jsonify({
            "service": "AYROHUB AI Multi-Agent System",
            "status": "🚀 OPERATIVO",
            "message": "Dashboard not found - API endpoints available",
            "endpoints": {
                "health": "/health",
                "test": "/test (POST)"
            }
        })
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "AYROHUB AI",
        "timestamp": datetime.now().isoformat(),
        "version": "1.2.0",
        "agents": {
            "lana": "✅" if openai_client else "🔧 Demo",
            "claude": "✅" if anthropic_client else "🔧 Demo", 
            "gemini": "✅" if GOOGLE_API_KEY else "🔧 Demo",
            "deepseek": "✅"
        }
    })

@app.route('/test', methods=['POST'])
def test_endpoint():
    """Endpoint di test per AYROHUB AI"""
    try:
        data = request.json or {}
        message = data.get("message", "Test AYROHUB AI - Sistema di coordinamento multi-agente per Christian De Palma")
        
        logger.info(f"Processing test message: {message[:100]}...")
        
        # Processa agenti
        responses = process_agents_parallel(message)
        
        # Formatta risposta
        formatted_response = format_response(message, responses)
        
        return jsonify({
            "status": "success",
            "message": message,
            "responses": {
                "lana": responses[0],
                "claude": responses[1], 
                "gemini": responses[2],
                "deepseek": responses[3]
            },
            "formatted": formatted_response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in test endpoint: {e}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info("🚀 Starting AYROHUB AI Webhook Service v1.2.0")
    logger.info("📍 Endpoints available:")
    logger.info("   - GET  / - Home")
    logger.info("   - GET  /health - Health check")
    logger.info("   - POST /test - Test endpoint")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
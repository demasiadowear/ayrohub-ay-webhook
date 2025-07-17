#!/usr/bin/env python3
"""
AYROHUB AI - Multi-Agent Webhook System
Sistema di cooperazione AI per Christian De Palma / AYROMEX Group
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from openai import OpenAI
import anthropic
import google.generativeai as genai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import concurrent.futures
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()

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

# Verifica che tutte le API keys siano presenti
required_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY', 'SLACK_BOT_TOKEN']
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    logger.error(f"Missing required environment variables: {missing_keys}")

# Configurazione Clients (solo se le chiavi esistono)
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
if ANTHROPIC_API_KEY:
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
if SLACK_BOT_TOKEN:
    slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Canali Slack
INPUT_CHANNEL = os.getenv('INPUT_CHANNEL', 'ayro-briefs')
OUTPUT_CHANNEL = os.getenv('OUTPUT_CHANNEL', 'ai-responses')

# ============================================================================
# AGENTI AI
# ============================================================================

def call_lana(message):
    """LANA - Coordinatrice AI strategica"""
    try:
        if not OPENAI_API_KEY:
            return "❌ OpenAI API Key non configurata"
            
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
            max_tokens=2000,
            timeout=30
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling LANA: {e}")
        return f"❌ LANA temporaneamente non disponibile: {str(e)}"

def call_claude(message):
    """CLAUDE - Motore di esecuzione tecnica"""
    try:
        if not ANTHROPIC_API_KEY:
            return "❌ Anthropic API Key non configurata"
            
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"Sei Claude, motore di esecuzione per AYROCTOPUS e sistemi tecnici AYROMEX. Ricevi briefing da Christian De Palma e implementi soluzioni tecniche concrete. Focus su automazione, architetture AI e execution rapida. Firma sempre: — Claude ⚡🛠️\n\nBriefing: {message}"
                }
            ],
            timeout=30
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Error calling Claude: {e}")
        return f"❌ Claude temporaneamente non disponibile: {str(e)}"

def call_gemini(message):
    """GEMINI - Creatore contenuti strategici"""
    try:
        if not GOOGLE_API_KEY:
            return "❌ Google API Key non configurata"
            
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
    """DEEPSEEK - Notifica sistema (placeholder)"""
    return "🧩 DeepSeek notificato via sistema AYROHUB AI — DeepSeek 🧩"

# ============================================================================
# SISTEMA SLACK
# ============================================================================

def send_to_slack(channel, message):
    """Invia messaggio a Slack"""
    try:
        if not SLACK_BOT_TOKEN:
            logger.error("Slack token not configured")
            return False
            
        response = slack_client.chat_postMessage(
            channel=f"#{channel}",
            text=message,
            unfurl_links=False,
            unfurl_media=False
        )
        logger.info(f"Message sent to #{channel}")
        return True
    except SlackApiError as e:
        logger.error(f"Error sending to Slack: {e}")
        return False

def process_agents_parallel(message):
    """Processa tutti gli agenti in parallelo usando ThreadPoolExecutor"""
    agents = [
        ('LANA', call_lana),
        ('CLAUDE', call_claude),
        ('GEMINI', call_gemini),
        ('DEEPSEEK', call_deepseek)
    ]
    
    results = [None] * 4
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {}
        
        for i, (name, agent_func) in enumerate(agents):
            if agent_func == call_deepseek:
                future = executor.submit(agent_func)
            else:
                future = executor.submit(agent_func, message)
            futures[future] = i
        
        for future in concurrent.futures.as_completed(futures, timeout=35):
            index = futures[future]
            try:
                results[index] = future.result()
            except Exception as e:
                logger.error(f"Agent {agents[index][0]} failed: {e}")
                results[index] = f"❌ Errore agente {agents[index][0]}: {str(e)}"
    
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

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "AYROHUB AI",
        "timestamp": datetime.now().isoformat(),
        "version": "1.1.0"
    })

@app.route('/test', methods=['POST'])
def test_endpoint():
    """Endpoint di test per AYROHUB AI"""
    try:
        data = request.json or {}
        message = data.get("message", "Test AYROHUB AI - Sistema di coordinamento multi-agente")
        
        logger.info(f"Test message: {message}")
        
        # Processa agenti
        responses = process_agents_parallel(message)
        
        # Formatta risposta
        formatted_response = format_response(message, responses)
        
        return jsonify({
            "status": "success",
            "message": message,
            "responses": responses,
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
    logger.info("🚀 Starting AYROHUB AI Webhook Service v1.1.0")
    logger.info("📍 Endpoints:")
    logger.info("   - GET  /health - Health check")
    logger.info("   - POST /test - Test endpoint")
    
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
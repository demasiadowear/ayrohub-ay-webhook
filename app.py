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

# Debug delle API keys
logger.info(f"OPENAI_API_KEY presente: {'✅' if OPENAI_API_KEY else '❌'}")
logger.info(f"ANTHROPIC_API_KEY presente: {'✅' if ANTHROPIC_API_KEY else '❌'}")
logger.info(f"GOOGLE_API_KEY presente: {'✅' if GOOGLE_API_KEY else '❌'}")

if OPENAI_API_KEY:
    logger.info(f"OPENAI_API_KEY inizia con: {OPENAI_API_KEY[:10]}...")
    
if ANTHROPIC_API_KEY:
    logger.info(f"ANTHROPIC_API_KEY inizia con: {ANTHROPIC_API_KEY[:10]}...")

# Configurazione Clients
openai_client = None
anthropic_client = None
slack_client = None

# Inizializzazione sicura dei client
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        logger.info(f"Attempting OpenAI initialization with key: {OPENAI_API_KEY[:20]}...")
        
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Test immediato con modello base
        logger.info("Testing OpenAI client with simple request...")
        test = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        logger.info("✅ OpenAI client initialized and tested successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
        logger.error(f"❌ Error type: {type(e).__name__}")
        openai_client = None
if ANTHROPIC_API_KEY:
    try:
        import anthropic
        anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        logger.info("✅ Anthropic client initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Anthropic client: {e}")
        anthropic_client = None

if GOOGLE_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        logger.info("✅ Google AI configured successfully")
    except Exception as e:
        logger.error(f"❌ Failed to configure Google AI: {e}")

if SLACK_BOT_TOKEN:
    try:
        from slack_sdk import WebClient
        slack_client = WebClient(token=SLACK_BOT_TOKEN)
        logger.info("✅ Slack client initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Slack client: {e}")

# Debug finale
logger.info(f"Final status - OpenAI client: {'✅' if openai_client else '❌'}")
logger.info(f"Final status - Anthropic client: {'✅' if anthropic_client else '❌'}")

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
            model="gpt-4o-mini",
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
    return '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AYROHUB AI - Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a3a 100%);
            color: #ffffff;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .header {
            text-align: center;
            padding: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #00d4ff, #ff6b00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .header p {
            opacity: 0.8;
            font-size: 1.1em;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        .status-bar {
            background: rgba(0, 212, 255, 0.1);
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            text-align: center;
        }
        .form-section {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        textarea {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            background: rgba(0, 0, 0, 0.3);
            color: #ffffff;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #00d4ff;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        }
        textarea::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }
        .btn {
            background: linear-gradient(45deg, #00d4ff, #ff6b00);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .responses {
            background: rgba(255, 255, 255, 0.05);
            padding: 30px;
            border-radius: 20px;
            display: none;
            backdrop-filter: blur(10px);
        }
        .agent {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            margin: 20px 0;
            border-radius: 15px;
            border-left: 4px solid #00d4ff;
            transition: all 0.3s ease;
        }
        .agent:hover {
            transform: translateX(5px);
            background: rgba(255, 255, 255, 0.15);
        }
        .agent h3 {
            margin-bottom: 15px;
            color: #00d4ff;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            margin: 20px 0;
        }
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top: 4px solid #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }
            .container {
                padding: 10px;
            }
            .form-section, .responses {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AYROHUB AI</h1>
            <p>Sistema di Coordinamento Multi-Agente per Christian De Palma / AYROMEX Group</p>
        </div>

        <div class="status-bar">
            <span style="color: #00ff88;">🟢 Sistema OPERATIVO</span> | 
            <span>🧠 LANA</span> | 
            <span>⚡ CLAUDE</span> | 
            <span>⚔️ GEMINI</span> | 
            <span>🧩 DEEPSEEK</span>
        </div>

        <div class="form-section">
            <h2 style="color: #00d4ff; margin-bottom: 20px;">📝 Invia Briefing al Team AI</h2>
            <form id="briefingForm">
                <textarea 
                    id="message" 
                    placeholder="Esempio: Ciao team AYROHUB! Voglio analizzare le tendenze AI 2025 e sviluppare una strategia per AYROMEX..."
                    required
                ></textarea>
                <br>
                <button type="submit" class="btn" id="sendBtn">🚀 Invia al Team AI</button>
            </form>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <h3>⏳ Il team AI sta elaborando il tuo briefing...</h3>
        </div>

        <div class="responses" id="responses">
            <h2 style="color: #ff6b00; margin-bottom: 25px;">💬 Risposte del Team AI</h2>
            <div id="responseContent"></div>
        </div>
    </div>

    <script>
        const form = document.getElementById('briefingForm');
        const loading = document.getElementById('loading');
        const responses = document.getElementById('responses');
        const responseContent = document.getElementById('responseContent');
        const sendBtn = document.getElementById('sendBtn');

        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const message = document.getElementById('message').value.trim();
            if (!message) return;

            // Show loading
            loading.style.display = 'block';
            responses.style.display = 'none';
            sendBtn.disabled = true;
            sendBtn.textContent = '⏳ Elaborando...';

            try {
                const response = await fetch('/test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });

                if (!response.ok) {
                    throw new Error('Errore di comunicazione con il server');
                }

                const data = await response.json();
                
                loading.style.display = 'none';
                
                const timestamp = new Date().toLocaleString('it-IT');
                
                responseContent.innerHTML = `
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-bottom: 25px; border-left: 4px solid #00d4ff;">
                        <strong>📝 Briefing:</strong> ${message}<br>
                        <strong>⏰ Timestamp:</strong> ${timestamp}
                    </div>

                    <div class="agent">
                        <h3>🧠 LANA (Coordinamento Strategico)</h3>
                        <p>${data.responses.lana || 'Non disponibile'}</p>
                    </div>

                    <div class="agent">
                        <h3>⚡ CLAUDE (Execution Tecnica)</h3>
                        <p>${data.responses.claude || 'Non disponibile'}</p>
                    </div>

                    <div class="agent">
                        <h3>⚔️ GEMINI (Creatività & Copy)</h3>
                        <pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">${data.responses.gemini || 'Non disponibile'}</pre>
                    </div>

                    <div class="agent">
                        <h3>🧩 DEEPSEEK (Sistema & Monitoring)</h3>
                        <p>${data.responses.deepseek || 'Non disponibile'}</p>
                    </div>

                    <div style="background: rgba(0,255,136,0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #00ff88; text-align: center; margin-top: 20px;">
                        ✅ <strong>Processo AYROHUB AI completato</strong>
                    </div>
                `;
                
                responses.style.display = 'block';
                responses.scrollIntoView({ behavior: 'smooth' });

            } catch (error) {
                loading.style.display = 'none';
                responseContent.innerHTML = `
                    <div style="background: rgba(255,0,0,0.1); padding: 20px; border-radius: 10px; border-left: 4px solid #ff6b6b; color: #ff6b6b;">
                        ❌ <strong>Errore:</strong> ${error.message}
                    </div>
                `;
                responses.style.display = 'block';
            } finally {
                sendBtn.disabled = false;
                sendBtn.textContent = '🚀 Invia al Team AI';
            }
        });

        // Auto-resize textarea
        const textarea = document.getElementById('message');
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    </script>
</body>
</html>'''

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
    logger.info("   - GET  / - Dashboard")
    logger.info("   - GET  /health - Health check")
    logger.info("   - POST /test - Test endpoint")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
import json
from flask import Flask, request, jsonify
import asyncio

# Inisialisasi Flask app
app = Flask(__name__)

# Konfigurasi token bot
BOT_TOKEN = os.getenv('BOT_TOKEN')


# Handler untuk perintah /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Halo! Bot serverless ini berjalan di Vercel!')

# Handler untuk pesan teks biasa
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Anda mengirim: {update.message.text}')

# Fungsi untuk memproses update
async def process_update(update_data):
    # Inisialisasi aplikasi
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Tambahkan handler
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Konversi data JSON menjadi objek Update
    update = Update.de_json(data=update_data, bot=application.bot)
    
    # Proses update
    await application.process_update(update)

# Loop event global
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@app.route('/api/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Ambil dan proses data update
        update_data = request.get_json()
        
        # Proses update menggunakan loop yang sudah ada alih-alih asyncio.run()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(process_update(update_data), loop=loop)
        loop.run_until_complete(future)
        
        return jsonify({"status": "ok"})
    
    return jsonify({"status": "error", "message": "Hanya menerima metode POST"})

@app.route('/api/webhook', methods=['GET'])
def index():
    return jsonify({
        "status": "active",
        "message": "Telegram webhook aktif. Gunakan metode POST untuk webhook.",
        "version": "1.0"
    })

# Handler untuk route utama
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "Bot Telegram aktif. Webhook tersedia di /api/webhook"
    })
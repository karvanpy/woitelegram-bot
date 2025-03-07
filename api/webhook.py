from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
import json
from http.server import BaseHTTPRequestHandler

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

# Handler untuk Vercel serverless function
class handler(BaseHTTPRequestHandler):
    async def do_POST_async(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update_data = json.loads(post_data.decode('utf-8'))
        
        await process_update(update_data)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
    
    def do_POST(self):
        import asyncio
        asyncio.run(self.do_POST_async())
        
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "active",
            "message": "Telegram webhook aktif. Gunakan metode POST untuk webhook."
        }).encode('utf-8'))
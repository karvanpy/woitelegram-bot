import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler

# Fungsi untuk menangani perintah /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Halo! Bot ini menggunakan webhook!')

# Fungsi untuk menangani pesan teks
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    await update.message.reply_text(f'Anda mengirim: {message_text}')

# Fungsi utama untuk menjalankan bot
async def main():
    # Gunakan token dari variabel lingkungan untuk keamanan
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '7923899587:AAEvh1gj_dCvxKyjRMdmubxZtP4LfIUh0QE')
    
    # URL lengkap untuk webhook (harus HTTPS)
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://woitelegram-bot-webhook.vercel.app/')
    
    # Port untuk webhook (biasanya 8443, 443, 80, 88)
    PORT = int(os.environ.get('PORT', '8443'))
    
    # Inisialisasi aplikasi
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Tambahkan handler
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Atur webhook
    await application.bot.set_webhook(url=WEBHOOK_URL)
    
    # Mulai webhook
    await application.run_webhook(
        listen='0.0.0.0',  # Atau IP server Anda
        port=PORT,
        url_path=BOT_TOKEN,  # Path webhook
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True,  # Opsional: abaikan update saat bot offline
        # secret_token='rahasia-token-anda',  # Opsional: token rahasia untuk autentikasi webhook
        certificate=None  # Opsional: jika menggunakan sertifikat self-signed
    )

if __name__ == '__main__':
    asyncio.run(main())
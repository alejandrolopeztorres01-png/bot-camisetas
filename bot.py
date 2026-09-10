import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Configurar el registro de eventos
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

TOKEN = '8744099373:AAGE8S07L_GjkqR2NBZ5MJaSe_7nzhUkQtY'
ADMIN_GROUP_ID = -5139678402

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! ¿Qué modelo de camiseta quieres pedir?")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ADMIN_GROUP_ID:
        return
    
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("Uso correcto: /responder ID_CLIENTE mensaje")
            return
        
        client_id = args[0]
        message_text = " ".join(args[1:])
        
        await context.bot.send_message(chat_id=client_id, text=f"Respuesta del admin: {message_text}")
        await update.message.reply_text("Mensaje enviado correctamente al cliente.")
    except Exception as e:
        await update.message.reply_text(f"Error al enviar el mensaje: {e}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("responder", responder))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), start))

    # Configuración de webhooks para Render
    PORT = int(os.environ.get("PORT", 10000))
    RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{RENDER_URL}/"
    )

if __name__ == '__main__':
    main()
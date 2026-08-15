import os
from dotenv import load_dotenv
load_dotenv()
import os
import re
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegramdan olingan linkni aniqlash
def detect_platform(url):
    """URL ni tekshirib, qaysi platformadan ekanligini aniqlaydi"""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'tiktok.com' in url:
        return 'tiktok'
    elif 'instagram.com' in url:
        return 'instagram'
    return None

# Video yuklab olish funksiyasi
def download_video(url, platform):
    """yt-dlp yordamida video yuklab oladi"""
    output_path = 'downloads'
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'best[ext=mp4]/best',
        'quiet': False,
        'no_warnings': False,
    }
    
    # TikTok uchun maxsus sozlamalar
    if platform == 'tiktok':
        ydl_opts['format'] = 'best'
    
    # Instagram uchun maxsus sozlamalar
    elif platform == 'instagram':
        ydl_opts['format'] = 'best'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename, info.get('title', 'Video')
    except Exception as e:
        logger.error(f"Yuklab olishda xatolik: {e}")
        return None, None

# /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot ishga tushganda xabar yuboradi"""
    welcome_message = """
🎥 *Universal Video Yuklovchi Botga Xush Kelibsiz!*

Men YouTube, TikTok va Instagram'dan videolarni yuklab olaman.

📝 *Qanday ishlatish:*
Shunchaki video linkini yuboring va men uni yuklab beraman!

✅ *Qo'llab-quvvatlanadigan platformalar:*
• YouTube (youtube.com, youtu.be)
• TikTok (tiktok.com)
• Instagram (instagram.com)

🚀 *Boshlash uchun link yuboring!*
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

# Link qabul qilish va video yuklab olish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi yuborgan linkni qayta ishlaydi"""
    url = update.message.text.strip()
    
    # Platformani aniqlash
    platform = detect_platform(url)
    
    if not platform:
        await update.message.reply_text(
            "❌ Link noto'g'ri yoki qo'llab-quvvatlanmaydi.\n"
            "Iltimos, YouTube, TikTok yoki Instagram linkini yuboring."
        )
        return
    
    # Jarayonni boshlash haqida xabar
    status_msg = await update.message.reply_text(
        f"⏳ {platform.title()}dan video yuklab olinmoqda...\n"
        "Iltimos, kuting..."
    )
    
    try:
        # Video yuklab olish
        filepath, title = download_video(url, platform)
        
        if filepath and os.path.exists(filepath):
            # Fayl hajmini tekshirish (Telegram limiti: 50MB)
            file_size = os.path.getsize(filepath)
            
            if file_size > 50 * 1024 * 1024:  # 50MB
                await status_msg.edit_text(
                    "❌ Video juda katta (>50MB).\n"
                    "Telegram orqali yuborib bo'lmaydi."
                )
                os.remove(filepath)
                return
            
            # Videoni yuklash jarayoni
            await status_msg.edit_text("📤 Video yuborilmoqda...")
            
            # Videoni yuborish
            with open(filepath, 'rb') as video:
                await update.message.reply_video(
                    video=video,
                    caption=f"✅ *{title}*\n\n🔗 Platform: {platform.title()}",
                    parse_mode='Markdown',
                    supports_streaming=True
                )
            
            # Status xabarini o'chirish
            await status_msg.delete()
            
            # Faylni o'chirish
            os.remove(filepath)
            
        else:
            await status_msg.edit_text(
                "❌ Video yuklab olinmadi.\n"
                "Iltimos, linkni tekshiring va qayta urinib ko'ring."
            )
    
    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")
        await status_msg.edit_text(
            "❌ Xatolik yuz berdi!\n"
            "Iltimos, keyinroq qayta urinib ko'ring."
        )

# Xatoliklarni tutish
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xatoliklarni loglaydi"""
    logger.error(f"Update {update} xatolikka sabab bo'ldi: {context.error}")

# Asosiy funksiya
def main():
    """Botni ishga tushiradi"""
    # Bot tokenini kiriting
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("❌ XATOLIK: Bot tokenini kiriting!")
        print("1. @BotFather ga boring")
        print("2. /newbot buyrug'ini yuboring")
        print("3. Bot nomini va username kiriting")
        print("4. Olingan tokenni kodga qo'shing")
        return
    
    # Application yaratish
    app = Application.builder().token(TOKEN).build()
    
    # Handlerlarni qo'shish
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    # Botni ishga tushirish
    print("✅ Bot ishga tushdi!")
    print("📱 Telegram'da botingizni toping va /start buyrug'ini yuboring")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
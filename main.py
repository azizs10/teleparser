import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN
from parser import parse_target_site
import database as db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class SetupStates(StatesGroup):
    waiting_for_url = State()
    waiting_for_keyword = State()

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await db.add_user(message.from_user.id)
    await message.answer(
        "Hello! I am your monitoring assistant.\n\n"
        "Please send me the website URL you want to monitor (e.g., https://books.toscrape.com/)"
    )
    await state.set_state(SetupStates.waiting_for_url)

@dp.message(SetupStates.waiting_for_url)
async def process_url(message: types.Message, state: FSMContext):
    input_text = message.text.strip()
    
    if not input_text.startswith("http"):
        await message.answer("Please send a valid URL starting with http:// or https://")
        return
        
    await state.update_data(url=input_text)
    await message.answer(
        "Great! Now enter your search keywords separated by commas.\n\n"
        "Example: laptop, ram, ssd"
    )
    await state.set_state(SetupStates.waiting_for_keyword)

@dp.message(SetupStates.waiting_for_keyword)
async def process_keyword(message: types.Message, state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    keyword = message.text.strip()
    
    await db.add_subscription(message.from_user.id, url, keyword)
    await message.answer(
        f"Setup completed successfully!\n\n"
        f"Website: {url}\n"
        f"Keywords: {keyword}\n\n"
        f"I will check this page regularly and send you a notification when any of these words match."
    )
    await state.clear()

async def check_updates_loop():
    while True:
        logging.info("Checking target updates...")
        subscriptions = await db.get_subscriptions()
        
        for user_id, url, keyword in subscriptions:
            items = parse_target_site(url, keyword)
            for item in items:
                if not await db.is_item_sent(item["key"]):
                    message_text = (
                        f"*Match Found!*\n\n"
                        f"*Product:* {item['title']}\n"
                        f"*Price:* {item['price']}\n"
                        f"[Go to Website]({item['link']})"
                    )
                    try:
                        await bot.send_message(chat_id=user_id, text=message_text, parse_mode="Markdown")
                        await db.save_sent_item(item["key"])
                    except Exception as e:
                        logging.error(f"Failed to notify user {user_id}: {e}")
        
        await asyncio.sleep(600)

async def main():
    await db.init_db()
    asyncio.create_task(check_updates_loop())
    logging.info("Bot is starting up...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
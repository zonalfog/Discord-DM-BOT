import discord
import asyncio
import threading
import sys

# --- KONFIGURATION ---
TOKEN = 'URTOKEN'
TARGET_USER_ID = URTARGETUSERID  # Die ID der Person
# ----------------------

class MyBot(discord.Client):
    def __init__(self):
        # Intents für Python 3.10 und discord.py 2.0+
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.target_user = None

    async def on_ready(self):
        print(f'--- Bot ist online als {self.user} ---')
        print(f'--- Du kannst jetzt in der PowerShell tippen und Enter drücken ---')
        try:
            self.target_user = await self.fetch_user(TARGET_USER_ID)
        except Exception as e:
            print(f"Fehler: Konnte User nicht finden: {e}")

    async def on_message(self, message):
        # Zeige Nachrichten der Zielperson in der PowerShell an
        if message.author.id == TARGET_USER_ID:
            print(f"\n[EMPFANGEN von {message.author}]: {message.content}")
            print("Deine Antwort: ", end="", flush=True)

    async def send_console_message(self, content):
        if self.target_user:
            try:
                await self.target_user.send(content)
                print(f"[GESENDET]: {content}")
            except Exception as e:
                print(f"[FEHLER]: Konnte Nachricht nicht senden: {e}")

# Funktion, die in der PowerShell auf deine Eingabe wartet
def console_input_thread(bot, loop):
    while True:
        # Liest deine Eingabe in der PowerShell
        reply = input("Deine Antwort: ")
        if reply.strip():
            # Übergibt die Nachricht an den Bot-Loop
            asyncio.run_coroutine_threadsafe(bot.send_console_message(reply), loop)

# Bot Instanz und Start
bot = MyBot()
loop = asyncio.get_event_loop()

# Thread starten, damit PowerShell-Input den Bot nicht blockiert
input_thread = threading.Thread(target=console_input_thread, args=(bot, loop), daemon=True)
input_thread.start()

try:
    bot.run(TOKEN)
except KeyboardInterrupt:
    print("Bot wird beendet...")
from discord import Intents, Game, Status, HTTPException
from discord.ext import commands
from keep_alive import keep_alive
import subprocess
from os import listdir, environ

Token = environ["Token"]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="kl!", intents=Intents.all(), help_command=None
        )

    async def setup_hook(self):
        keep_alive()
        for nm in listdir("commands"):
            if not nm.startswith(("_", ".")):
                n = f"commands.{nm[:-3] if nm.endswith('.py') else nm}"
                await bot.load_extension(n)
        await self.tree.sync()

    async def on_ready(self):
        synced = await self.tree.sync()
        gameo = Game(f"kl!help | {len(self.guilds)}サーバーで稼働中")
        await self.change_presence(status=Status.online, activity=gameo)
        print("起動完了")
        print("------------------------------------")
        print(f"ユーザーネーム&タグ: {self.user}")
        print(f"コマンドの数: {len(synced)}コマンド")
        print("------------------------------------")


bot = Bot()


try:
    bot.run(token=Token)
except HTTPException:
    print("Rate Limit")
    subprocess.call("kill 1")

import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
import subprocess

Token = os.environ["Token"]

from replit import db


def verify_db(key, data):
    db[f"verify_1_db_{key}"] = data


def verify_db_get(key):
    return db[f"verify_1_db_{key}"]


class Button1(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="認証", style=discord.ButtonStyle.primary, custom_id="verify_type_1"
        )


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="kl!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        synced = await self.tree.sync()
        gameo = discord.Game(f"kl!help | {len(self.guilds)}サーバーで稼働中")
        await self.change_presence(status=discord.Status.online, activity=gameo)
        print("起動完了")
        print("------------------------------------")
        print(f"ユーザーネーム&タグ: {self.user}")
        print(f"コマンドの数: {len(synced)}コマンド")
        print("------------------------------------")


bot = Bot()
bot.remove_command("help")


@bot.hybrid_command(
    name="serverinfo", with_app_command=True, description="サーバーの詳細を表示します。"
)
async def serverinfo(ctx: commands.Context):
    guild = ctx.message.guild
    roles = [role for role in guild.roles]
    text_channels = [text_channels for text_channels in guild.text_channels]
    embed = discord.Embed(
        title="サーバー詳細", timestamp=ctx.message.created_at, color=discord.Colour.purple()
    )
    embed.set_thumbnail(url=ctx.guild.icon)
    embed.add_field(name="チャンネル数", value=f"{len(text_channels)}")
    embed.add_field(name="ロール数", value=f"{len(roles)}")
    embed.add_field(name="サーバーブースター", value=guild.premium_subscription_count)
    embed.add_field(name="メンバー数", value=guild.member_count)
    embed.set_footer(text=f"実行者: {ctx.author} ", icon_url=ctx.author.avatar)
    await ctx.reply(embed=embed)


@bot.hybrid_command(name="help", description="コマンドの一覧を表示します。")
async def help(ctx: commands.Context):
    num = 0
    embed = discord.Embed(
        title="コマンド一覧", timestamp=ctx.message.created_at, color=discord.Colour.purple()
    )
    for command in bot.tree.walk_commands():
        num = num + 1
        if num > 24:
            embed.add_field(name=command.name, value=command.description)
        else:
            embed.add_field(name=command.name, value=command.description)
    embed.set_footer(text=f"実行者: {ctx.author} ", icon_url=ctx.author.avatar)
    await ctx.send(embed=embed)


@bot.listen(name="on_interaction")
async def verify_interaction_callback(i: discord.Interaction):
    if i.data.get("custom_id") == "verify_type_1":
        data = verify_db_get(int(i.message.id))
        await i.guild.get_member(i.user.id).add_roles(
            i.guild.get_role(int(data["role_id"]))
        )
        await i.response.send_message("ロールを付与しました。", ephemeral=True)
    else:
        return


@discord.app_commands.describe(name="パネルの名前", description="パネルの説明", role="付与するロール")
@bot.hybrid_command(name="clickverify", description="ワンクリック認証できます。")
async def clickverify(
    ctx: commands.Context, name: str, description: str, role: discord.Role
):
    buttonView = discord.ui.View(timeout=None)
    buttonView.add_item(Button1())

    msg = await bot.get_channel(ctx.channel.id).send(
        embed=discord.Embed(title=name, description=description).add_field(
            name="付与するロール", value=f"{role.mention}"
        ),
        view=buttonView,
    )
    verify_db(int(msg.id), {"msg_id": int(msg.id), "role_id": role.id})
    await ctx.send("パネルの生成が完了しました。", ephemeral=True)


keep_alive()


try:
    bot.run(token=Token)
except discord.HTTPException:
    print("Rate Limit")
    subprocess.call("kill 1")

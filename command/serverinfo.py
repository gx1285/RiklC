from discord.ext import commands
from discord import ButtonStyle, Color, ui, Embed
from replit import db


def verify_db(key, data):
    db[f"verify_1_db_{key}"] = data


def verify_db_get(key):
    return db[f"verify_1_db_{key}"]


class Button1(ui.Button):
    def __init__(self):
        super().__init__(
            label="認証", style=ButtonStyle.primary, custom_id="verify_type_1"
        )


class serverinfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(
        name="serverinfo", with_app_command=True, description="サーバーの詳細を表示します。"
    )
    async def serverinfo(self, ctx: commands.Context):
        guild = ctx.guild
        roles = [role for role in guild.roles]
        text_channel = [text_channels for text_channels in guild.text_channels]
        p = Color.purple()
        title = "サーバー詳細"
        embed = Embed(title=title, timestamp=ctx.message.created_at, color=p)
        embed.add_field(name="チャンネル数", value=f"{len(text_channel)}")
        embed.add_field(name="ロール数", value=f"{len(roles)}")
        embed.add_field(name="サーバーブースター", value=guild.premium_subscription_count)
        embed.add_field(name="メンバー数", value=guild.member_count)
        embed.set_thumbnail(url=ctx.guild.icon)
        if ctx.author.avatar is None:
            embed.set_footer(
                text=f"実行者: {ctx.author} ",
                icon_url=ctx.author.default_avatar,
            )
        else:
            embed.set_footer(
                text=f"実行者: {ctx.author} ",
                icon_url=ctx.author.avatar,
            )
        await ctx.reply(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(serverinfo(bot))

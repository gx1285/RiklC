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


class help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="help", description="コマンドの一覧を表示します。")
    async def help(self, ctx: commands.Context):
        num = 0
        embed = Embed(
            title="コマンド一覧", timestamp=ctx.message.created_at, color=Color.purple()
        )

        for command in self.bot.tree.walk_commands():
            num = num + 1
            if num > 24:
                embed.add_field(name=command.name, value=command.description)
            else:
                embed.add_field(name=command.name, value=command.description)
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
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(help(bot))

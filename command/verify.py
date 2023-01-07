from discord.ext import commands
from discord import ButtonStyle, Role, app_commands, ui, Embed
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


class verify(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.describe(name="パネルの名前", description="パネルの説明", role="付与するロール")
    @commands.hybrid_command(name="clickverify", description="ワンクリック認証できます。")
    async def clickverify(
        self, ctx: commands.Context, name: str, description: str, role: Role
    ):
        buttonView = ui.View(timeout=None)
        buttonView.add_item(Button1())

        msg = await self.bot.get_channel(ctx.channel.id).send(
            embed=Embed(title=name, description=description).add_field(
                name="付与するロール", value=f"{role.mention}"
            ),
            view=buttonView,
        )

        verify_db(int(msg.id), {"msg_id": int(msg.id), "role_id": role.id})
        await ctx.send("パネルの生成が完了しました。", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(verify(bot))

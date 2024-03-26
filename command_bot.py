import disnake
from disnake.ext import commands
from art import tprint
from time import sleep
from colorama import init
from colorama import Fore
import config_for_command_bot as cfg

init()
bot = commands.Bot(command_prefix="!",
                   help_command=None,
                   intents=disnake.Intents.all(),
                   activity=disnake.Game(name="тестовый сервер")
                   )


@bot.event
async def on_ready():
    print(Fore.GREEN + f"Бот {bot.user} готов к работе")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(cfg.GREETING_CHANNEL)
    role = disnake.utils.get(member.guild.roles, id=1154684084681977867)
    embed = disnake.Embed(
        title="Новый участник!",
        description=f"{member.mention}",
        color=0xffffff
    )

    await member.add_roles(role)
    await channel.send(embed=embed)

    print(Fore.LIGHTBLUE_EX + f"[НОВЫЙ ПОЛЬЗОВАТЕЛЬ] Пользователь {member.name} присоединяется к серверу")
    print(Fore.LIGHTGREEN_EX + f"[УСПЕХ] Роль {role.name} добавлена для пользователя {member.name}")


@bot.command()
async def verify(ctx, member: disnake.Member, reason="indefinite"):
    user_role = disnake.utils.get(ctx.guild.roles, id=1155140411455721603)
    if user_role not in ctx.author.roles:
        await ctx.send(f"{ctx.author.mention}, у вас должна быть соответствующая роль для использования этой команды")
        print(Fore.RED + f"[ОШИБКА] У пользователя {ctx.author.name} недостаточно прав")

    else:
        role = disnake.utils.get(member.guild.roles, name=reason)
        if role.id in list(cfg.ROLES.values()):
            delete_roles = []
            for new_role in member.roles:
                if new_role.id in cfg.ID_ROLES:
                    await member.remove_roles(new_role)
                    delete_roles.append(new_role.name)

            await member.add_roles(role)
            await ctx.send(f"Саппорт {ctx.author.mention} верифицировал пользователя {member.mention} как {role.name}")
            print(Fore.LIGHTGREEN_EX + f"[УСПЕХ] Роль {', '.join(delete_roles)} удалена для пользователя {member.name}")
            print(Fore.LIGHTGREEN_EX + f"[УСПЕХ] Роль {role.name} добавлена для пользователя {member.name} саппортом {ctx.author.name}")

        else:
            await ctx.send(f"{ctx.author.mention}, вы не можете выдать роль {role.name}")
            print(Fore.RED + f"[ОШИБКА] У пользователя {ctx.author.name} недостаточно прав, тобы выдать роль {role.name}")


if __name__ == "__main__":
    try:
        tprint("DISCORD   BOT")
        sleep(2)
        bot.run(cfg.TOKEN)
    except Exception as e:
        print(repr(e))
    finally:
        print(Fore.BLUE + "Бот завершил работу... З.ы. обращайтесь еще ;) ")

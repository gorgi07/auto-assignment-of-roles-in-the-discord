# -----------------------------------------------------------
# Бот для верификации новых пользователей саппортом
# на дискорд сервере, методом использования команды,
# и автоматической выдачи роли 'indefinite'.
#
# (C) Егорио, 2023 г.
# -----------------------------------------------------------

import discord
from discord import utils
from art import tprint
from time import sleep
from colorama import init
from colorama import Fore
import config


class MyClient(discord.Client):
    async def on_ready(self):
        print(Fore.GREEN + f"Вошёл как {self.user}!")

    async def on_raw_reaction_add(self, payload):
        emoji = ""
        if payload.message_id == config.POST_ID:
            channel = self.get_channel(payload.channel_id)  # получаем объект канала
            message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
            member = utils.get(message.guild.members,
                               id=payload.user_id)  # получаем объект пользователя который поставил реакцию

            try:
                emoji = str(payload.emoji)  # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=config.ROLES[emoji])  # объект выбранной роли (если есть)
                indefinite_role = utils.get(member.guild.roles, id=1154684084681977867)
                if len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER:
                    await member.add_roles(role)
                    print(Fore.LIGHTGREEN_EX + f"[УСПЕХ] Пользователю {member.display_name} предоставлена роль {role.name}")
                    if indefinite_role in member.roles:
                        await member.remove_roles(indefinite_role)
                        print(Fore.LIGHTGREEN_EX + f"[УСПЕХ] Роль {indefinite_role.name} удалена для пользователя {member.display_name}")
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print(Fore.RED + f"[ОШИБКА] Слишком много ролей для пользователя {member.display_name}")

            except KeyError as e:
                print(Fore.RED + f"[ОШИБКА] KeyError, роль для {emoji} не найдена")
            except Exception as e:
                print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        emoji = ""
        channel = self.get_channel(payload.channel_id)  # получаем объект канала
        message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
        member = utils.get(message.guild.members,
                           id=payload.user_id)  # получаем объект пользователя который поставил реакцию

        try:
            emoji = str(payload.emoji)  # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])  # объект выбранной роли (если есть)
            indefinite_role = utils.get(member.guild.roles, id=1154684084681977867)

            await member.remove_roles(role)
            print(Fore.LIGHTGREEN_EX + f"[УСПЕХ] Роль {role.name} удалена для пользователя {member.display_name}")

            await member.add_roles(indefinite_role)
            print(Fore.LIGHTGREEN_EX + f"[УСПЕХ] Роль {indefinite_role.name} добавлена для пользователя {member.display_name}")

        except KeyError as e:
            print(Fore.RED + f"[ОШИБКА] KeyError, роль для {emoji} не найдена")
        except Exception as e:
            print(repr(e))

    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, id=1154684084681977867)
        print(Fore.LIGHTBLUE_EX + f"[НОВЫЙ ПОЛЬЗОВАТЕЛЬ] пользователь {member.display_name} присоединяется к серверам")
        await member.add_roles(role)


if __name__ == "__main__":
    init()
    client = MyClient(intents=discord.Intents.all())
    tprint("Discord     Bot")
    sleep(1)

    try:
        client.run(config.TOKEN)
    except Exception as e:
        print(repr(e))
    finally:
        print(Fore.BLUE + "Бот завершил работу... З.ы. обращайтесь еще ;) ")


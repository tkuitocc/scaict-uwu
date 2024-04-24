# Standard imports
import json
import os
import random
# Third-party imports
import discord
from discord.ext import commands
# Local imports
from cog.core.sql import write
from cog.core.sql import read
from cog.core.sql import link_sql
from cog.core.sql import end

def get_channels(): # 取得特殊用途頻道的清單，這裡會用來判斷是否在簽到頻道簽到，否則不予受理

    with open(f"{os.getcwd()}/DataBase/server.config.json", "r", encoding = "utf-8") as file:
        return json.load(file)["SCAICT-alpha"]

stickers = get_channels()["stickers"]['logo']

class Game(commands.Cog):
    # User can use this command to play ✊-🤚-✌️ with the bot in the command channel
    @discord.slash_command(name = "rock_paper_scissors", description = "玩剪刀石頭布")
    # useser can choose ✊, 🤚, or ✌️ in their command
    async def rock_paper_scissors(
        self,
        interaction,
        choice: discord.Option(str, choices = [ "✊", "🤚", "✌️" ])
    ):
        if interaction.channel.id != get_channels()["channel"]["commandChannel"]:
            await interaction.response.send_message("這裡不是指令區喔")
            return
        user_id = interaction.user.id
        nickname = interaction.user
        connection, cursor = link_sql() # SQL 會話

        point = read(user_id, 'point', cursor)
        if point < 5:
            await interaction.response.send_message("你的電電點不足以玩這個遊戲")
            end(connection, cursor)
            return
        if choice not in [ "✊", "🤚", "✌️" ]:
            await interaction.response.send_message("請輸入正確的選擇")
            end(connection, cursor)
            return
        botChoice = random.choice(["✊", "🤚", "✌️"])
        # print(botChoice)
        game_outcomes = {
            ("✌️", "✊"): 5,
            ("✌️", "🤚"): -5,
            ("✊", "✌️"): -5,
            ("✊", "🤚"): 5,
            ("🤚", "✌️"): 5,
            ("🤚", "✊"): -5,
        }

        if bot_choice == choice:
            await interaction.response.send_message(
                content = f"我出{bot_choice}，平手。你還有{point}{stickers}")
        else:
            point += game_outcomes[(botChoice, choice)]
            result = "你贏了" if game_outcomes[(botChoice, choice)] > 0 else "你輸了"
            await interaction.response.send_message(content=f"我出{botChoice}，{result}，你還有{point}{stickers}")
            print(f"{userId},{nickName} Get {game_outcomes[(botChoice, choice)]} point by playing rock-paper-scissors")
        write(userId, 'point',point ,CURSOR)
        end(CONNECTION,CURSOR)
    @discord.slash_command(name="number_status", description="數數狀態")
    async def numberStatus(self, interaction):
        CONNECTION,CURSOR=linkSQL()#SQL 會話
        CURSOR.execute("SELECT seq FROM game")
        nowStatus=CURSOR.fetchone()[0]
        end(CONNECTION,CURSOR)
        embed = discord.Embed(
            title="現在數到",
            description=f"{nowStatus} (dec) 了，接下去吧!",
            color=0xff24cf,
            )
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Game(bot))

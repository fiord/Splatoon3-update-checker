# インストールした discord.py を読み込む
import discord
from discord.ext import tasks
from discord.app_commands import CommandTree
import requests
import datetime
import os

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.getenv("DISCORD_TOKEN")

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = CommandTree(self)
        self.channel = None
    
    async def on_ready(self):
        await self.tree.sync()
        print('ログインしました')

    async def get_page(self):
        url = 'https://support.nintendo.com/jp/switch/software_support/av5ja/index.html'
        response = requests.get(url)
        print(datetime.datetime.now(), response.text)
        if 'URL=./1010.html' not in response.text:
            return url
        else:
            return ''
    
    @tasks.loop(seconds=5)
    async def checkForUpdate(self):
        response = await self.get_page()
        if response != '':
            await self.channel.send(response)
            self.checkForUpdate.stop()

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = MyClient(intents=intents)

# コマンド
@client.tree.command(name="neko", description="ねこ")
async def neko(interaction: discord.Interaction):
    await interaction.response.send_message("にゃーん")

@client.tree.command(name="check_for_update", description="5秒ごとにアプデページをチェックして、更新があったら報告するよ")
async def check_for_update(interaction: discord.Interaction):
    if not client.checkForUpdate.is_running():
        client.channel = interaction.channel
        client.checkForUpdate.start()
        await interaction.response.send_message("check_for_updat start", ephemeral=True)
    else:
        await interaction.response.send_message("check_for_update already running", ephemeral=True)

@client.tree.command(name="stop_check", description="/check_for_updateを停止するよ")
async def stop_check(interaction: discord.Interaction):
    client.checkForUpdate.stop()
    await interaction.response.send_message("check_for_update stopped", ephemeral=True)

@client.tree.command(name="manual_check", description="アプデページを1回確認してくるよ")
async def manual_check(interaction: discord.Interaction):
    response = await client.get_page()
    if response == '':
        await interaction.response.send_message("まだ更新されていないみたい")
    else:
        await interaction.response.send_message(response)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

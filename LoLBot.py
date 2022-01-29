import os

from discord.ext import commands
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError


class LoLBot(commands.Cog):

    def __init__(self, bot: commands.Bot, RIOT_TOKEN):
        self.bot = bot
        self.lolwatcher = LolWatcher(RIOT_TOKEN)
        self.summoners = {}  # Dictionary to save linked summoners name.

    @commands.Cog.listener()
    async def on_ready(self):
        """Prints to console when the bot is connected"""

        print("Connected to server.")
        print(f"Logged in as: {self.bot.user}")

    @commands.command(name="linksummoner")
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def link_summoner(self, ctx: commands.Context, summoner_name):
        """Link summoner name to the author's discord account."""

        # TODO: Si un summoners name est deja linked l'afficher et demander si l'utilisateur desir le changer
        try:
            summoner_info = self.lolwatcher.summoner.by_name('na1', summoner_name)
            self.summoners[ctx.message.author] = summoner_info
            await ctx.send("Summoner name successfully linked.")
        except ApiError as err:
            if err.response.status_code == 404:
                await ctx.send("Invalid summoner name.")

    @commands.command(name="summoner")
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def show_linked_summoner(self, ctx: commands.Context):
        """Show what summoner name is linked to the author's discord account."""

        try:
            message = f"Your linked summoner name is: {self.summoners[ctx.message.author]['name']}."
            await ctx.send(message)
        except KeyError:
            await ctx.send("You don't have a summoner's name linked to your account.")

    @commands.command(name="rank")
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def show_rank(self, ctx: commands.Context):
        """Displays the command's author Solo/Duo rank."""
        try:
            summoner_info = self.summoners[ctx.message.author]
            rank_info = self.lolwatcher.league.by_summoner('na1', summoner_info['id'])
            message = f"Your rank is: {rank_info[0]['tier']} {rank_info[0]['rank']} {rank_info[0]['leaguePoints']}LP"
            await ctx.send(message)
        except KeyError:
            await ctx.send("There are no summoner name linked to your account.")


def setup(bot: commands.Bot):
    load_dotenv()
    RIOT_TOKEN = os.getenv("RIOT_TOKEN")
    bot.add_cog(LoLBot(bot, RIOT_TOKEN))

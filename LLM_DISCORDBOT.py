import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook

class QueryCog(commands.Cog):
    def __init__(self, bot, agent):
        self.bot = bot
        self.agent = agent

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

def start_discord_client(bot_token, agent):
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="/", intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')

    @bot.command()
    async def ping(ctx):
        await ctx.send('Im live!')

    @bot.command()
    async def ask(ctx, *args):
        query = ' '.join(args) 
        processing_message = await ctx.send('Processing your request...')
        try:
            response = agent.process_query(query)
            await ctx.send(response) 
        except Exception as e:
            await ctx.send(f'An error occurred: {e}')
        finally:
            await processing_message.delete() 

    bot.add_cog(QueryCog(bot, agent))
    bot.run(bot_token)
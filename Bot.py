import discord
from discord.ext import commands
import random
import requests

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace with the actual role ID you want to assign
TARGET_ROLE_ID = 1292419497122201620

# Fun commands
@bot.command()
async def ping(ctx):
    """Ping command to check if the bot is responsive."""
    await ctx.send("Pong! 🏓")

@bot.command()
async def about(ctx):
    """Displays information about the bot and lists all available commands."""
    embed = discord.Embed(
        title="About Me",
        description="I'm a bot that can assign roles when you send me an image. I also have some fun commands to try out! 🎉",
        color=discord.Color.blue()
    )
    
    # Dynamically create the list of commands
    command_list = "\n".join([f"`!{command.name}` - {command.help}" for command in bot.commands])

    embed.add_field(name="Available Commands", value=command_list)
    await ctx.send(embed=embed)

@bot.command()
async def hello(ctx):
    """Sends a personalized greeting."""
    user = ctx.author
    await ctx.send(f"Hello, {user.mention}! How's it going? 😊")

@bot.command()
async def fact(ctx):
    """Sends a random fun fact."""
    facts = [
        "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old!",
        "A day on Venus is longer than a year on Venus.",
        "There are more stars in the universe than grains of sand on all the Earth's beaches.",
        "Sloths only poop once a week!",
        "Wombat poop is cube-shaped."
    ]
    fact = random.choice(facts)
    await ctx.send(f"Here's a fun fact: {fact} 🧠✨")

@bot.command()
async def weather(ctx):
    """Sends a random weather-related fact or joke."""
    weather_facts_or_jokes = [
        "Why did the tornado break up with the hurricane? It was a whirlwind romance! 🌪️",
        "It can rain diamonds on Jupiter and Saturn due to extreme pressure. 💎☔",
        "The highest temperature ever recorded on Earth was 134°F (56.7°C) in Death Valley, California, in 1913. 🌞",
        "Did you know? On Mars, the seasons are twice as long as Earth’s because it takes Mars 687 days to orbit the sun! 🌌"
    ]
    fact_or_joke = random.choice(weather_facts_or_jokes)
    await ctx.send(f"Here's a weather-related fact or joke: {fact_or_joke} 🌧️")

@bot.event
async def on_ready():
    """Sets the bot's status and Rich Presence when the bot is ready."""
    activity = discord.Activity(
        type=discord.ActivityType.playing,  # 'playing', 'watching', 'listening'
        name="Monitoring Quasar.cc Free Users 👀💻"
    )
    await bot.change_presence(
        activity=activity, 
        status=discord.Status.online  # Ensure bot shows as online
    )
    print(f"Logged in as {bot.user} and online status set correctly.")

@bot.event
async def on_message(message):
    """Handles messages and roles when a valid image is sent in a DM."""
    if message.author == bot.user:
        return

    # Check if the message is a DM and contains an attachment
    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        # Ensure the attachment is an image
        if any(att.content_type.startswith("image") for att in message.attachments):
            # Iterate through mutual guilds to assign the role
            for guild in bot.guilds:
                member = guild.get_member(message.author.id)
                if member:
                    role = guild.get_role(TARGET_ROLE_ID)
                    if role:
                        await member.add_roles(role)
                        # Send the confirmation message with an embedded response
                        embed = discord.Embed(
                            title="Role Assigned! 🎉",
                            description=f"You have been given the '{role.name}' role in {guild.name}! 🎉",
                            color=discord.Color.green()
                        )
                        embed.add_field(name="Fun Commands", value="I also have other fun commands! Try `!ping`, `!about`, `!hello`, `!fact`, `!weather`. ")
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("The specified role doesn't exist in the server.")
        else:
            await message.channel.send("Please send a valid image file to get the role.")
    
    # Process commands if it's not a DM with an attachment
    await bot.process_commands(message)

# Run the bot with your fake Discord token
bot.run("MTMwNTM0NjE1NzAxNDE1OTQyMw.G7QYt6.EiyYuecyO6YSIP3N-FKeHW8sLVv5KWKgRtW09M")

from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions
from pycord.ext import ipc
import aiosqlite
import urllib.parse
from tools.get_channel_info import (
    get_announcement_channel,
    set_announcement_channel_tool,
    get_counting_channel,
)
from dotenv import load_dotenv
import os

load_dotenv()


app = Quart(__name__)
# set static folder
app.static_folder = "static"
# get secret key from env
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
ipc_client = ipc.Client(secret_key=os.getenv("SECRET_KEY"))
app.config["DISCORD_CLIENT_ID"] = os.getenv(
    "client_id"
)  # Your Client ID here   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.getenv(
    "client_secret"
)  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["Owner_ID"] = os.getenv("owner_id")


discord = DiscordOAuth2Session(app)


@app.route("/")
async def home():
    return await render_template("index.html", authorized=await discord.authorized)


@app.route("/login")
async def login():
    return await discord.create_session()


@app.route("/logout")
async def logout():
    discord.revoke()
    return redirect(url_for("home"))


@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except Exception:
        pass

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
async def dashboard():
    if not await discord.authorized:
        return redirect(url_for("login"))

    guild_count = await ipc_client.request("get_guild_count")
    guild_ids = await ipc_client.request("get_guild_ids")

    user_guilds = await discord.fetch_guilds()

    guilds = []

    for guild in user_guilds:
        if guild.permissions.administrator:
            guild.class_color = (
                "green-border" if guild.id in guild_ids else "red-border"
            )
            guilds.append(guild)

    guilds.sort(key=lambda x: x.class_color == "red-border")
    name = (await discord.fetch_user()).name
    return await render_template(
        "dashboard.html", guild_count=guild_count, guilds=guilds, username=name
    )


@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    guild = await ipc_client.request("get_guild", guild_id=guild_id)
    if guild is None:
        return redirect(
            f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}'
        )
    servername = guild["name"]
    prefix = guild["prefix"]
    channels = await ipc_client.request("get_channels", guild_id=guild_id)
    announment_channel = await get_announcement_channel(guild_id)
    announment_channel_name = await ipc_client.request(
        "get_channel_name", guild_id=guild_id, channel_id=announment_channel
    )
    counting_channel = await get_counting_channel(guild_id)
    counting_channel_name = await ipc_client.request(
        "get_channel_name", guild_id=guild_id, channel_id=counting_channel
    )

    name = (await discord.fetch_user()).name
    return await render_template(
        "dashboard_server.html",
        guild_id=guild_id,
        servername=servername,
        prefix=prefix,
        channels=channels,
        name=name,
        announment_channel=announment_channel_name,
        counting_channel=counting_channel_name,
    )


@app.route("/dashboard/<int:guild_id>/change_prefix", methods=["POST"])
async def change_prefix(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    prefix = await request.get_data("prefix")
    prefix = prefix.decode("utf-8")
    prefix = prefix.replace("prefix=", "")
    # turn http codes into readable text
    prefix = urllib.parse.unquote(prefix)
    print(prefix)
    await ipc_client.request("change_prefix", guild_id=guild_id, prefix=prefix)
    return redirect(url_for("dashboard_server", guild_id=guild_id))


@app.route("/dashboard/<int:guild_id>/set_counting_channel", methods=["POST"])
async def set_counting_channel(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    channel_id = await request.get_data("channel_id")
    channel_id = channel_id.decode("utf-8")
    channel_id = channel_id.replace("channel_id=", "")
    # turn http codes into readable text
    channel_id = urllib.parse.unquote(channel_id)
    print(channel_id)
    async with aiosqlite.connect("./databases/counting.db") as db:
        data = await db.execute(
            "SELECT * FROM counting WHERE guild_id = ?", (guild_id,)
        )
        data = await data.fetchall()
        if len(data) == 0:
            if channel_id == "None":
                channel_id = None
            await db.execute(
                "INSERT INTO counting VALUES (?, ?, ?, ?, ?,?)",
                (guild_id, channel_id, 0, 0, None, 0),
            )
            await db.commit()
        else:
            if channel_id == "None":
                channel_id = None
            await db.execute(
                "UPDATE counting SET counting_channel = ? WHERE guild_id = ?",
                (channel_id, guild_id),
            )
            await db.commit()
    return redirect(url_for("dashboard_server", guild_id=guild_id))


@app.route("/dashboard/<int:guild_id>/set_announcement_channel", methods=["POST"])
async def set_announcement_channel(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    channel_id = await request.get_data("channel_id")
    channel_id = channel_id.decode("utf-8")
    channel_id = channel_id.replace("channel_id=", "")
    # turn http codes into readable text
    channel_id = urllib.parse.unquote(channel_id)
    await set_announcement_channel_tool(guild_id, channel_id)
    return redirect(url_for("dashboard_server", guild_id=guild_id))

@app.route("/xp_leaderboard/<int:guild_id>")
async def xp_leaderboard(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    guild = await ipc_client.request("get_guild", guild_id=guild_id)
    if guild is None:
        return redirect(
            f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}'
        )
    servername = guild["name"]
    name = (await discord.fetch_user()).name
    #ipc request get xp leaderboard from cog 
    leaderboard = await ipc_client.request("get_xp_leaderboard", guild_id=guild_id)
    return await render_template(
        "xp_leaderboard.html",
        guild_id=guild_id,
        servername=servername,
        leaderboard=leaderboard,
        name=name,
    )



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)

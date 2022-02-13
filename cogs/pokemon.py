import asyncio
import discord
from discord.ext import commands
import os
import json
import random
import httpx as requests



class pokemon(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.first_move = True

    @commands.command(aliases=['pokedex'])
    async def pokidex(self, ctx, *, name):
        if len(name.split(" ")) == 1:
            try:
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
                data = response.json()

                poke_image = get_image(data)
                hp = data['base_experience']
                name = data['name'].title()
                height = str(data['height'] / 10) + "m"
                weight = str(data['weight'] / 10) + "kg"
                category = data['types'][0]['type']['name'].title()
                ability = [d['ability']['name'].capitalize() for d in data['abilities']]

                message = discord.Embed(title=name, color=discord.Colour.orange())

                message.set_thumbnail(url=poke_image)
                message.add_field(name="HP", value=hp)
                message.add_field(name="Height", value=height)
                message.add_field(name="Weight", value=weight)
                message.add_field(name="Category", value=category)
                message.add_field(name="Abilities", value="\n".join(ability))

                await ctx.send(embed=message)

            except:
                message = discord.Embed(title="Sorry, no Pokemon found", color=discord.Colour.orange())
                await ctx.send(embed=message)

        else:
            message = discord.Embed(title="The name cannot contain two or more words", color=discord.Colour.orange())
            await ctx.send(embed=message)


def check_pokemon(pokemon_name):
    URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"

    try:
        response = requests.get(URL)
        response = response.json()
        name = response['name'].title()
        return True
    except:
        return False


def get_pokemon_data(pokemon_name):
    URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(URL)
    response = response.json()

    pokemon_data = dict()
    pokemon_data["name"] = response["name"]
    pokemon_data["health"] = response["stats"][0]["base_stat"]

    try:
        image_url = response['sprites']['other']['official-artwork']['front_default']
    except:
        image_url = response['sprites']['front_shiny']

    poke_moves = []
    move_names = []

    for i, move in enumerate(response['moves']):
        url = move["move"]["url"]
        response = requests.get(url)
        response = response.json()
        if response["power"] is None: power = 20
        else: power = round(int(response["power"])/3)

        tmp_dict = {
            "move_name": move['move']['name'],
            "damage": power,
            "move_index": i+1
        }
        move_names.append(f"{move['move']['name']} - {power}")
        poke_moves.append(tmp_dict)

        if i == 3:
            break

    pokemon_data['moves'] = poke_moves[:4]

    embed_message = discord.Embed(title=pokemon_data["name"], color=discord.Colour.orange())
    embed_message.add_field(name="Health", value=pokemon_data["health"])
    embed_message.add_field(name="Moves", value="\n".join(move_names[:4]))
    embed_message.set_thumbnail(url=image_url)

    return pokemon_data, embed_message

def get_image(data):
    try:
        image = data['sprites']['other']['official-artwork']['front_default']
    except:
        image = data['sprites']['front_shiny']
    return image


def setup(client):
    client.add_cog(pokemon(client))
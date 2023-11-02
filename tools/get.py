import aiohttp
import asyncio


async def post_get_json(url, data=None):
    """
    This function makes a POST request to a url and returns the json
    Args:
        url (str) : The url to make a request to
        data (Dict, optional) : This is a dictionary of any extra params to send the request

    Returns:
        Dict : The json response
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            try:
                response = await resp.json()
            except Exception as e:
                print(e)
                response = resp
    return response

from asyncio import get_even_loop

from obhavo import ObHavo

async def main():
    data = await ObHavo(city='toshkent').obhavo()
    print(data)
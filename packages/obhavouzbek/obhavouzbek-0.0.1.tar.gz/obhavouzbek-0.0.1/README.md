```python
from asyncio import get_event_loop

from obhavo import ObHavo


async def main():
    data = await ObHavo(city='toshkent').obhavo()
    print(data)

if __name__ == '__main__':
    get_event_loop().run_until_complete(main())
```
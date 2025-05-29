import asyncio

async def heartbeat():
    try:
        while True:
            print("Heartbeat...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Heartbeat cancelled.")

async def main():
    task = asyncio.create_task(heartbeat())
    await asyncio.sleep(3)
    task.cancel()
    await task

asyncio.run(main())

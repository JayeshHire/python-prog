import asyncio
import random

async def poll_sensor():
    while True:
        value = random.randint(1, 100)
        print(f"Sensor value: {value}")
        if value > 90:
            print("Threshold reached, stopping...")
            break
        await asyncio.sleep(0.5)  # Simulate async waiting

asyncio.run(poll_sensor())

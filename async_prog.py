import asyncio
import time 
import io 


async def gen_a_seq(text_stream: io.StringIO):
    try:
        while True:
            text_stream.write("a")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("cancelling sequence generation for task")


async def gen_b_seq(text_stream: io.StringIO):
    try:
        while True:
            text_stream.write("b")
            await asyncio.sleep(1.5)
    except asyncio.CancelledError:
        print("cancelling sequence generation for task")


async def detect_seq(text_stream: io.StringIO):
    abs_pos = 0
    try:
        while True:
            text_stream.seek(abs_pos)
            val = text_stream.read(1)
            if val == 'a':
                print(f"reading a {abs_pos}")
            elif val == "b":
                print("reading b")
            else:
                print(f"none value {abs_pos}")
                text_stream.seek(abs_pos)
            abs_pos = text_stream.tell()
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("cancelling the sequence detection")

async def main():
    stream = io.StringIO()
    seq_a_task = asyncio.create_task(gen_a_seq(stream))
    seq_b_task = asyncio.create_task(gen_b_seq(stream))
    seq_detect_task = asyncio.create_task(detect_seq(stream))
    await asyncio.sleep(6)
    seq_a_task.cancel()
    seq_b_task.cancel()
    await seq_a_task
    await seq_b_task
    await asyncio.sleep(5)
    seq_detect_task.cancel()
    await seq_detect_task

    stream.seek(0)
    print(stream.read())


if __name__ == "__main__":    
    asyncio.run(main())
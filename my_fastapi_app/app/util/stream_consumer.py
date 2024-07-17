import httpx
import asyncio
import json

async def consume_streaming_endpoint(url):
    while True:
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("GET", url) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        yield json.dumps({"url": url, "data": chunk.decode()})
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            print(f"An error occurred with {url}: {exc}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            print(f"Stream consumption cancelled for {url}.")
            break
        except Exception as exc:
            print(f"Unexpected error with {url}: {exc}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)

async def consume_and_yield(url):
    async for result in consume_streaming_endpoint(url):
        yield result

async def task_wrapper(generator, results):
    async for result in generator:
        results.append(result)

async def video_generator(urls):
    results = []
    tasks = [asyncio.create_task(task_wrapper(consume_and_yield(url), results)) for url in urls]

    while tasks:
        if results:
            result = results.pop(0)
            yield f"data: {result}\n\n"
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            try:
                await task
            except Exception as exc:
                print(f"Unexpected error in task: {exc}")
            tasks.remove(task)

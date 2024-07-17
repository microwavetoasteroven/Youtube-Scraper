import httpx
import asyncio
import time

async def consume_streaming_endpoint(url):
    while True:
        try:
            # Create an asynchronous HTTP client
            async with httpx.AsyncClient() as client:
                # Send a GET request and get a streaming response
                async with client.stream("GET", url) as response:
                    response.raise_for_status()  # Check for HTTP errors
                    # Iterate over the response in chunks of bytes
                    async for chunk in response.aiter_bytes():
                        # Process the binary data (e.g., save to file, process video frames, etc.)
                        print(chunk)
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            # Handle request and HTTP errors
            print(f"An error occurred: {exc}. Reconnecting in 5 seconds...")
            time.sleep(5)  # Wait before reconnecting
        except asyncio.CancelledError:
            # Handle cancellation, such as when stopping the program
            print("Stream consumption cancelled.")
            break
        except Exception as exc:
            # Handle any other exceptions
            print(f"Unexpected error: {exc}. Reconnecting in 5 seconds...")
            time.sleep(5)  # Wait before reconnecting

# Define the URL of the streaming endpoint
url = "http://your-fastapi-server/stream-endpoint"

# Run the asynchronous function
asyncio.run(consume_streaming_endpoint(url))

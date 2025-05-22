import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai

client = genai.Client()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

bucket = f"gs://{PROJECT_ID}-assets"

# MCP tools
imagen_stdio = StdioServerParameters(
    command="mcp-imagen-go",
    args=[],
    env={"PROJECT_ID": PROJECT_ID},
)

veo_stdio = StdioServerParameters(
    command="mcp-veo-go",
    args=[],
    env={"PROJECT_ID": PROJECT_ID},
)

current_working_dir = os.getcwd()


# prompt = f"""Let's make magic! 
# First: Create an image of 'a cat running through the woods'

# Use the following bucket: {bucket}. Then download this image to {current_working_dir}
# """

prompt = f"""Let's generate some media!

1.  **Image Task**: Create an image of 'a tortiseshell cat surveying a savanna kingdom at sunset', in 16:9 aspect.

2.  **Video Task**: Create 4 8-second 16:9 video clips using the image generated.

Use the GCS bucket for each task: {bucket}
Download each asset to the local directory: {current_working_dir}

Please confirm once both tasks are initiated or completed, providing any relevant URIs or information.
"""

async def run():
    
    async with stdio_client(veo_stdio) as (read, write):
        async with stdio_client(veo_stdio) as (veo_read, veo_write):
            async with ClientSession(veo_read, veo_write) as veo_session:
                print("Initializing Veo MCP session...")
                await veo_session.initialize()
                print("Veo MCP session initialized.")

                async with stdio_client(imagen_stdio) as (read, write):
                    async with ClientSession(read, write) as imagen_session:
                        # Initialize the connection between client and server
                        await imagen_session.initialize()


                        # Send request to the model with MCP function declarations
                        response = await client.aio.models.generate_content(
                            model="gemini-2.0-flash",
                            contents=prompt,
                            config=genai.types.GenerateContentConfig(
                                temperature=0,
                                tools=[imagen_session, veo_session],
                                # do NOT automatically call MCP
                                # automatic_function_calling=genai.types.AutomaticFunctionCallingConfig(
                                #     disable=True
                                # ),
                                system_instruction=
                                    [
                                    """You are a helpful generative media creation assistant. Use your tools to fullfill the tasks."""
                                    ]
                            ),
                        )
                        print(response.text)

# Start the asyncio event loop and run the main function
asyncio.run(run())



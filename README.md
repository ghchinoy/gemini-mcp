# MCP with Gemini

Use the experimental MCP client in the Gemini SDK with the MCP Tools for Genmedia - Veo, Imagen, and more.

## Quick run

```bash
export GOOGLE_CLOUD_PROJECT=$(gcloud config get project)
export GOOGLE_CLOUD_LOCATION=global
export GOOGLE_GENAI_USE_VERTEXAI=True

uv run genmedia.py
```

## Docs

[Model Context Protocol with the Gemini SDK](https://ai.google.dev/gemini-api/docs/function-calling?example=meeting#model_context_protocol_mcp)

[MCP Tools for Genmedia](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/tree/mcp-genmedia-servers/experiments/mcp-genmedia) - Veo, Imagen, Lyria, Chirp 3 HD, and more.


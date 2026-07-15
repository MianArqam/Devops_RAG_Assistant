from app.core.config import settings


SYSTEM_GUIDANCE = """You are a junior DevOps engineer assistant.
Use the provided context to diagnose likely causes and suggest practical fixes.
Be concise, cite sources by filename, and mention when the context is insufficient."""


def build_prompt(query: str, context: str) -> str:
    return f"""{SYSTEM_GUIDANCE}

Context:
{context}

Question or log:
{query}

Return:
- Possible cause
- Suggested fix
- Source citations
"""


async def generate_answer(query: str, context: str) -> str:
    provider = settings.llm_provider.lower()
    prompt = build_prompt(query, context)

    try:
        if provider == "openai" and settings.openai_api_key:
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_GUIDANCE},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            return response.choices[0].message.content or ""

        if provider == "gemini" and settings.gemini_api_key:
            return await generate_gemini_answer(prompt)
    except Exception as exc:
        return (
            f"LLM provider error ({provider}): {exc}\n\n"
            "The app still retrieved local documentation, but the configured LLM call failed.\n\n"
            f"{fallback_answer(query, context)}"
        )

    return fallback_answer(query, context)


async def generate_gemini_answer(prompt: str) -> str:
    import httpx

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.gemini_model}:generateContent"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2},
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            url,
            params={"key": settings.gemini_api_key},
            json=payload,
        )

    if response.status_code >= 400:
        detail = response.text[:500]
        raise RuntimeError(f"Gemini API returned HTTP {response.status_code}: {detail}")

    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini returned no candidates.")
    parts = candidates[0].get("content", {}).get("parts", [])
    return "\n".join(part.get("text", "") for part in parts).strip()


def fallback_answer(query: str, context: str) -> str:
    if not context.strip():
        return (
            "Possible cause:\n"
            "I could not find matching documentation in the local knowledge base yet.\n\n"
            "Suggested fix:\n"
            "Upload AWS, Docker, Kubernetes, or log documents with POST /upload, then try again.\n\n"
            "Source:\n"
            "No local source matched."
        )

    return (
        "Possible cause:\n"
        "The retrieved documentation contains related DevOps guidance for this error. "
        "Review the cited source snippets below and check permissions, runtime state, "
        "networking, or deployment configuration depending on the service involved.\n\n"
        "Suggested fix:\n"
        "Use the top matching source sections as the first troubleshooting path. "
        "For a more polished generated answer, set LLM_PROVIDER to openai or gemini "
        "and add the matching API key in backend/.env.\n\n"
        f"Retrieved context:\n{context}"
    )

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
KB_DIR = ROOT / "kb"
SYSTEM_PROMPT = (ROOT / "prompts" / "system_prompt.md").read_text()


def load_retrieved_docs() -> list[str]:
    return [path.read_text() for path in sorted(KB_DIR.glob("*.md"))]


def build_messages(user_request: str) -> list[dict[str, str]]:
    retrieved_docs = load_retrieved_docs()
    # Vulnerability: untrusted retrieved docs are merged into a high-authority system block.
    system_content = SYSTEM_PROMPT + "\n\nRetrieved context:\n" + "\n\n".join(retrieved_docs)
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_request},
    ]


if __name__ == "__main__":
    for message in build_messages("Answer the onboarding question."):
        print(message["role"].upper())
        print(message["content"])
        print("---")

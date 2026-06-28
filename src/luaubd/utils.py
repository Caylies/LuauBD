import re

START_CODE_BLOCK_RE = re.compile(r"^((```(lua(u)?))(?=\s)|(```))")

__all__ = ("clean_luau_markdown",)


def clean_luau_markdown(content: str):
    """
    Removes Luau code markdown from a string.

    Parameters
    ----------
    content: str
        The content containing the markdown.

    Returns
    -------
    str
        The content with no luau code block markdown.
    """
    if content.startswith("```") and content.endswith("```"):
        return START_CODE_BLOCK_RE.sub("", content)[:-3]

    return content.strip("` \n")

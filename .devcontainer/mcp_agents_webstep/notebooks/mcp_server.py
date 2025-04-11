from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP Server")


@mcp.tool()
async def count_letters(word: str, letter: str) -> int:
    """
    Count the occurrences of a letter in a word.

    Args:
        word: The word in which to count the letter.
        letter: The letter to count.
    Returns:
        The number of occurrences of the letter in the word.
    """
    return word.lower().count(letter.lower())


if __name__ == "__main__":
    mcp.run(transport="stdio")

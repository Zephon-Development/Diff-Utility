"""
Simple greeter module demonstrating type-safe code per CODING_STANDARDS.md.

This module serves as a template example showing:
- Explicit type annotations (§2.1)
- Google-style docstrings (§3.1)
- Clean, testable functions
"""


def greeter(name: str, *, formal: bool = False) -> str:
    """
    Generate a greeting message for the given name.

    Args:
        name: The name to greet.
        formal: If True, use formal greeting style. Defaults to False.

    Returns:
        A greeting string appropriate for the specified formality level.

    Raises:
        ValueError: If name is empty or contains only whitespace.

    Examples:
        >>> greeter("World")
        'Hello, World!'
        >>> greeter("Dr. Smith", formal=True)
        'Good day, Dr. Smith.'
    """
    if not name or not name.strip():
        msg = "Name cannot be empty or whitespace"
        raise ValueError(msg)

    clean_name = name.strip()

    if formal:
        return f"Good day, {clean_name}."

    return f"Hello, {clean_name}!"

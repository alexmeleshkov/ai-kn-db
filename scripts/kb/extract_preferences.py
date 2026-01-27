#!/usr/bin/env python3
"""
Extract color and font preferences from user prompts.

Parses user input for style keywords and maps them to concrete CSS values.
Returns structured preferences for CSS injection.

Repository rule: file contents and code comments must be in English.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class StylePreferences:
    """Structured style preferences extracted from user prompt."""
    colors: dict[str, str]
    fonts: dict[str, str]
    font_url: str | None


# Color keyword mappings
COLOR_MAPPINGS = {
    "pink": {
        "primary": "#ff69b4",
        "light": "#ffc0cb",
        "dark": "#c71585",
        "background": "#fff5f8",
    },
    "rose": {
        "primary": "#ff69b4",
        "light": "#ffc0cb",
        "dark": "#c71585",
        "background": "#fff5f8",
    },
    "purple": {
        "primary": "#9b59b6",
        "light": "#e8daef",
        "dark": "#6c3483",
        "background": "#f4ecf7",
    },
    "blue": {
        "primary": "#3498db",
        "light": "#aed6f1",
        "dark": "#1f618d",
        "background": "#ebf5fb",
    },
    "green": {
        "primary": "#27ae60",
        "light": "#abebc6",
        "dark": "#186a3b",
        "background": "#e8f8f5",
    },
    "dark": {
        "primary": "#2c3e50",
        "light": "#566573",
        "dark": "#1c2833",
        "background": "#ecf0f1",
    },
    "light": {
        "primary": "#ecf0f1",
        "light": "#ffffff",
        "dark": "#bdc3c7",
        "background": "#fdfefe",
    },
    "red": {
        "primary": "#e74c3c",
        "light": "#f5b7b1",
        "dark": "#922b21",
        "background": "#fadbd8",
    },
    "orange": {
        "primary": "#f39c12",
        "light": "#f8c471",
        "dark": "#b9770e",
        "background": "#fef5e7",
    },
    "yellow": {
        "primary": "#f1c40f",
        "light": "#f9e79f",
        "dark": "#9a7d0a",
        "background": "#fef9e7",
    },
}

# Font style keyword mappings
FONT_MAPPINGS = {
    "fancy": {
        "heading": "'Playfair Display', serif",
        "body": "'Crimson Text', serif",
        "url": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Crimson+Text:wght@400;600&display=swap",
    },
    "elegant": {
        "heading": "'Cormorant Garamond', serif",
        "body": "'Lora', serif",
        "url": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;700&family=Lora:wght@400;600&display=swap",
    },
    "playful": {
        "heading": "'Fredoka One', cursive",
        "body": "'Quicksand', sans-serif",
        "url": "https://fonts.googleapis.com/css2?family=Fredoka+One&family=Quicksand:wght@400;600&display=swap",
    },
    "minimal": {
        "heading": "'Inter', sans-serif",
        "body": "'Inter', sans-serif",
        "url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
    },
    "modern": {
        "heading": "'Montserrat', sans-serif",
        "body": "'Roboto', sans-serif",
        "url": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto:wght@400;600&display=swap",
    },
}

# Default styles (system fonts, neutral colors)
DEFAULT_COLORS = {
    "primary": "#4a5568",
    "light": "#e2e8f0",
    "dark": "#2d3748",
    "background": "#ffffff",
}

DEFAULT_FONTS = {
    "heading": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "body": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
}


def extract_color_keywords(prompt: str) -> list[str]:
    """Extract color keywords from prompt (case-insensitive)."""
    prompt_lower = prompt.lower()
    found = []
    for color_key in COLOR_MAPPINGS.keys():
        if re.search(r"\b" + re.escape(color_key) + r"\b", prompt_lower):
            found.append(color_key)
    return found


def extract_font_keywords(prompt: str) -> list[str]:
    """Extract font style keywords from prompt (case-insensitive)."""
    prompt_lower = prompt.lower()
    found = []
    for font_key in FONT_MAPPINGS.keys():
        if re.search(r"\b" + re.escape(font_key) + r"\b", prompt_lower):
            found.append(font_key)
    return found


def extract_preferences(prompt: str) -> StylePreferences:
    """
    Parse user prompt and extract style preferences.

    Args:
        prompt: User's project description (e.g., "create chat in pink with fancy fonts")

    Returns:
        StylePreferences with colors, fonts, and optional Google Fonts URL
    """
    color_keywords = extract_color_keywords(prompt)
    font_keywords = extract_font_keywords(prompt)

    # Select first matching color, fallback to defaults
    colors = DEFAULT_COLORS.copy()
    if color_keywords:
        colors = COLOR_MAPPINGS[color_keywords[0]].copy()

    # Select first matching font style, fallback to defaults
    fonts = DEFAULT_FONTS.copy()
    font_url = None
    if font_keywords:
        font_data = FONT_MAPPINGS[font_keywords[0]]
        fonts = {"heading": font_data["heading"], "body": font_data["body"]}
        font_url = font_data["url"]

    return StylePreferences(colors=colors, fonts=fonts, font_url=font_url)


def preferences_to_dict(prefs: StylePreferences) -> dict[str, Any]:
    """Convert StylePreferences to plain dict for serialization."""
    return {
        "colors": prefs.colors,
        "fonts": prefs.fonts,
        "font_url": prefs.font_url,
    }


if __name__ == "__main__":
    # Standalone test
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python extract_preferences.py <prompt>")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    prefs = extract_preferences(prompt)

    print(json.dumps(preferences_to_dict(prefs), indent=2, ensure_ascii=False))

#!/usr/bin/env python3
"""
Inject CSS preferences into generated project files.

Finds .tsx files with <style> blocks and injects CSS custom properties.
Replaces hardcoded colors and fonts with CSS variables.

Repository rule: file contents and code comments must be in English.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def generate_css_variables(preferences: dict[str, Any]) -> str:
    """
    Generate CSS custom properties from preferences.

    Args:
        preferences: Dict with 'colors' and 'fonts' keys

    Returns:
        CSS string with :root custom properties
    """
    colors = preferences.get("colors", {})
    fonts = preferences.get("fonts", {})

    css_lines = ["        :root {"]

    # Color variables
    for key, value in colors.items():
        css_var_name = f"--color-{key.replace('_', '-')}"
        css_lines.append(f"          {css_var_name}: {value};")

    # Font variables
    for key, value in fonts.items():
        css_var_name = f"--font-{key.replace('_', '-')}"
        css_lines.append(f"          {css_var_name}: {value};")

    css_lines.append("        }")
    css_lines.append("")

    return "\n".join(css_lines)


def inject_google_fonts(file_path: Path, font_url: str) -> None:
    """
    Inject Google Fonts import at the beginning of the <style> block.

    Args:
        file_path: Path to .tsx file
        font_url: Google Fonts URL
    """
    content = file_path.read_text(encoding="utf-8")

    # Find <style>{` ... `}</style> block
    style_pattern = r"(<style>\{\`)(.*?)(\`\}</style>)"
    match = re.search(style_pattern, content, re.DOTALL)

    if not match:
        return  # No style block found

    before_style = match.group(1)
    style_content = match.group(2)
    after_style = match.group(3)

    # Check if font import already exists
    if "@import" in style_content and font_url in style_content:
        return  # Already injected

    # Add Google Fonts import at the beginning
    import_line = f"\n        @import url('{font_url}');\n"
    new_style_content = import_line + style_content

    new_content = (
        content[: match.start()]
        + before_style
        + new_style_content
        + after_style
        + content[match.end() :]
    )

    file_path.write_text(new_content, encoding="utf-8")


def inject_css_variables(file_path: Path, preferences: dict[str, Any]) -> None:
    """
    Inject CSS variables into a .tsx file's <style> block.

    Args:
        file_path: Path to .tsx file
        preferences: Dict with colors, fonts, and font_url
    """
    content = file_path.read_text(encoding="utf-8")

    # Find <style>{` ... `}</style> block
    style_pattern = r"(<style>\{\`)(.*?)(\`\}</style>)"
    match = re.search(style_pattern, content, re.DOTALL)

    if not match:
        return  # No style block found

    before_style = match.group(1)
    style_content = match.group(2)
    after_style = match.group(3)

    # Check if variables already injected
    if ":root {" in style_content and "--color-primary" in style_content:
        return  # Already injected

    # Generate CSS variables
    css_vars = generate_css_variables(preferences)

    # Inject at the beginning of style block
    new_style_content = "\n" + css_vars + style_content

    new_content = (
        content[: match.start()]
        + before_style
        + new_style_content
        + after_style
        + content[match.end() :]
    )

    file_path.write_text(new_content, encoding="utf-8")


def replace_hardcoded_colors(file_path: Path) -> None:
    """
    Replace hardcoded color values with CSS variables.

    Mapping:
    - #007bff (blue) -> var(--color-primary)
    - #f8f9fa, #f1f3f5, #f5f5f5 (light grays) -> var(--color-light)
    - white -> var(--color-background)
    - #333, #666 (dark grays) -> var(--color-dark)
    """
    content = file_path.read_text(encoding="utf-8")

    # Color replacements (only within style blocks)
    color_map = {
        r"#007bff": "var(--color-primary)",
        r"#f8f9fa": "var(--color-background)",
        r"#f1f3f5": "var(--color-light)",
        r"#f5f5f5": "var(--color-light)",
        r"white": "var(--color-background)",
        r"#333": "var(--color-dark)",
        r"#666": "var(--color-dark)",
    }

    # Find style block
    style_pattern = r"(<style>\{\`)(.*?)(\`\}</style>)"
    match = re.search(style_pattern, content, re.DOTALL)

    if not match:
        return

    before_style = match.group(1)
    style_content = match.group(2)
    after_style = match.group(3)

    # Replace colors in style content
    for color_hex, css_var in color_map.items():
        # Only replace in color properties (not in content strings)
        # Match patterns like: color: #333; or background-color: white;
        pattern = rf"(\b(?:color|background-color|background|border-color)\s*:\s*){color_hex}(\s*[;}}])"
        style_content = re.sub(pattern, rf"\1{css_var}\2", style_content, flags=re.IGNORECASE)

    new_content = (
        content[: match.start()]
        + before_style
        + style_content
        + after_style
        + content[match.end() :]
    )

    file_path.write_text(new_content, encoding="utf-8")


def replace_hardcoded_fonts(file_path: Path) -> None:
    """
    Replace hardcoded font-family values with CSS variables.

    Replaces system font stacks with var(--font-body) or var(--font-heading)
    """
    content = file_path.read_text(encoding="utf-8")

    # Find style block
    style_pattern = r"(<style>\{\`)(.*?)(\`\}</style>)"
    match = re.search(style_pattern, content, re.DOTALL)

    if not match:
        return

    before_style = match.group(1)
    style_content = match.group(2)
    after_style = match.group(3)

    # Replace system font stacks with CSS variable
    # Match: font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', ...;
    font_pattern = r"(font-family\s*:\s*)[-a-zA-Z,\s'\"()]+;"

    def font_replacer(m: re.Match) -> str:
        prop = m.group(1)
        # Use var(--font-body) as default
        return f"{prop}var(--font-body);"

    style_content = re.sub(font_pattern, font_replacer, style_content)

    new_content = (
        content[: match.start()]
        + before_style
        + style_content
        + after_style
        + content[match.end() :]
    )

    file_path.write_text(new_content, encoding="utf-8")


def inject_styles(project_dir: Path, preferences: dict[str, Any]) -> None:
    """
    Inject style preferences into all .tsx files in project.

    Args:
        project_dir: Root directory of generated project
        preferences: Dict with colors, fonts, and optional font_url

    Steps:
        1. Find all .tsx files
        2. Inject Google Fonts URL if provided
        3. Inject CSS custom properties
        4. Replace hardcoded colors with variables
        5. Replace hardcoded fonts with variables
    """
    if not project_dir.exists():
        print(f"ERROR: Project directory not found: {project_dir}")
        return

    # Find all .tsx files
    tsx_files = list(project_dir.glob("**/*.tsx"))
    if not tsx_files:
        print("INFO: No .tsx files found, skipping style injection")
        return

    print(f"==> inject_styles: found {len(tsx_files)} .tsx files")

    font_url = preferences.get("font_url")

    for tsx_file in tsx_files:
        print(f"==> inject_styles: processing {tsx_file.name}")

        # Step 1: Inject Google Fonts if URL provided
        if font_url:
            inject_google_fonts(tsx_file, font_url)

        # Step 2: Inject CSS variables
        inject_css_variables(tsx_file, preferences)

        # Step 3: Replace hardcoded colors
        replace_hardcoded_colors(tsx_file)

        # Step 4: Replace hardcoded fonts
        replace_hardcoded_fonts(tsx_file)

    print("==> inject_styles: complete")


if __name__ == "__main__":
    # Standalone test
    import sys
    import json

    if len(sys.argv) < 3:
        print("Usage: python inject_styles.py <project_dir> <preferences_json>")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    prefs_json = sys.argv[2]
    prefs = json.loads(prefs_json)

    inject_styles(project_path, prefs)

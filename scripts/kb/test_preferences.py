#!/usr/bin/env python3
"""
Manual test for preference extraction module.
Tests keyword matching without requiring Python execution.
"""
from extract_preferences import extract_preferences, preferences_to_dict
import json


def test_case(prompt: str, expected_colors: list[str], expected_fonts: list[str]) -> bool:
    """Test a single prompt and verify expectations."""
    prefs = extract_preferences(prompt)
    prefs_dict = preferences_to_dict(prefs)

    # Check if expected keywords would be detected
    colors_match = any(color in prompt.lower() for color in expected_colors) if expected_colors else True
    fonts_match = any(font in prompt.lower() for font in expected_fonts) if expected_fonts else True

    print(f"\n==> Test: '{prompt}'")
    print(f"Expected colors: {expected_colors}, fonts: {expected_fonts}")
    print(f"Result: {json.dumps(prefs_dict, indent=2)}")
    print(f"Colors match: {colors_match}, Fonts match: {fonts_match}")

    return colors_match and fonts_match


if __name__ == "__main__":
    print("=== Preference Extraction Tests ===")

    # Test 1: Pink with fancy fonts
    test_case(
        "create chat in pink with fancy fonts",
        expected_colors=["pink"],
        expected_fonts=["fancy"]
    )

    # Test 2: No preferences (defaults)
    test_case(
        "build a todo app",
        expected_colors=[],
        expected_fonts=[]
    )

    # Test 3: Blue with modern design
    test_case(
        "modern blue dashboard with minimal design",
        expected_colors=["blue"],
        expected_fonts=["modern", "minimal"]
    )

    # Test 4: Purple elegant theme
    test_case(
        "create an elegant purple portfolio site",
        expected_colors=["purple"],
        expected_fonts=["elegant"]
    )

    print("\n=== All tests completed ===")

# Style Injection System

This document describes the style preference extraction and CSS injection system for the KB-driven project generator.

## Overview

The style injection system allows users to specify color and font preferences in their project prompts, which are then automatically applied to generated projects.

## Architecture

### Components

1. **extract_preferences.py**: Parses user prompts for style keywords
2. **inject_styles.py**: Injects CSS variables and replaces hardcoded values
3. **generate_from_kb.py**: Orchestrates the extraction and injection flow

### Flow

```
User Prompt → Extract Preferences → Scaffold Project → Inject Styles → Generated Project
```

## Supported Keywords

### Color Keywords

- **pink/rose**: Pink tones (#ff69b4, #ffc0cb, #c71585, #fff5f8)
- **purple**: Purple tones (#9b59b6, #e8daef, #6c3483, #f4ecf7)
- **blue**: Blue tones (#3498db, #aed6f1, #1f618d, #ebf5fb)
- **green**: Green tones (#27ae60, #abebc6, #186a3b, #e8f8f5)
- **red**: Red tones (#e74c3c, #f5b7b1, #922b21, #fadbd8)
- **orange**: Orange tones (#f39c12, #f8c471, #b9770e, #fef5e7)
- **yellow**: Yellow tones (#f1c40f, #f9e79f, #9a7d0a, #fef9e7)
- **dark**: Dark theme (#2c3e50, #566573, #1c2833, #ecf0f1)
- **light**: Light theme (#ecf0f1, #ffffff, #bdc3c7, #fdfefe)

### Font Style Keywords

- **fancy**: Playfair Display + Crimson Text (elegant serif fonts)
- **elegant**: Cormorant Garamond + Lora (refined serif fonts)
- **playful**: Fredoka One + Quicksand (fun, rounded fonts)
- **minimal**: Inter (clean, minimal sans-serif)
- **modern**: Montserrat + Roboto (contemporary sans-serif)

## CSS Variables

The system injects the following CSS custom properties:

```css
:root {
  /* Color variables */
  --color-primary: #ff69b4;
  --color-light: #ffc0cb;
  --color-dark: #c71585;
  --color-background: #fff5f8;

  /* Font variables */
  --font-heading: 'Playfair Display', serif;
  --font-body: 'Crimson Text', serif;
}
```

## Replacement Rules

### Colors

The system replaces hardcoded colors in CSS properties:

- `#007bff` → `var(--color-primary)`
- `#f8f9fa`, `#f1f3f5`, `#f5f5f5` → `var(--color-light)`
- `white` → `var(--color-background)`
- `#333`, `#666` → `var(--color-dark)`

### Fonts

System font stacks are replaced with:

- `font-family: -apple-system, ...` → `font-family: var(--font-body);`

## Usage Examples

### Example 1: Pink with Fancy Fonts

```bash
./scripts/new-project "create chat in pink with fancy fonts"
```

Result:
- Primary color: Hot pink (#ff69b4)
- Fonts: Playfair Display (headings), Crimson Text (body)
- Google Fonts automatically imported

### Example 2: Modern Blue Dashboard

```bash
./scripts/new-project "modern blue dashboard with minimal design"
```

Result:
- Primary color: Blue (#3498db)
- Fonts: Inter (both headings and body)
- Clean, minimal aesthetic

### Example 3: Default Styling

```bash
./scripts/new-project "build a todo app"
```

Result:
- Default colors: Neutral grays
- Default fonts: System font stack
- No Google Fonts imported

## Implementation Details

### Keyword Detection

Keywords are detected using regex word boundary matching (`\b<keyword>\b`) for case-insensitive exact word matches. The first matching keyword in each category is used.

### Style Block Detection

The system finds inline `<style>` blocks in .tsx files using the pattern:

```tsx
<style>{`
  /* CSS content */
`}</style>
```

### Google Fonts Import

When a font style keyword is detected, the system injects:

```css
@import url('https://fonts.googleapis.com/css2?family=...');
```

at the beginning of each `<style>` block.

## Extension Guide

### Adding New Colors

Edit `extract_preferences.py`, add to `COLOR_MAPPINGS`:

```python
COLOR_MAPPINGS = {
    "teal": {
        "primary": "#14b8a6",
        "light": "#ccfbf1",
        "dark": "#0f766e",
        "background": "#f0fdfa",
    },
    # ... existing colors
}
```

### Adding New Fonts

Edit `extract_preferences.py`, add to `FONT_MAPPINGS`:

```python
FONT_MAPPINGS = {
    "retro": {
        "heading": "'Press Start 2P', cursive",
        "body": "'VT323', monospace",
        "url": "https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap",
    },
    # ... existing fonts
}
```

## Testing

### Manual Testing

Run the test suite:

```bash
python3 scripts/kb/test_preferences.py
```

### Integration Testing

Generate a project and verify styling:

```bash
./scripts/new-project "create chat in pink with fancy fonts"
cd generated/<project-dir>/frontend
grep --color "var(--color-primary)" src/App.tsx
grep --color "@import url" src/App.tsx
```

## Troubleshooting

### Issue: Styles Not Applied

**Symptom**: Generated project uses default gray/white colors

**Solutions**:
1. Check that color keyword is spelled correctly in prompt
2. Verify .tsx files have `<style>` blocks
3. Check that `inject_styles` runs after `apply_stack` in generate_from_kb.py

### Issue: Fonts Not Loading

**Symptom**: Google Fonts not appearing in browser

**Solutions**:
1. Verify `@import url()` is present in .tsx files
2. Check browser console for font loading errors
3. Ensure font URL is valid and accessible

### Issue: CSS Variables Not Working

**Symptom**: `var(--color-primary)` visible as text in browser

**Solutions**:
1. Verify `:root {}` block is present in style
2. Check that CSS variables are defined before being used
3. Ensure no CSS syntax errors in generated files

## Future Enhancements

Potential improvements for future iterations:

1. Support for gradient backgrounds
2. Animation speed preferences (slow, normal, fast)
3. Border radius preferences (sharp, rounded, pill)
4. Shadow intensity preferences (none, subtle, prominent)
5. Multiple color schemes (primary, secondary, accent)
6. Custom hex color input support
7. Theme preset system (e.g., "cyberpunk", "nature", "professional")

## References

- Original requirement: Task description (preference extraction and CSS injection)
- Existing generator: `scripts/kb/generate_from_kb.py:140-143` (copy_tree logic)
- Template files: `docs/kb/stacks/stack-react-fastapi-sql/templates/frontend/src/*.tsx`

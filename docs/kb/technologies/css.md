# CSS

**Technology**: CSS3 with CSS Variables
**Category**: Styling

---

## Overview

Complete stylesheet with Ipswich Town color scheme, CSS variables, component styles, and responsive design.

---

## Usage Files

- `frontend/src/styles/index.css` (3049 lines)

---

## Complete Usage Patterns

### CSS Variables (index.css)

**Pattern**:
```css
:root {
  --color-primary: #1a365d;
  --color-bg-main: #f7fafc;
  --spacing-md: 1rem;
  --radius-md: 0.5rem;
  --transition-fast: 150ms ease;
}

.button {
  background-color: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  transition: background-color var(--transition-fast);
}
```

**All Behaviors**:
- CSS custom properties for theme
- Ipswich blue color palette
- Spacing scale (xs, sm, md, lg, xl)
- Border radius scale
- Transition timing

### Component Styling

**Pattern**:
```css
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--color-bg-main);
}

.message-user {
  align-self: flex-end;
  background-color: var(--color-primary);
  color: var(--color-text-white);
}

.message-assistant {
  align-self: flex-start;
  background-color: var(--color-bg-white);
  color: var(--color-text-dark);
}
```

**All Behaviors**:
- Flexbox layouts
- Responsive design (768px breakpoint)
- Hover states
- Ipswich Town branding

---

## Configuration

```css
/* Ipswich Town Color Palette */
--color-primary: #1a365d
--color-accent: #3182ce

/* Spacing Scale */
--spacing-xs: 0.25rem (4px)
--spacing-sm: 0.5rem (8px)
--spacing-md: 1rem (16px)
--spacing-lg: 1.5rem (24px)
--spacing-xl: 2rem (32px)

/* Responsive Breakpoint */
@media (max-width: 768px) { ... }
```

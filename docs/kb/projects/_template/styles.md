# Styling System: [Project Name]

## CSS Architecture

**Approach**: [e.g., Global CSS with CSS custom properties | Tailwind CSS | styled-components | CSS Modules]
**Location**: [e.g., `frontend/src/styles/index.css`]
**Framework**: [Framework name and version, or "None (vanilla CSS)"]

## Color Palette

### Primary Colors

| Variable | Hex | RGB | Usage |
|----------|-----|-----|-------|
| `--color-primary` | #[hex] | rgb([r, g, b]) | Primary brand color, CTAs, accents |
| `--color-primary-light` | #[hex] | rgb([r, g, b]) | Light variant for hover states |
| `--color-primary-dark` | #[hex] | rgb([r, g, b]) | Dark variant for emphasis |

### Background Colors

| Variable | Hex | RGB | Usage |
|----------|-----|-----|-------|
| `--color-background` | #[hex] | rgb([r, g, b]) | Main page background |
| `--color-surface` | #[hex] | rgb([r, g, b]) | Card/container backgrounds |
| `--color-surface-hover` | #[hex] | rgb([r, g, b]) | Interactive surface hover state |

### Text Colors

| Variable | Hex | RGB | Usage |
|----------|-----|-----|-------|
| `--color-text-primary` | #[hex] | rgb([r, g, b]) | Primary text content |
| `--color-text-secondary` | #[hex] | rgb([r, g, b]) | Secondary/muted text |
| `--color-text-disabled` | #[hex] | rgb([r, g, b]) | Disabled text |

### Semantic Colors

| Variable | Hex | RGB | Usage |
|----------|-----|-----|-------|
| `--color-success` | #[hex] | rgb([r, g, b]) | Success states, confirmations |
| `--color-error` | #[hex] | rgb([r, g, b]) | Error states, warnings |
| `--color-warning` | #[hex] | rgb([r, g, b]) | Warning states |
| `--color-info` | #[hex] | rgb([r, g, b]) | Informational messages |

### Border Colors

| Variable | Hex | RGB | Usage |
|----------|-----|-----|-------|
| `--color-border` | #[hex] | rgb([r, g, b]) | Default borders and dividers |
| `--color-border-focus` | #[hex] | rgb([r, g, b]) | Focused input borders |

## Typography

### Font Families

| Element | Font Family | Fallback | Usage |
|---------|-------------|----------|-------|
| Headings | [font-name] | serif/sans-serif | Page titles, section headers |
| Body | [font-name] | system-ui, sans-serif | Main content |
| Code | [font-name] | monospace | Code blocks, technical content |
| UI | [font-name] | system-ui, sans-serif | Buttons, inputs, labels |

### Font Sizes

| Variable | Size | Usage |
|----------|------|-------|
| `--font-size-xs` | [size] | Small labels, captions |
| `--font-size-sm` | [size] | Secondary text |
| `--font-size-base` | [size] | Body text (default) |
| `--font-size-lg` | [size] | Subheadings |
| `--font-size-xl` | [size] | Section headings |
| `--font-size-2xl` | [size] | Page titles |
| `--font-size-3xl` | [size] | Hero text |

### Font Weights

| Variable | Weight | Usage |
|----------|--------|-------|
| `--font-weight-normal` | 400 | Regular text |
| `--font-weight-medium` | 500 | Emphasized text |
| `--font-weight-semibold` | 600 | Subheadings |
| `--font-weight-bold` | 700 | Headings, strong emphasis |

### Line Heights

| Variable | Value | Usage |
|----------|-------|-------|
| `--line-height-tight` | [value] | Headings |
| `--line-height-normal` | [value] | Body text |
| `--line-height-relaxed` | [value] | Long-form content |

### Font Loading

```html
<!-- If using Google Fonts or external fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=[Font+Name]:[weights]&display=swap" rel="stylesheet">
```

Or if using CSS imports:
```css
@import url('https://fonts.googleapis.com/css2?family=[Font+Name]:[weights]&display=swap');
```

## Spacing System

| Variable | Size | Usage |
|----------|------|-------|
| `--space-xs` | [size] | Minimal spacing |
| `--space-sm` | [size] | Small spacing |
| `--space-md` | [size] | Medium spacing (default) |
| `--space-lg` | [size] | Large spacing |
| `--space-xl` | [size] | Extra large spacing |
| `--space-2xl` | [size] | Section spacing |

## Component Styling Patterns

### [Component Name 1]

**File**: `frontend/src/components/[Component].tsx`

**Purpose**: [Brief description]

**CSS Classes/Pattern**:
```css
.component-name {
  /* Main container styles */
  property: value;
}

.component-name__element {
  /* BEM-style element */
  property: value;
}

.component-name--modifier {
  /* BEM-style modifier */
  property: value;
}
```

**Usage**:
```tsx
<div className="component-name">
  <div className="component-name__element">Content</div>
</div>
```

### [Component Name 2]

[Repeat structure for other key components]

## Layout Patterns

### Container Widths

| Breakpoint | Max Width | Usage |
|------------|-----------|-------|
| Mobile | 100% | Full width |
| Tablet | [width] | Tablet container |
| Desktop | [width] | Desktop container |
| Wide | [width] | Wide screen container |

### Grid System

[If using a grid system, document columns, gaps, breakpoints]

## Responsive Design

### Breakpoints

```css
/* Mobile first approach */
/* Base styles: Mobile (< 640px) */

@media (min-width: 640px) {  /* sm: Small tablets */
  /* Tablet styles */
}

@media (min-width: 768px) {  /* md: Tablets */
  /* Tablet landscape styles */
}

@media (min-width: 1024px) { /* lg: Laptops */
  /* Desktop styles */
}

@media (min-width: 1280px) { /* xl: Desktops */
  /* Large desktop styles */
}

@media (min-width: 1536px) { /* 2xl: Wide screens */
  /* Extra wide styles */
}
```

### Mobile Adaptations

Document key responsive changes:
- [Component/feature]: [How it adapts on mobile]
- [Component/feature]: [How it adapts on tablet]
- etc.

## Animation & Transitions

### Transition Timing

| Variable | Duration | Easing | Usage |
|----------|----------|--------|-------|
| `--transition-fast` | [duration] | ease-in-out | Micro-interactions |
| `--transition-base` | [duration] | ease-in-out | Standard transitions |
| `--transition-slow` | [duration] | ease-in-out | Page transitions |

### Common Animations

```css
/* Example animation patterns */
@keyframes [animation-name] {
  from {
    /* Start state */
  }
  to {
    /* End state */
  }
}

.animated-element {
  animation: [animation-name] [duration] [easing] [delay];
}
```

## Shadows & Depth

| Variable | Value | Usage |
|----------|-------|-------|
| `--shadow-sm` | [shadow] | Subtle elevation |
| `--shadow-md` | [shadow] | Card elevation |
| `--shadow-lg` | [shadow] | Modal/dialog elevation |
| `--shadow-xl` | [shadow] | Maximum elevation |

## Border Radius

| Variable | Size | Usage |
|----------|------|-------|
| `--radius-sm` | [size] | Small elements |
| `--radius-md` | [size] | Standard elements |
| `--radius-lg` | [size] | Large containers |
| `--radius-full` | [size] | Circular elements |

## Z-Index Scale

| Variable | Value | Usage |
|----------|-------|-------|
| `--z-base` | 1 | Base elements |
| `--z-dropdown` | 1000 | Dropdowns |
| `--z-sticky` | 1020 | Sticky elements |
| `--z-fixed` | 1030 | Fixed position elements |
| `--z-modal-backdrop` | 1040 | Modal backdrops |
| `--z-modal` | 1050 | Modal dialogs |
| `--z-popover` | 1060 | Popovers |
| `--z-tooltip` | 1070 | Tooltips |

## Accessibility

### Focus States
- All interactive elements must have visible focus indicators
- Focus ring color: [color]
- Focus ring width: [width]
- Focus ring offset: [offset]

### Color Contrast
- Text on background: [ratio] (WCAG [level] compliant)
- Primary on background: [ratio] (WCAG [level] compliant)
- Document any known contrast issues

### Font Sizes
- Minimum body text size: [size] (prevents mobile zoom on input focus)
- Minimum touch target size: [size] × [size]

## Theme Variants

[If the application supports multiple themes like dark mode]

### Light Theme
[Document light theme specific variables]

### Dark Theme
[Document dark theme specific variables]

### Theme Switching
[Document how theme switching is implemented]

## CSS Framework Configuration

[If using Tailwind, Bootstrap, Material-UI, etc.]

### Configuration File
**Location**: [e.g., `frontend/tailwind.config.js`]

[Include relevant configuration excerpts]

### Custom Extensions
[Document any custom extensions to the framework]

## Generator Usage Notes

### For Base Project
- Copy `frontend/src/styles/index.css` with core variables
- Include font preconnect links in `index.html`
- Copy CSS variable definitions to `:root`

### For Specific Capabilities
- `[capability_name]`: Add `.capability-*` classes to styles
- Ensure required color variables are defined
- Include any capability-specific font imports

### Style Customization
Document how generator should apply user preferences:
- Color scheme keywords → variable values mapping
- Font style keywords → font family mapping
- Theme keywords → theme variant selection

## Evidence

[Reference source files or documentation used to extract this styling information]
- Color values extracted from: [file path]
- Typography from: [file path]
- Component patterns observed in: [file paths]

# CSS (Cascading Style Sheets)

**Category**: Styling Language
**Website**: https://www.w3.org/Style/CSS/
**Documentation**: https://developer.mozilla.org/en-US/docs/Web/CSS

---

## Overview

CSS is the standard language for styling HTML documents. It controls layout, colors, fonts, animations, and responsive design across web pages.

---

## Key Features

**Selectors**: Target HTML elements for styling
**Box Model**: Margin, border, padding, content
**Flexbox**: One-dimensional layouts
**Grid**: Two-dimensional layouts
**Variables**: Reusable values (custom properties)
**Animations**: Keyframes and transitions
**Media Queries**: Responsive design

---

## Common Use Cases

- **Layout**: Flexbox, Grid, positioning
- **Typography**: Fonts, sizes, spacing
- **Colors**: Backgrounds, borders, shadows
- **Responsive Design**: Mobile-first layouts
- **Animations**: Transitions, keyframes
- **Theming**: Dark mode, color schemes

---

## Basic Syntax

```css
/* Selector */
.my-class {
  /* Property: value; */
  color: blue;
  font-size: 16px;
  margin: 10px;
}

/* ID selector */
#header {
  background: white;
}

/* Element selector */
p {
  line-height: 1.5;
}

/* Pseudo-class */
button:hover {
  background: lightblue;
}
```

---

## Layout

### Flexbox
```css
.container {
  display: flex;
  justify-content: space-between;  /* Horizontal alignment */
  align-items: center;             /* Vertical alignment */
  gap: 20px;                       /* Space between items */
}

.item {
  flex: 1;  /* Grow to fill space */
}
```

### Grid
```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);  /* 3 equal columns */
  gap: 20px;
}

.grid-item {
  grid-column: span 2;  /* Take 2 columns */
}
```

### Positioning
```css
.relative {
  position: relative;
  top: 10px;
  left: 20px;
}

.absolute {
  position: absolute;
  top: 0;
  right: 0;
}

.fixed {
  position: fixed;  /* Fixed to viewport */
  bottom: 20px;
  right: 20px;
}
```

---

## CSS Variables

```css
:root {
  --primary-color: #3498db;
  --spacing: 16px;
  --border-radius: 4px;
}

.button {
  background: var(--primary-color);
  padding: var(--spacing);
  border-radius: var(--border-radius);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --primary-color: #5dade2;
  }
}
```

---

## Responsive Design

### Media Queries
```css
/* Mobile first */
.container {
  width: 100%;
  padding: 10px;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    width: 750px;
    margin: 0 auto;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    width: 1000px;
  }
}
```

### Responsive Units
```css
/* Relative to font size */
p {
  font-size: 1rem;        /* 16px by default */
  padding: 0.5em;         /* Relative to element font size */
}

/* Viewport units */
.hero {
  height: 100vh;          /* 100% of viewport height */
  width: 50vw;            /* 50% of viewport width */
}

/* Responsive font sizing */
h1 {
  font-size: clamp(1.5rem, 5vw, 3rem);  /* Min, preferred, max */
}
```

---

## Animations

### Transitions
```css
.button {
  background: blue;
  transition: background 0.3s ease;
}

.button:hover {
  background: darkblue;
}
```

### Keyframes
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.element {
  animation: fadeIn 0.5s ease-in-out;
}
```

---

## Best Practices

**DO**:
- Use CSS variables for theming
- Mobile-first responsive design
- Use flexbox/grid for layouts
- Minimize specificity conflicts
- Use semantic class names (BEM, SMACSS)
- Optimize for performance (avoid expensive selectors)

**DON'T**:
- Don't use !important (increases specificity)
- Don't use inline styles (hard to maintain)
- Don't use IDs for styling (high specificity)
- Don't overuse absolute positioning
- Don't forget vendor prefixes for compatibility

---

## Common Patterns

### Dark Mode
```css
:root {
  --bg-color: white;
  --text-color: black;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-color: #1a1a1a;
    --text-color: white;
  }
}

body {
  background: var(--bg-color);
  color: var(--text-color);
}
```

### Card Component
```css
.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: box-shadow 0.3s;
}

.card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
```

### Loading Spinner
```css
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  border: 3px solid rgba(0, 0, 0, 0.1);
  border-top-color: blue;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}
```

---

## CSS Frameworks

**Tailwind CSS**: Utility-first CSS
**Bootstrap**: Component library
**Bulma**: Flexbox-based framework
**Material-UI**: Material Design components

**Vanilla CSS Advantages**:
- No build step
- Full control
- No learning curve
- Better performance (no unused CSS)

---

## Performance

**Optimization**:
- Minimize repaints and reflows
- Use transform/opacity for animations (GPU accelerated)
- Avoid complex selectors (e.g., `div > p + span`)
- Use will-change for animations
- Minify and compress CSS

**Critical CSS**:
```html
<!-- Inline critical CSS for above-the-fold content -->
<style>
  /* Critical styles here */
</style>

<!-- Load rest async -->
<link rel="preload" href="styles.css" as="style" onload="this.rel='stylesheet'">
```

---

## Alternatives

**Sass/SCSS**: CSS preprocessor (variables, nesting, mixins)
**Less**: Another CSS preprocessor
**Styled Components**: CSS-in-JS for React
**Tailwind**: Utility-first framework
**CSS Modules**: Scoped CSS

**Why Vanilla CSS**:
- No build step required
- Native browser support
- CSS Variables provide theming
- Modern CSS is very powerful

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Technologies often used with**: [[react-hooks]], [[typescript]]

# Styling System: ITFC Analysis

## CSS Architecture

Approach: Global CSS with CSS custom properties
Location: frontend/src/styles/index.css
Framework: None (vanilla CSS)

## Color Palette

### Ipswich Town Brand Colors

| Variable | Hex | Usage |
|----------|-----|-------|
| Primary base | #1a365d | Sidebar, headings |
| Primary dark | #142850 | Hover states |
| Accent base | #3182ce | Links, highlights |
| Success | #38a169 | Success messages |
| Error | #e53e3e | Error messages |

## Typography

Font family: System font stack (-apple-system, BlinkMacSystemFont, Segoe UI)
Base size: 16px
Line height: 1.5
Code font: SF Mono, monospace

## Spacing

- xs: 0.25rem
- sm: 0.5rem
- md: 1rem
- lg: 1.5rem
- xl: 2rem

## Component Patterns

### ChatContainer
Main chat interface with message list

### DataViewer
Query result tables with Ipswich blue headers

### QueryChart
Chart.js visualizations using brand colors

## Responsive Design

Mobile-first approach with breakpoints at 640px, 768px, 1024px

## Evidence
Extracted from frontend/src/styles/index.css and kb-scan-styles.json

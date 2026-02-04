# Data Visualization

**Feature ID**: visualization.chartjs
**Capability**: data-visualization
**Technologies**: chartjs, react-hooks

---

## Overview

Automatic data visualization using Chart.js with intelligent data detection, multiple chart types (bar, line, pie), and custom Ipswich Town color palette.

**Key characteristics**:
- Auto-detection of chartable data (numeric columns)
- Chart type selection (bar for categories, line for time series, pie for distributions)
- 8-color Ipswich Town palette
- Responsive charts with legend
- CSV export for raw data
- Chart rendering within chat messages

---

## File Structure

```
frontend/src/
  components/
    QueryChart.tsx         # Chart component
    ChatMessage.tsx        # Integrates chart rendering
```

---

## Implementation Patterns

### 1. Query Chart (QueryChart.tsx)

**Purpose**: Chart.js wrapper component with auto-detection and type selection

**Interface**:
```typescript
interface QueryChartProps {
  columns: string[];
  data: any[][];
}

export function QueryChart({ columns, data }: QueryChartProps): JSX.Element
```

**Complete Flow**:
1. Analyze data structure:
   - Find numeric columns (columns with all numeric values)
   - Find categorical columns (strings, dates)
2. Determine chart type:
   - If 1 categorical + 1 numeric: bar chart
   - If date column + numeric: line chart
   - If categories sum to ~100: pie chart
   - Default: bar chart
3. Prepare chart data:
   - labels: categorical column values
   - dataset: numeric column values
   - backgroundColor: Ipswich color palette
4. Render Chart.js component (Bar, Line, or Pie)

**Chart Type Detection**:
```typescript
function detectChartType(columns, data):
  numericCols = columns with all numeric values
  categoricalCols = columns with string/date values

  if categoricalCols.length = 1 and numericCols.length = 1:
    if categoricalCol contains dates:
      return 'line'  // Time series
    else:
      return 'bar'   // Category comparison

  if numericCols sum to ~100 (±5):
    return 'pie'  // Distribution/percentage

  return 'bar'  // Default
```

**Ipswich Color Palette**:
```typescript
const IPSWICH_COLORS = [
  '#1a365d',  // Primary blue
  '#3182ce',  // Accent blue
  '#2c5282',  // Medium blue
  '#4299e1',  // Light blue
  '#63b3ed',  // Sky blue
  '#90cdf4',  // Pale blue
  '#bee3f8',  // Very pale blue
  '#ebf8ff',  // Almost white blue
];
```

**All Behaviors**:
- Auto-detection of chartable data
- Responsive charts (width adapts to container)
- Legend with color squares
- Tooltips on hover
- Chart title from query context
- Fallback to table if data not chartable
- Maximum 8 categories (more → "Show table instead")

---

### 2. Chat Message Integration (ChatMessage.tsx)

**Purpose**: Integrates chart rendering within message display

**Complete Flow**:
1. Render assistant message text (markdown)
2. If message has executedQueries with results:
   - For each query result:
     - Check if data is chartable (has numeric columns)
     - If chartable: render QueryChart component
     - Always render table below chart
     - Add CSV export button

**All Behaviors**:
- Chart displayed above table
- Both visualizations shown (chart + table)
- CSV export works for both
- Chart collapses on mobile (<768px)

---

## Usage Across Projects

**Used in**:
- [db-chat-nl-master](../projects/db-chat-nl-master/README.md) - Query result visualization

---

## Related Technologies

- **[Chart.js](../technologies/chartjs.md)** - Charting library
- **[React Hooks](../technologies/react-hooks.md)** - Component state

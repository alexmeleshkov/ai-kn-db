# Chart.js

**Technology**: Chart.js 4+ with react-chartjs-2
**Category**: Visualization Library

---

## Overview

JavaScript charting library for rendering bar, line, and pie charts with React wrapper.

---

## Usage Files

- `frontend/src/components/QueryChart.tsx`
- `frontend/src/components/ChatMessage.tsx`

---

## Complete Usage Patterns

### Chart Component (QueryChart.tsx)

**Pattern**:
```typescript
import { Bar, Line, Pie } from 'react-chartjs-2';

const chartData = {
  labels: ['Jan', 'Feb', 'Mar'],
  datasets: [{
    label: 'Sales',
    data: [100, 200, 150],
    backgroundColor: IPSWICH_COLORS,
  }]
};

const options = {
  responsive: true,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Chart Title' }
  }
};

<Bar data={chartData} options={options} />
```

**All Behaviors**:
- Bar charts for category comparison
- Line charts for time series
- Pie charts for distributions
- Responsive sizing
- Legend and tooltips
- Custom color palette (Ipswich blue theme)

---

## Configuration

```typescript
IPSWICH_COLORS = ['#1a365d', '#3182ce', '#2c5282', '#4299e1', '#63b3ed', '#90cdf4', '#bee3f8', '#ebf8ff']
```

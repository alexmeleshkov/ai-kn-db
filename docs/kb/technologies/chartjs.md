# Chart.js

**Category**: Data Visualization Library
**Website**: https://www.chartjs.org/
**Documentation**: https://www.chartjs.org/docs/

---

## Overview

Chart.js is a simple yet flexible JavaScript charting library for creating responsive, animated charts. It supports 8 chart types out of the box and can be extended with plugins.

---

## Key Features

**Responsive**: Charts resize automatically
**Animated**: Smooth animations on load and update
**Canvas-based**: Uses HTML5 Canvas for rendering
**Extensible**: Plugin system for custom behavior
**Mix Types**: Combine different chart types in one chart
**Accessible**: ARIA labels for screen readers

---

## Common Chart Types

- **Line**: Time series, trends
- **Bar**: Comparisons, categorical data
- **Pie/Doughnut**: Proportions, percentages
- **Scatter**: Correlations, distributions
- **Radar**: Multi-dimensional data
- **Polar Area**: Cyclic data
- **Bubble**: 3-dimensional data
- **Mixed**: Combine multiple types

---

## Prerequisites

**Installation**:

**CDN**:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

**npm**:
```bash
npm install chart.js

# React wrapper
npm install react-chartjs-2
```

---

## Basic Usage

### Vanilla JavaScript
```javascript
const ctx = document.getElementById('myChart');

new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Red', 'Blue', 'Yellow'],
    datasets: [{
      label: 'Votes',
      data: [12, 19, 3],
      backgroundColor: ['red', 'blue', 'yellow']
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});
```

### React (with react-chartjs-2)
```typescript
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement);

function BarChart() {
  const data = {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [{
      label: 'Sales',
      data: [65, 59, 80],
      backgroundColor: 'rgba(75, 192, 192, 0.6)'
    }]
  };

  return <Bar data={data} />;
}
```

---

## Chart Types

### Line Chart
```javascript
new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr'],
    datasets: [{
      label: 'Revenue',
      data: [10, 20, 15, 25],
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1  // Curve smoothness
    }]
  }
});
```

### Pie Chart
```javascript
new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ['Chrome', 'Firefox', 'Safari'],
    datasets: [{
      data: [55, 25, 20],
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
    }]
  }
});
```

### Scatter Plot
```javascript
new Chart(ctx, {
  type: 'scatter',
  data: {
    datasets: [{
      label: 'Data Points',
      data: [
        { x: 10, y: 20 },
        { x: 15, y: 25 },
        { x: 20, y: 15 }
      ],
      backgroundColor: 'rgb(255, 99, 132)'
    }]
  }
});
```

---

## Common Patterns

### Dynamic Updates
```javascript
function updateChart(chart, newData) {
  chart.data.datasets[0].data = newData;
  chart.update();
}

// Update chart when data changes
updateChart(myChart, [30, 40, 50]);
```

### Responsive Configuration
```javascript
const options = {
  responsive: true,
  maintainAspectRatio: false,  // Fill container
  plugins: {
    legend: {
      display: true,
      position: 'top'
    },
    tooltip: {
      enabled: true,
      callbacks: {
        label: function(context) {
          return context.label + ': ' + context.parsed.y + ' units';
        }
      }
    }
  }
};
```

### Custom Colors
```javascript
const data = {
  labels: ['A', 'B', 'C'],
  datasets: [{
    data: [10, 20, 30],
    backgroundColor: [
      'rgba(255, 99, 132, 0.5)',
      'rgba(54, 162, 235, 0.5)',
      'rgba(255, 206, 86, 0.5)'
    ],
    borderColor: [
      'rgba(255, 99, 132, 1)',
      'rgba(54, 162, 235, 1)',
      'rgba(255, 206, 86, 1)'
    ],
    borderWidth: 1
  }]
};
```

---

## Best Practices

**DO**:
- Destroy charts before creating new ones
- Use responsive: true for mobile support
- Register components before use (Chart.js 3+)
- Use plugins for advanced features
- Limit data points for performance (lazy load if needed)

**DON'T**:
- Don't create multiple charts on same canvas
- Don't forget to destroy charts on unmount
- Don't use too many data points (causes lag)
- Don't skip axis labels (accessibility)
- Don't use default colors (not accessible)

---

## React Integration

```typescript
import { useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';

function ChartComponent({ data }: { data: number[] }) {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    // Destroy previous chart
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    // Create new chart
    chartInstance.current = new Chart(chartRef.current, {
      type: 'bar',
      data: {
        labels: ['A', 'B', 'C'],
        datasets: [{ data }]
      }
    });

    // Cleanup
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [data]);

  return <canvas ref={chartRef} />;
}
```

---

## Performance

**Large Datasets**:
- Use decimation plugin (reduce visible points)
- Enable spanGaps: false
- Disable animations for large datasets
- Use downsampling before rendering

**Optimization**:
```javascript
const options = {
  animation: false,  // Disable for large data
  parsing: false,    // Pre-parsed data
  normalized: true,  // Data already normalized
  elements: {
    point: {
      radius: 0  // Hide points on line chart
    }
  }
};
```

---

## Alternatives

**D3.js**: More powerful, steeper learning curve
**Recharts**: React-specific, declarative API
**Victory**: React components, highly customizable
**ApexCharts**: Modern, feature-rich
**Plotly**: Scientific charts, 3D support

**Why Chart.js**:
- Simple API
- Good documentation
- Responsive by default
- Works with vanilla JS and frameworks
- Lightweight (58kb gzipped)

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Features**: [[data-visualization]]
**Technologies often used with**: [[react-hooks]], [[typescript]]

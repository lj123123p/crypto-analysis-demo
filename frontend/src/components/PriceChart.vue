<template>
  <div class="price-chart">
    <div class="chart-title">价格走势图 (模拟数据)</div>
    <div class="chart-disclaimer">以下走势数据为模拟生成，仅用于技术演示</div>
    <canvas ref="chartContainer" class="chart-container"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  TimeScale,
  Tooltip,
  Filler,
} from 'chart.js'
import 'chartjs-adapter-date-fns'

Chart.register(LineController, LineElement, PointElement, LinearScale, TimeScale, Tooltip, Filler)

const props = defineProps({
  data: { type: Array, default: () => [] },
  coin: { type: String, default: 'BTC' },
})

const chartContainer = ref(null)
let chartInstance = null

watch(
  () => props.data,
  async (val) => {
    await nextTick()
    if (val && val.length) renderChart(val)
  },
  { deep: false }
)

watch(
  () => props.coin,
  () => {
    if (chartInstance) {
      chartInstance.destroy()
      chartInstance = null
    }
  }
)

function renderChart(data) {
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
  if (!chartContainer.value || !data.length) return

  const ctx = chartContainer.value.getContext('2d')
  const points = data.map(d => ({ x: d.timestamp, y: d.close }))
  const isUp = data.length > 1 && data[data.length - 1].close >= data[0].close
  const lineColor = isUp ? '#00e676' : '#ff1744'
  const fillColor = isUp ? 'rgba(0, 230, 118, 0.08)' : 'rgba(255, 23, 68, 0.08)'

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [
        {
          label: props.coin + ' 价格',
          data: points,
          borderColor: lineColor,
          backgroundColor: fillColor,
          borderWidth: 2,
          pointRadius: 0,
          pointHitRadius: 5,
          fill: true,
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 800 },
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        tooltip: {
          enabled: true,
          backgroundColor: 'rgba(17, 24, 39, 0.95)',
          titleColor: '#e0e6f0',
          bodyColor: '#8899aa',
          borderColor: '#1e3a5f',
          borderWidth: 1,
          padding: 10,
          callbacks: {
            title: (items) => {
              const d = new Date(items[0].parsed.x)
              return d.toLocaleDateString('zh-CN')
            },
            label: (ctx) => ctx.parsed.y.toFixed(2) + ' USDT',
          },
        },
      },
      scales: {
        x: {
          type: 'time',
          time: { unit: 'day', displayFormats: { day: 'MM/dd' } },
          grid: { color: 'rgba(30, 58, 95, 0.2)', drawBorder: false },
          ticks: { color: '#8899aa', maxRotation: 0 },
        },
        y: {
          grid: { color: 'rgba(30, 58, 95, 0.2)', drawBorder: false },
          ticks: {
            color: '#8899aa',
            callback: (val) => val.toLocaleString(),
          },
        },
      },
    },
  })
}

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
})
</script>

<style scoped>
.price-chart {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 20px;
  margin-bottom: 20px;
}
.chart-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--accent-blue);
  margin-bottom: 4px;
}
.chart-disclaimer {
  font-size: 11px;
  color: var(--accent-yellow);
  opacity: 0.7;
  margin-bottom: 12px;
}
.chart-container {
  width: 100%;
  height: 180px !important;
  max-height: 180px;
}
</style>

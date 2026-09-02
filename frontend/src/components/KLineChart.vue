<template>
  <div class="kline-chart">
    <div class="chart-header">
      <span class="chart-title">K 线图 (模拟数据)</span>
      <el-select v-model="localDays" size="small" @change="onDaysChange" style="width:100px">
        <el-option label="7天" :value="7" />
        <el-option label="30天" :value="30" />
        <el-option label="90天" :value="90" />
        <el-option label="365天" :value="365" />
      </el-select>
    </div>
    <div class="chart-disclaimer">以下K线数据为模拟生成，仅用于技术演示</div>
    <canvas ref="chartContainer" class="chart-container"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount, nextTick } from 'vue'
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
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['update:days'])

const localDays = ref(90)
const chartContainer = ref(null)
let chartInstance = null

function onDaysChange(val) {
  emit('update:days', val)
}

// ---- Custom candlestick plugin ----
const candlestickPlugin = {
  id: 'candlestick',
  afterDraw(chart) {
    const { ctx, scales, data: chartData } = chart
    if (!chartData.datasets.length) return
    const dataset = chartData.datasets[0]
    const xScale = scales.x
    const yScale = scales.y
    if (!xScale || !yScale) return

    const barWidth = Math.max(2, (xScale.getPixelForValue(1) - xScale.getPixelForValue(0)) * 0.6)

    ctx.save()
    dataset.data.forEach((d) => {
      if (!d) return
      const x = xScale.getPixelForValue(d.x)
      const yHigh = yScale.getPixelForValue(d.h)
      const yLow = yScale.getPixelForValue(d.l)
      const yOpen = yScale.getPixelForValue(d.o)
      const yClose = yScale.getPixelForValue(d.c)

      const isUp = d.c >= d.o
      const color = isUp ? '#00e676' : '#ff1744'

      // Wick (high-low line)
      ctx.beginPath()
      ctx.moveTo(x, yHigh)
      ctx.lineTo(x, yLow)
      ctx.strokeStyle = color
      ctx.lineWidth = 1.5
      ctx.stroke()

      // Body (open-close rectangle)
      const bodyTop = Math.min(yOpen, yClose)
      const bodyHeight = Math.max(Math.abs(yClose - yOpen), 1)
      ctx.fillStyle = color
      ctx.fillRect(x - barWidth / 2, bodyTop, barWidth, bodyHeight)
    })
    ctx.restore()
  },
}

// ---- Watch data ----
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
  (newCoin, oldCoin) => {
    if (oldCoin && newCoin !== oldCoin) {
      destroyChart()
    }
  }
)

function destroyChart() {
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }
}

function renderChart(data) {
  destroyChart()
  if (!chartContainer.value || !data.length) return

  const ohlc = data.map(d => ({
    x: d.timestamp,
    o: d.open,
    h: d.high,
    l: d.low,
    c: d.close,
  }))

  // Add a dummy line dataset so scales are auto-calculated
  const closes = ohlc.map(d => ({ x: d.x, y: d.c }))

  // Unregister then re-register plugin to avoid duplicates
  try { Chart.unregister(candlestickPlugin) } catch (e) {}
  Chart.register(candlestickPlugin)

  chartInstance = new Chart(chartContainer.value, {
    type: 'line',
    data: {
      datasets: [
        {
          label: props.coin + ' 收盘价',
          data: closes,
          borderColor: 'rgba(0, 212, 255, 0.3)',
          backgroundColor: 'transparent',
          borderWidth: 1,
          pointRadius: 0,
          pointHitRadius: 5,
          tension: 0.2,
          // Hide from legend/tooltip by default
          order: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 300 },
      plugins: {
        legend: { display: false },
        tooltip: {
          enabled: true,
          backgroundColor: 'rgba(17, 24, 39, 0.95)',
          titleColor: '#e0e6f0',
          bodyColor: '#8899aa',
          borderColor: '#1e3a5f',
          borderWidth: 1,
          padding: 12,
          callbacks: {
            title: (items) => {
              const d = new Date(items[0].parsed.x)
              return d.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
            },
            label: (ctx) => {
              const idx = ctx.dataIndex
              const d = ohlc[idx]
              if (!d) return ''
              return [
                '开: ' + d.o.toFixed(2),
                '高: ' + d.h.toFixed(2),
                '低: ' + d.l.toFixed(2),
                '收: ' + d.c.toFixed(2),
              ]
            },
          },
        },
      },
      scales: {
        x: {
          type: 'time',
          time: { unit: 'day', displayFormats: { day: 'MM/dd' } },
          grid: { color: 'rgba(30, 58, 95, 0.3)', drawBorder: false },
          ticks: { color: '#8899aa', maxRotation: 0, maxTicksLimit: 12 },
        },
        y: {
          grid: { color: 'rgba(30, 58, 95, 0.3)', drawBorder: false },
          ticks: {
            color: '#8899aa',
            callback: (val) => val.toLocaleString(),
          },
        },
      },
    },
    plugins: [candlestickPlugin],
  })
}

onBeforeUnmount(() => {
  destroyChart()
})
</script>

<style scoped>
.kline-chart {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 16px;
}
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}
.chart-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent-cyan);
}
.chart-disclaimer {
  font-size: 11px;
  color: var(--accent-yellow);
  opacity: 0.7;
  margin-bottom: 8px;
}
.chart-container {
  width: 100%;
  height: 360px !important;
  max-height: 360px;
  display: block;
  max-height: 360px;
  display: block;
}
</style>
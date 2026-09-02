<template>
  <div class="ai-panel">
    <div class="panel-title">
      <el-icon style="margin-right:6px; color: var(--accent-cyan)"><Monitor /></el-icon>
      模拟AI分析结果
    </div>
    <div class="panel-subtitle">以下分析内容完全由模拟算法生成，不可作为真实交易参考</div>

    <div v-if="!result" class="empty-state">
      <el-icon :size="48" color="#334"><Cpu /></el-icon>
      <p>输入新闻并点击"开始模拟分析"</p>
      <p class="empty-hint">系统将模拟AI模型对市场进行分析</p>
    </div>

    <div v-else class="result-content">
      <div class="result-header">
        <span class="result-coin">{{ result.coin }}/USDT</span>
        <span :class="['result-price', result.trend === '上涨' ? 'up' : result.trend === '下跌' ? 'down' : '']">
          {{ result.current_price.toFixed(2) }}
        </span>
      </div>

      <div class="indicator-grid">
        <div class="indicator-item">
          <span class="indicator-label">趋势</span>
          <span :class="['indicator-value', trendClass(result.trend)]">{{ result.trend }}</span>
        </div>
        <div class="indicator-item">
          <span class="indicator-label">RSI(14)</span>
          <span :class="['indicator-value', rsiClass(result.rsi)]">{{ result.rsi }}</span>
        </div>
        <div class="indicator-item">
          <span class="indicator-label">情绪</span>
          <span :class="['indicator-value', sentimentClass(result.sentiment)]">{{ result.sentiment }}</span>
        </div>
        <div class="indicator-item">
          <span class="indicator-label">模拟预测</span>
          <span :class="['indicator-value', predClass(result.prediction)]">{{ result.prediction }}</span>
        </div>
        <div class="indicator-item">
          <span class="indicator-label">模拟支撑</span>
          <span class="indicator-value down">{{ result.support.toFixed(2) }}</span>
        </div>
        <div class="indicator-item">
          <span class="indicator-label">模拟阻力</span>
          <span class="indicator-value up">{{ result.resistance.toFixed(2) }}</span>
        </div>
      </div>

      <div class="analysis-text">
        <div class="analysis-label">模拟综合评述</div>
        <p>{{ result.summary }}</p>
      </div>

      <div class="disclaimer-box">
        ⚠ {{ result.disclaimer }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Monitor, Cpu } from '@element-plus/icons-vue'

const props = defineProps({
  result: { type: Object, default: null },
})

function trendClass(v) {
  if (v === '上涨') return 'up'
  if (v === '下跌') return 'down'
  return ''
}
function rsiClass(v) {
  if (v >= 70) return 'up'
  if (v <= 30) return 'down'
  return ''
}
function sentimentClass(v) {
  if (v && v.includes('多')) return 'up'
  if (v && v.includes('空')) return 'down'
  return ''
}
function predClass(v) {
  if (v && v.includes('多')) return 'up'
  if (v && v.includes('空')) return 'down'
  return ''
}
</script>

<style scoped>
.ai-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 12px;
  height: 100%;
}
.panel-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--accent-cyan);
  display: flex;
  align-items: center;
  margin-bottom: 4px;
}
.panel-subtitle {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 10px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px 12px;
  color: #445;
  text-align: center;
}
.empty-state p {
  margin-top: 12px;
  font-size: 14px;
}
.empty-hint {
  font-size: 12px !important;
  color: #334;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 10px;
}
.result-coin {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
}
.result-price {
  font-size: 15px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}
.result-price.up { color: var(--accent-green); }
.result-price.down { color: var(--accent-red); }

.indicator-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
  margin-bottom: 10px;
}
.indicator-item {
  background: rgba(10, 14, 23, 0.5);
  border-radius: 8px;
  padding: 10px;
  text-align: center;
}
.indicator-label {
  display: block;
  font-size: 11px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}
.indicator-value {
  font-size: 14px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}
.indicator-value.up { color: var(--accent-green); }
.indicator-value.down { color: var(--accent-red); }

.analysis-text {
  background: rgba(0, 212, 255, 0.04);
  border: 1px solid rgba(0, 212, 255, 0.12);
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 8px;
}
.analysis-label {
  font-size: 12px;
  color: var(--accent-cyan);
  margin-bottom: 8px;
  font-weight: 600;
}
.analysis-text p {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-secondary);
}

.disclaimer-box {
  font-size: 12px;
  color: var(--accent-yellow);
  background: rgba(255, 214, 0, 0.06);
  border: 1px solid rgba(255, 214, 0, 0.15);
  border-radius: 8px;
  padding: 8px 10px;
  line-height: 1.5;
}
</style>

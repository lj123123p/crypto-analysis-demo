<template>
  <div class="dashboard">
    <!-- Risk Warning -->
    <RiskWarning />

    <!-- Top Bar: Coin Selector + Price Info -->
    <div class="top-bar">
      <CoinSelector v-model="currentCoin" :coin-list="coinList" />
      <div class="price-info">
        <span class="price-label">当前价格</span>
        <span class="price-value" :class="priceDir">{{ currentPrice }}</span>
      </div>
    </div>

    <!-- Main Area: KLine + Right Panel -->
    <div class="main-area">
      <div class="main-chart">
        <KLineChart
          :data="historyData"
          :coin="currentCoin"
          :loading="historyLoading"
          @update:days="onDaysChange"
        />
      </div>
      <div class="side-panel">
        <NewsInput
          v-model="newsText"
          :loading="analyzeLoading"
          @analyze="onAnalyze"
        />
        <AIAnalysisPanel :result="analyzeResult" />
      </div>
    </div>

    <!-- Price Chart -->
    <PriceChart
      :data="historyData"
      :coin="currentCoin"
    />

    <!-- Footer Risk -->
    <div class="footer-risk">
      <p>我国不承认虚拟货币的法定地位，禁止虚拟货币交易行为。本站所有内容均为模拟生成，不构成任何投资建议。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import RiskWarning from '../components/RiskWarning.vue'
import CoinSelector from '../components/CoinSelector.vue'
import KLineChart from '../components/KLineChart.vue'
import PriceChart from '../components/PriceChart.vue'
import NewsInput from '../components/NewsInput.vue'
import AIAnalysisPanel from '../components/AIAnalysisPanel.vue'
import { fetchHistory, postAnalyze, fetchCoins } from '../utils/api'

const currentCoin = ref('BTC')
const coinList = ref([])
const historyData = ref([])
const historyDays = ref(90)
const historyLoading = ref(false)
const newsText = ref('')
const analyzeLoading = ref(false)
const analyzeResult = ref(null)
const priceDir = ref('')

const currentPrice = computed(() => {
  if (historyData.value.length > 0) {
    const last = historyData.value[historyData.value.length - 1].close
    return last.toFixed(2) + ' USDT'
  }
  return '--'
})

watch(currentCoin, () => { loadHistory() })

function onDaysChange(days) {
  historyDays.value = days
  loadHistory()
}

async function loadHistory() {
  historyLoading.value = true
  try {
    const res = await fetchHistory(currentCoin.value, historyDays.value)
    historyData.value = res.data
  } catch (e) {
    ElMessage.error('获取行情数据失败')
    historyData.value = []
  } finally {
    historyLoading.value = false
  }
}

async function onAnalyze(news) {
  if (!news.trim()) {
    ElMessage.warning('请输入新闻内容')
    return
  }
  analyzeLoading.value = true
  analyzeResult.value = null
  try {
    const res = await postAnalyze(currentCoin.value, news)
    analyzeResult.value = res
  } catch (e) {
    ElMessage.error('分析请求失败: ' + (e.response?.data?.detail || e.message))
  } finally {
    analyzeLoading.value = false
  }
}

onMounted(async () => {
  try {
    const res = await fetchCoins()
    coinList.value = res.coins
  } catch {
    coinList.value = [
      { symbol: 'BTC', name: 'Bitcoin' },
      { symbol: 'ETH', name: 'Ethereum' },
      { symbol: 'SOL', name: 'Solana' },
      { symbol: 'BNB', name: 'BNB' },
    ]
  }
  loadHistory()
})
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 16px 24px;
}

/* Top Bar */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.price-info {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 8px 18px;
  white-space: nowrap;
}
.price-label {
  font-size: 12px;
  color: var(--text-secondary);
}
.price-value {
  font-size: 20px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: var(--accent-green);
}

/* Main Area: KLine + Side Panel */
.main-area {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 12px;
  margin-bottom: 12px;
  align-items: start;
}
.main-chart {
  min-width: 0;
}
.side-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
  overflow-y: auto;
}

/* Mobile */
@media (max-width: 900px) {
  .main-area {
    grid-template-columns: 1fr;
    min-height: auto;
  }
  .side-panel {
    max-height: none;
  }
}
@media (max-width: 768px) {
  .dashboard {
    padding: 8px 8px 16px;
  }
  .top-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .price-info {
    justify-content: center;
  }
}

.footer-risk {
  text-align: center;
  padding: 16px;
  border-top: 1px solid var(--border-color);
  margin-top: 8px;
}
.footer-risk p {
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.6;
}
</style>
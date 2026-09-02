<template>
  <div class="news-input">
    <div class="panel-title">时事新闻输入</div>
    <div class="panel-subtitle">输入与虚拟币相关的新闻文本，模拟AI将据此进行分析</div>
    <el-input
      v-model="localNews"
      type="textarea"
      :rows="3"
      placeholder="请输入新闻内容，例如：&quot;某机构宣布将推出比特币ETF产品，市场情绪高涨&quot;"
      maxlength="500"
      show-word-limit
    />
    <div class="news-hints">
      <span class="hint-label">快速填入:</span>
      <el-tag
        v-for="(h, i) in hints"
        :key="i"
        size="small"
        class="hint-tag"
        @click="localNews = h"
      >
        {{ h.slice(0, 12) }}...
      </el-tag>
    </div>
    <el-button
      type="primary"
      :loading="loading"
      class="analyze-btn"
      @click="handleAnalyze"
      :disabled="!localNews.trim()"
    >
      <el-icon style="margin-right:6px"><TrendCharts /></el-icon>
      开始模拟分析
    </el-button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { TrendCharts } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['update:modelValue', 'analyze'])

const localNews = ref(props.modelValue)

const hints = [
  '某机构宣布推出比特币ETF，市场情绪高涨，机构资金持续流入',
  '监管机构发布新规，加强虚拟货币交易监管，市场恐慌情绪蔓延',
  '以太坊网络完成重大升级，生态项目快速增长，开发者数量创新高',
  '宏观经济数据不及预期，美联储降息预期升温，风险资产普涨',
]

function handleAnalyze() {
  if (localNews.value.trim()) {
    emit('analyze', localNews.value)
  }
}
</script>

<style scoped>
.news-input {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 12px;
  height: 100%;
}
.panel-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.panel-subtitle {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}
.news-hints {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  flex-wrap: wrap;
}
.hint-label {
  font-size: 12px;
  color: var(--text-secondary);
  white-space: nowrap;
}
.hint-tag {
  cursor: pointer;
  transition: all 0.2s;
}
.hint-tag:hover {
  opacity: 0.8;
  transform: translateY(-1px);
}
.analyze-btn {
  margin-top: 10px;
  width: 100%;
}
</style>

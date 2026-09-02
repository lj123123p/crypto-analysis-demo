<template>
  <div class="coin-selector">
    <div class="selector-label">选择币种</div>
    <div class="coin-buttons">
      <button
        v-for="c in coinList"
        :key="c.symbol"
        :class="['coin-btn', { active: modelValue === c.symbol }]"
        @click="('update:modelValue', c.symbol)"
      >
        <span class="coin-symbol">{{ c.symbol }}</span>
        <span class="coin-name">{{ c.name }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: String, default: 'BTC' },
  coinList: { type: Array, default: () => [] },
})
defineEmits(['update:modelValue'])
</script>

<style scoped>
.coin-selector {
  margin-bottom: 20px;
}
.selector-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 10px;
  letter-spacing: 1px;
}
.coin-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.coin-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 28px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-secondary);
  font-family: inherit;
}
.coin-btn:hover {
  border-color: var(--accent-cyan);
  background: var(--bg-card-hover);
  color: var(--text-primary);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.1);
}
.coin-btn.active {
  border-color: var(--accent-cyan);
  background: rgba(0, 212, 255, 0.1);
  color: var(--accent-cyan);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
}
.coin-symbol {
  font-size: 18px;
  font-weight: 700;
}
.coin-name {
  font-size: 11px;
  opacity: 0.7;
}
</style>

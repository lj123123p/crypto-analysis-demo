<template>
  <div class="risk-warning">
    <div class="warning-icon">⚠</div>
    <div class="warning-text">
      <strong>风险提示：</strong>
      我国不承认虚拟货币的法定地位，禁止虚拟货币交易。
      本站所有行情、分析、预测均为<em>模拟推演</em>，仅用于技术学习演示，
      <strong>绝不构成任何投资建议，不可作为交易依据。</strong>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.risk-warning {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 20px;
  background: linear-gradient(135deg, rgba(255, 23, 68, 0.12), rgba(255, 23, 68, 0.06));
  border: 1px solid rgba(255, 23, 68, 0.3);
  border-radius: var(--radius);
  margin-bottom: 20px;
  animation: warningPulse 3s ease-in-out infinite;
}

@keyframes warningPulse {
  0%, 100% { border-color: rgba(255, 23, 68, 0.3); }
  50% { border-color: rgba(255, 23, 68, 0.6); }
}

.warning-icon {
  font-size: 24px;
  flex-shrink: 0;
  animation: shake 2s ease-in-out infinite;
}

@keyframes shake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-5deg); }
  75% { transform: rotate(5deg); }
}

.warning-text {
  font-size: 13px;
  line-height: 1.6;
  color: #ff8a9e;
}

.warning-text strong {
  color: #ff1744;
}

.warning-text em {
  color: #ffd600;
  font-style: normal;
  font-weight: 600;
}
</style>

<script setup>
import { ref } from 'vue'

const loading = ref(false)
const result = ref(null)
const error = ref('')
const elapsed = ref(0)

async function testConnection() {
  loading.value = true
  result.value = null
  error.value = ''

  const startedAt = performance.now()

  try {
    const response = await fetch('/api/health')
    const data = await response.json().catch(() => null)

    if (!response.ok) {
      throw new Error(data?.detail ?? `HTTP ${response.status} ${response.statusText}`)
    }

    result.value = data
  } catch (err) {
    error.value = err instanceof Error ? err.message : String(err)
  } finally {
    elapsed.value = Math.round(performance.now() - startedAt)
    loading.value = false
  }
}
</script>

<template>
  <section class="backend-tester">
    <div class="tester-header">
      <div>
        <h2>后端连接测试</h2>
        <p class="endpoint">GET /api/health</p>
      </div>
      <button type="button" :disabled="loading" @click="testConnection">
        {{ loading ? '请求中...' : '测试连接' }}
      </button>
    </div>

    <p v-if="loading" class="status">正在请求后端...</p>
    <p v-else-if="error" class="status status--error">连接失败：{{ error }}</p>
    <div v-else-if="result" class="status status--success">
      <p>连接成功，耗时 {{ elapsed }} ms</p>
      <pre>{{ JSON.stringify(result, null, 2) }}</pre>
    </div>
    <p v-else class="status status--hint">点击按钮向后端发送一次请求</p>
  </section>
</template>

<style scoped>
.backend-tester {
  padding: 1.75rem;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.tester-header {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  justify-content: space-between;
}

h2 {
  font-size: 1.15rem;
}

.endpoint {
  margin-top: 0.3rem;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--color-text-faint);
}

button {
  flex-shrink: 0;
  padding: 0.55rem 1rem;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-bg);
  background-color: var(--color-text);
  border: 1px solid transparent;
  border-radius: 999px;
  transition:
    color 0.2s ease,
    background-color 0.2s ease;
}

button:hover:not(:disabled) {
  color: var(--color-on-accent);
  background-color: var(--color-accent);
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.status {
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: var(--color-text-soft);
}

.status--error {
  color: #c2413b;
}

.status--success p {
  color: var(--color-accent);
}

.status--success pre {
  padding: 1rem;
  margin-top: 0.75rem;
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--color-code-text);
  background-color: var(--color-code-bg);
  border-radius: var(--radius-sm);
}

.status--hint {
  color: var(--color-text-faint);
}

@media (max-width: 560px) {
  .tester-header {
    flex-direction: column;
  }
}
</style>

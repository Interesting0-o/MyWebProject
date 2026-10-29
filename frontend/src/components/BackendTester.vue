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
    <h1>后端连接测试</h1>
    <p class="endpoint">GET /api/health</p>

    <button type="button" :disabled="loading" @click="testConnection">
      {{ loading ? '请求中...' : '测试连接' }}
    </button>

    <p v-if="loading" class="status">正在请求后端...</p>
    <p v-else-if="error" class="status error">连接失败：{{ error }}</p>
    <div v-else-if="result" class="status success">
      <p>连接成功，耗时 {{ elapsed }} ms</p>
      <pre>{{ JSON.stringify(result, null, 2) }}</pre>
    </div>
    <p v-else class="status hint">点击按钮向后端发送一次请求</p>
  </section>
</template>

<style scoped>
.backend-tester {
  width: 100%;
  max-width: 520px;
  margin: 0 auto;
  padding: 2rem;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  background-color: var(--color-background-soft);
  text-align: center;
}

h1 {
  margin-bottom: 0.5rem;
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--color-heading);
}

.endpoint {
  margin-bottom: 1.5rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.9rem;
  color: var(--color-text);
  opacity: 0.75;
}

button {
  padding: 0.6rem 1.6rem;
  border: none;
  border-radius: 8px;
  background-color: hsla(160, 100%, 37%, 1);
  color: #fff;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

button:hover:not(:disabled) {
  opacity: 0.85;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.status {
  margin-top: 1.5rem;
}

.status.error {
  color: #d9534f;
}

.status.success {
  text-align: left;
}

.status.success > p {
  text-align: center;
}

.status.success pre {
  margin-top: 0.75rem;
  padding: 1rem;
  border-radius: 8px;
  background-color: var(--color-background-mute);
  overflow-x: auto;
}
</style>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { formatDateTime } from '@/utils/format'

const props = defineProps({
  slug: {
    type: String,
    required: true,
  },
})

const comments = ref([])
const loading = ref(true)
const loadError = ref('')
const authorName = ref('')
const content = ref('')
const submitting = ref(false)
const formError = ref('')

async function readErrorMessage(response) {
  const payload = await response.json().catch(() => null)
  if (payload && typeof payload.detail === 'string') {
    return payload.detail
  }
  if (payload && Array.isArray(payload.detail) && payload.detail[0]?.msg) {
    return payload.detail[0].msg
  }
  return '提交失败，请稍后再试。'
}

async function loadComments() {
  loading.value = true
  loadError.value = ''

  try {
    const response = await fetch(`/api/posts/${encodeURIComponent(props.slug)}/comments`)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    comments.value = await response.json()
  } catch {
    loadError.value = '评论加载失败，请稍后再试。'
  } finally {
    loading.value = false
  }
}

async function submitComment() {
  formError.value = ''
  const name = authorName.value.trim()
  const text = content.value.trim()

  if (name.length < 2) {
    formError.value = '昵称至少需要 2 个字符。'
    return
  }
  if (text.length < 2) {
    formError.value = '评论至少需要 2 个字符。'
    return
  }

  submitting.value = true

  try {
    const response = await fetch(`/api/posts/${encodeURIComponent(props.slug)}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ author_name: name, content: text }),
    })

    if (!response.ok) {
      throw new Error(await readErrorMessage(response))
    }

    const comment = await response.json()
    comments.value = [...comments.value, comment]
    content.value = ''
    loadError.value = ''
  } catch (error) {
    formError.value = error instanceof Error ? error.message : '提交失败，请稍后再试。'
  } finally {
    submitting.value = false
  }
}

onMounted(loadComments)
watch(() => props.slug, loadComments)
</script>

<template>
  <section id="comments" class="comments" aria-labelledby="comments-title">
    <header class="comments-header">
      <h2 id="comments-title">评论</h2>
      <span class="comments-count">{{ comments.length }} 条</span>
    </header>

    <p v-if="loading" class="comments-status">正在加载评论…</p>

    <div v-else-if="loadError" class="comments-status">
      <p>{{ loadError }}</p>
      <button type="button" class="button button--ghost" @click="loadComments">重新加载</button>
    </div>

    <p v-else-if="!comments.length" class="comments-status">还没有评论，来留下第一条吧。</p>

    <ol v-else class="comment-list">
      <li v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-meta">
          <span class="comment-avatar" aria-hidden="true">{{ comment.author_name.charAt(0) }}</span>
          <span class="comment-author">{{ comment.author_name }}</span>
          <time class="comment-time" :datetime="comment.created_at">
            {{ formatDateTime(comment.created_at) }}
          </time>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
      </li>
    </ol>

    <form class="comment-form" @submit.prevent="submitComment">
      <h3>写下你的评论</h3>

      <div class="comment-fields">
        <label>
          <span>昵称</span>
          <input
            v-model="authorName"
            type="text"
            maxlength="40"
            minlength="2"
            required
            placeholder="怎么称呼你？"
          />
        </label>

        <label>
          <span>评论</span>
          <textarea
            v-model="content"
            rows="4"
            maxlength="1000"
            minlength="2"
            required
            placeholder="友善交流，不必留下邮箱。"
          ></textarea>
        </label>
      </div>

      <p v-if="formError" class="comment-error" role="alert">{{ formError }}</p>

      <div class="comment-form-footer">
        <p class="comment-note">
          评论会公开显示。提交即表示你同意
          <RouterLink :to="{ name: 'privacy' }">隐私政策</RouterLink>。
        </p>
        <button type="submit" class="button" :disabled="submitting">
          {{ submitting ? '提交中…' : '发表评论' }}
        </button>
      </div>
    </form>
  </section>
</template>

<style scoped>
.comments {
  max-width: var(--reading-width);
  padding-top: 2rem;
  margin-top: 4rem;
  border-top: 1px solid var(--color-border);
}

.comments-header {
  display: flex;
  gap: 1rem;
  align-items: baseline;
  justify-content: space-between;
}

.comments-header h2 {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-faint);
}

.comments-count {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--color-text-faint);
}

.comments-status {
  padding-block: 1.5rem;
  font-size: 0.9rem;
  color: var(--color-text-soft);
}

.comments-status .button {
  margin-top: 0.9rem;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  margin-top: 1.5rem;
}

.comment-item {
  padding: 1rem 1.15rem;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.comment-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.comment-avatar {
  display: grid;
  width: 1.7rem;
  height: 1.7rem;
  font-family: var(--font-serif);
  font-size: 0.8rem;
  color: var(--color-accent);
  background-color: var(--color-accent-soft);
  border-radius: 50%;
  place-items: center;
}

.comment-author {
  font-size: 0.85rem;
  font-weight: 500;
}

.comment-time {
  margin-left: auto;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--color-text-faint);
}

.comment-content {
  margin-top: 0.7rem;
  overflow-wrap: anywhere;
  font-size: 0.92rem;
  line-height: 1.8;
  color: var(--color-text-soft);
  white-space: pre-line;
}

.comment-form {
  padding: 1.25rem;
  margin-top: 2rem;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.comment-form h3 {
  font-size: 0.95rem;
}

.comment-fields {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
  margin-top: 1rem;
}

.comment-fields label {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.04em;
  color: var(--color-text-faint);
}

.comment-fields input,
.comment-fields textarea {
  padding: 0.65rem 0.8rem;
  font-family: var(--font-sans);
  font-size: 0.9rem;
  color: var(--color-text);
  background-color: var(--color-bg);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-sm);
  transition:
    border-color 0.2s ease,
    background-color 0.2s ease;
}

.comment-fields input:focus,
.comment-fields textarea:focus {
  border-color: var(--color-accent);
}

.comment-fields textarea {
  min-height: 6rem;
  resize: vertical;
}

.comment-form-footer {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  margin-top: 1rem;
}

.comment-note {
  max-width: 26rem;
  font-size: 0.74rem;
  line-height: 1.6;
  color: var(--color-text-faint);
}

.comment-note a {
  color: var(--color-accent);
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s ease;
}

.comment-note a:hover {
  border-color: currentcolor;
}

.comment-error {
  margin-top: 0.8rem;
  font-size: 0.8rem;
  color: var(--color-danger);
}

.comment-form .button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
  transform: none;
}

@media (max-width: 560px) {
  .comment-form {
    padding: 1rem;
  }

  .comment-form-footer {
    align-items: stretch;
    flex-direction: column;
  }

  .comment-form-footer .button {
    width: 100%;
  }
}
</style>

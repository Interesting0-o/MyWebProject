<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  summary: {
    type: String,
    default: '',
  },
})

const copied = ref(false)
let timer = 0

const shareUrl = computed(() => window.location.href)
const encodedUrl = computed(() => encodeURIComponent(shareUrl.value))
const encodedTitle = computed(() => encodeURIComponent(props.title))
const weiboUrl = computed(
  () =>
    `https://service.weibo.com/share/share.php?url=${encodedUrl.value}&title=${encodedTitle.value}`,
)
const xUrl = computed(
  () => `https://twitter.com/intent/tweet?url=${encodedUrl.value}&text=${encodedTitle.value}`,
)

async function copyLink() {
  try {
    await navigator.clipboard.writeText(shareUrl.value)
  } catch {
    const input = document.createElement('textarea')
    input.value = shareUrl.value
    input.setAttribute('readonly', '')
    input.style.position = 'fixed'
    input.style.opacity = '0'
    document.body.append(input)
    input.select()
    if (typeof document.execCommand === 'function') {
      document.execCommand('copy')
    }
    input.remove()
  }

  copied.value = true
  window.clearTimeout(timer)
  timer = window.setTimeout(() => {
    copied.value = false
  }, 2000)
}

async function nativeShare() {
  if (!navigator.share) {
    await copyLink()
    return
  }

  try {
    await navigator.share({ title: props.title, text: props.summary, url: shareUrl.value })
  } catch {
    return
  }
}

onBeforeUnmount(() => {
  window.clearTimeout(timer)
})
</script>

<template>
  <section class="post-share" aria-labelledby="share-title">
    <h2 id="share-title" class="share-title">分享这篇文章</h2>
    <div class="share-actions">
      <button type="button" class="share-button" @click="nativeShare">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
          aria-hidden="true"
          focusable="false"
        >
          <circle cx="18" cy="5" r="2.5" />
          <circle cx="6" cy="12" r="2.5" />
          <circle cx="18" cy="19" r="2.5" />
          <path d="m8.2 10.8 7.6-4.3M8.2 13.2l7.6 4.3" />
        </svg>
        {{ copied ? '已复制链接' : '分享' }}
      </button>

      <a class="share-button" :href="weiboUrl" target="_blank" rel="noreferrer">微博</a>
      <a class="share-button" :href="xUrl" target="_blank" rel="noreferrer">X</a>

      <button type="button" class="share-button" @click="copyLink">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
          aria-hidden="true"
          focusable="false"
        >
          <rect x="9" y="9" width="11" height="11" rx="2" />
          <path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1" />
        </svg>
        {{ copied ? '已复制' : '复制链接' }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.share-title {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-faint);
}

.share-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.9rem;
}

.share-button {
  display: inline-flex;
  gap: 0.4rem;
  align-items: center;
  padding: 0.42rem 0.8rem;
  font-size: 0.8rem;
  color: var(--color-text-soft);
  background-color: transparent;
  border: 1px solid var(--color-border-strong);
  border-radius: 999px;
  transition:
    color 0.2s ease,
    background-color 0.2s ease,
    border-color 0.2s ease;
}

.share-button:hover {
  color: var(--color-accent);
  background-color: var(--color-surface-muted);
  border-color: var(--color-accent);
}

.share-button svg {
  width: 0.95rem;
  height: 0.95rem;
}
</style>

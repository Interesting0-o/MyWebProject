<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PostList from '@/components/PostList.vue'
import { useSeo } from '@/composables/useSeo'
import { allTags, posts } from '@/data/posts'
import { searchPosts } from '@/utils/search'

const route = useRoute()
const router = useRouter()

function readQuery(value) {
  return typeof value === 'string' ? value : ''
}

const query = ref(readQuery(route.query.q))
const activeTag = ref(readQuery(route.query.tag))

const results = computed(() => searchPosts(posts, query.value, activeTag.value))

useSeo(() => ({
  title: query.value.trim() ? `搜索：${query.value.trim()}` : '搜索',
  description: '按标题、摘要、标签或正文内容搜索站内文章。',
  keywords: ['站内搜索', ...allTags.map((tag) => tag.name)],
  path: '/search',
}))

watch([query, activeTag], ([nextQuery, nextTag]) => {
  const next = {}
  if (nextQuery) {
    next.q = nextQuery
  }
  if (nextTag) {
    next.tag = nextTag
  }
  router.replace({ name: 'search', query: next })
})

watch(
  () => route.query,
  (value) => {
    const nextQuery = readQuery(value.q)
    const nextTag = readQuery(value.tag)
    if (query.value !== nextQuery) {
      query.value = nextQuery
    }
    if (activeTag.value !== nextTag) {
      activeTag.value = nextTag
    }
  },
)

function toggleTag(tag) {
  activeTag.value = activeTag.value === tag ? '' : tag
}
</script>

<template>
  <div class="container page search-page">
    <header class="page-header">
      <p class="eyebrow">Search</p>
      <h1 class="page-title">站内搜索</h1>
      <p class="page-description">按标题、摘要、标签或正文内容查找文章。</p>
    </header>

    <form class="search-form" role="search" @submit.prevent>
      <label class="visually-hidden" for="search-input">搜索文章</label>
      <input
        id="search-input"
        v-model="query"
        type="search"
        placeholder="输入关键词，例如 Vue、Docker…"
        autocomplete="off"
        autofocus
      />
      <button v-if="query" type="button" class="button button--ghost" @click="query = ''">
        清空
      </button>
    </form>

    <div class="tag-filter" role="group" aria-label="按标签筛选">
      <button
        v-for="tag in allTags"
        :key="tag.name"
        type="button"
        class="filter-chip"
        :class="{ 'is-active': activeTag === tag.name }"
        :aria-pressed="activeTag === tag.name"
        @click="toggleTag(tag.name)"
      >
        <span class="filter-hash" aria-hidden="true">#</span>{{ tag.name }}
        <span class="filter-count">{{ tag.count }}</span>
      </button>
    </div>

    <p class="result-count" aria-live="polite">找到 {{ results.length }} 篇文章</p>

    <PostList v-if="results.length" :posts="results" />

    <div v-else class="empty-state">
      <p>没有找到匹配的文章，换个关键词或标签试试。</p>
      <RouterLink class="button" :to="{ name: 'home' }">回到首页</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.search-form {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  margin-bottom: 1.25rem;
}

.search-form input {
  flex: 1;
  min-width: 0;
  padding: 0.8rem 1.1rem;
  font-size: 0.98rem;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border-strong);
  border-radius: 999px;
  transition:
    border-color 0.2s ease,
    background-color 0.2s ease;
}

.search-form input:focus {
  border-color: var(--color-accent);
}

.search-form input::placeholder {
  color: var(--color-text-faint);
}

.search-form .button {
  flex-shrink: 0;
}

.tag-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-border);
}

.filter-chip {
  display: inline-flex;
  gap: 0.3rem;
  align-items: baseline;
  padding: 0.32rem 0.7rem;
  font-size: 0.8rem;
  color: var(--color-text-soft);
  background-color: transparent;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  transition:
    color 0.2s ease,
    background-color 0.2s ease,
    border-color 0.2s ease;
}

.filter-chip:hover {
  color: var(--color-text);
  background-color: var(--color-surface-muted);
}

.filter-chip.is-active {
  color: var(--color-accent);
  background-color: var(--color-accent-soft);
  border-color: var(--color-accent);
}

.filter-hash {
  font-family: var(--font-mono);
  opacity: 0.5;
}

.filter-count {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--color-text-faint);
}

.result-count {
  margin-block: 1.5rem;
  font-family: var(--font-mono);
  font-size: 0.74rem;
  letter-spacing: 0.04em;
  color: var(--color-text-faint);
}

@media (max-width: 560px) {
  .search-form {
    align-items: stretch;
  }

  .search-form .button {
    padding-inline: 0.9rem;
  }
}
</style>

<script setup>
import { useSeo } from '@/composables/useSeo'
import { allTags } from '@/data/posts'

useSeo(() => ({
  title: '标签',
  description: `共 ${allTags.length} 个标签，点击查看相关文章。`,
  keywords: allTags.map((tag) => tag.name),
}))
</script>

<template>
  <div class="container page tags">
    <header class="page-header">
      <p class="eyebrow">Tags</p>
      <h1 class="page-title">标签</h1>
      <p class="page-description">共 {{ allTags.length }} 个标签，点击查看相关文章。</p>
    </header>

    <ul class="tag-grid">
      <li v-for="tag in allTags" :key="tag.name">
        <RouterLink class="tag-card" :to="{ name: 'tag', params: { tag: tag.name } }">
          <span class="tag-hash" aria-hidden="true">#</span>
          <span class="tag-name">{{ tag.name }}</span>
          <span class="tag-count">{{ tag.count }} 篇</span>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.tag-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 0.75rem;
}

.tag-card {
  display: flex;
  gap: 0.5rem;
  align-items: baseline;
  padding: 1rem 1.1rem;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition:
    border-color 0.2s ease,
    background-color 0.2s ease,
    transform 0.2s ease;
}

.tag-card:hover {
  background-color: var(--color-surface-muted);
  border-color: var(--color-border-strong);
  transform: translateY(-1px);
}

.tag-hash {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--color-accent);
}

.tag-name {
  font-family: var(--font-serif);
  font-size: 1.05rem;
}

.tag-count {
  margin-left: auto;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  color: var(--color-text-faint);
}
</style>

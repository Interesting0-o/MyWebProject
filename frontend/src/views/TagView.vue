<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import PostList from '@/components/PostList.vue'
import { useSeo } from '@/composables/useSeo'
import { getPostsByTag } from '@/data/posts'

const route = useRoute()

const tag = computed(() => String(route.params.tag ?? ''))
const tagPosts = computed(() => getPostsByTag(tag.value))

useSeo(() => ({
  title: tag.value ? `标签 · ${tag.value}` : '标签',
  description: `标签「${tag.value}」下共有 ${tagPosts.value.length} 篇文章。`,
  keywords: [tag.value, '标签'],
  path: route.path,
}))
</script>

<template>
  <div class="container page tag-page">
    <RouterLink class="back-link" :to="{ name: 'tags' }">
      <span aria-hidden="true">←</span>
      全部标签
    </RouterLink>

    <header class="page-header">
      <p class="eyebrow">Tag</p>
      <h1 class="page-title"><span class="tag-hash" aria-hidden="true">#</span>{{ tag }}</h1>
      <p class="page-description">共 {{ tagPosts.length }} 篇文章</p>
    </header>

    <PostList v-if="tagPosts.length" :posts="tagPosts" />

    <div v-else class="empty-state">
      <p>这个标签下还没有文章。</p>
      <RouterLink class="button" :to="{ name: 'tags' }">看看其他标签</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.back-link {
  display: inline-flex;
  gap: 0.4rem;
  align-items: center;
  margin-bottom: 2rem;
  font-size: 0.82rem;
  color: var(--color-text-soft);
  transition: color 0.2s ease;
}

.back-link:hover {
  color: var(--color-accent);
}

.tag-hash {
  margin-right: 0.15em;
  font-family: var(--font-mono);
  font-size: 0.65em;
  color: var(--color-accent);
  vertical-align: 0.15em;
}
</style>

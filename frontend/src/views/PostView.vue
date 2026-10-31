<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import PostContent from '@/components/PostContent.vue'
import TagLink from '@/components/TagLink.vue'
import { usePageTitle } from '@/composables/usePageTitle'
import { getPostBySlug, posts } from '@/data/posts'
import { formatDate } from '@/utils/format'

const route = useRoute()

const post = computed(() => getPostBySlug(route.params.slug))
const postIndex = computed(() => posts.findIndex((item) => item.slug === route.params.slug))
const olderPost = computed(() =>
  postIndex.value >= 0 ? (posts[postIndex.value + 1] ?? null) : null,
)
const newerPost = computed(() => (postIndex.value > 0 ? posts[postIndex.value - 1] : null))

usePageTitle(() => post.value?.title ?? '文章不存在')
</script>

<template>
  <article v-if="post" class="container post">
    <header class="post-header">
      <RouterLink class="back-link" :to="{ name: 'home' }">
        <span aria-hidden="true">←</span>
        返回首页
      </RouterLink>

      <h1 class="post-title">{{ post.title }}</h1>
      <p class="post-summary">{{ post.summary }}</p>

      <div class="post-meta">
        <time :datetime="post.date">{{ formatDate(post.date) }}</time>
        <span class="meta-divider" aria-hidden="true">·</span>
        <span>{{ post.readingTime }} 分钟阅读</span>
        <span class="meta-divider" aria-hidden="true">·</span>
        <div class="post-tags">
          <TagLink v-for="tag in post.tags" :key="tag" :tag="tag" />
        </div>
      </div>
    </header>

    <PostContent :blocks="post.content" />

    <footer v-if="olderPost || newerPost" class="post-footer">
      <nav class="post-nav" aria-label="文章导航">
        <RouterLink
          v-if="olderPost"
          class="post-nav-link"
          :to="{ name: 'post', params: { slug: olderPost.slug } }"
        >
          <span class="post-nav-label">上一篇</span>
          <span class="post-nav-title">{{ olderPost.title }}</span>
        </RouterLink>

        <RouterLink
          v-if="newerPost"
          class="post-nav-link post-nav-link--next"
          :to="{ name: 'post', params: { slug: newerPost.slug } }"
        >
          <span class="post-nav-label">下一篇</span>
          <span class="post-nav-title">{{ newerPost.title }}</span>
        </RouterLink>
      </nav>
    </footer>
  </article>

  <div v-else class="container container--narrow page empty-state">
    <p class="eyebrow">404</p>
    <h1 class="page-title">文章不存在</h1>
    <p>这篇文章可能已经被移动或删除。</p>
    <RouterLink class="button" :to="{ name: 'home' }">回到首页</RouterLink>
  </div>
</template>

<style scoped>
.post {
  padding-block: 3rem 5rem;
}

.post-header {
  max-width: var(--reading-width);
  padding-bottom: 2rem;
  margin: 0 auto 3rem;
  border-bottom: 1px solid var(--color-border);
}

.back-link {
  display: inline-flex;
  gap: 0.4rem;
  align-items: center;
  margin-bottom: 1.5rem;
  font-size: 0.82rem;
  color: var(--color-text-soft);
  transition: color 0.2s ease;
}

.back-link:hover {
  color: var(--color-accent);
}

.post-title {
  font-family: var(--font-serif);
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 600;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.post-summary {
  margin-top: 1rem;
  font-size: 1.05rem;
  line-height: 1.75;
  color: var(--color-text-soft);
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 0.7rem;
  align-items: center;
  margin-top: 1.5rem;
  font-family: var(--font-mono);
  font-size: 0.74rem;
  color: var(--color-text-faint);
}

.meta-divider {
  opacity: 0.55;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.15rem;
  font-family: var(--font-sans);
}

.post-footer {
  max-width: var(--reading-width);
  padding-top: 2rem;
  margin: 4rem auto 0;
  border-top: 1px solid var(--color-border);
}

.post-nav {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.75rem;
}

.post-nav-link {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 1rem 1.15rem;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition:
    border-color 0.2s ease,
    background-color 0.2s ease,
    transform 0.2s ease;
}

.post-nav-link:hover {
  background-color: var(--color-surface-muted);
  border-color: var(--color-border-strong);
  transform: translateY(-1px);
}

.post-nav-label {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  color: var(--color-text-faint);
}

.post-nav-title {
  font-family: var(--font-serif);
  font-size: 0.98rem;
  line-height: 1.45;
}

.post-nav-link--next {
  text-align: right;
}

@media (max-width: 640px) {
  .post {
    padding-block: 2rem 4rem;
  }
}
</style>

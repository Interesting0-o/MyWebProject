<script setup>
import PostList from '@/components/PostList.vue'
import { site } from '@/config/site'
import { usePageTitle } from '@/composables/usePageTitle'
import { posts } from '@/data/posts'
import { formatCompactDate } from '@/utils/format'

usePageTitle()

const latestDate = posts[0]?.date
</script>

<template>
  <div class="container home">
    <section class="hero">
      <p class="eyebrow">{{ site.hero.eyebrow }}</p>
      <h1 class="hero-title">
        {{ site.hero.greeting }}<span class="hero-name">{{ site.name }}</span
        >。
      </h1>
      <p class="hero-description">{{ site.hero.description }}</p>

      <div class="hero-actions">
        <RouterLink class="button" :to="{ name: 'archive' }">浏览全部文章</RouterLink>
        <RouterLink class="button button--ghost" :to="{ name: 'about' }">关于我</RouterLink>
      </div>

      <p class="hero-meta">
        <span>{{ posts.length }} 篇文章</span>
        <span aria-hidden="true">/</span>
        <span v-if="latestDate">最近更新 {{ formatCompactDate(latestDate) }}</span>
      </p>
    </section>

    <section id="latest" class="latest">
      <div class="section-header">
        <h2 class="section-title">最新文章</h2>
        <RouterLink class="section-link" :to="{ name: 'archive' }">全部归档 →</RouterLink>
      </div>
      <PostList :posts="posts" />
    </section>
  </div>
</template>

<style scoped>
.hero {
  padding-block: clamp(2rem, 6vw, 4.5rem) clamp(3rem, 8vw, 5rem);
  margin-bottom: 2.5rem;
  border-bottom: 1px solid var(--color-border);
}

.hero-title {
  max-width: 16em;
  margin-top: 1rem;
  font-family: var(--font-serif);
  font-size: clamp(2.4rem, 6.5vw, 4rem);
  font-weight: 600;
  line-height: 1.15;
  letter-spacing: -0.02em;
}

.hero-name {
  color: var(--color-accent);
}

.hero-description {
  max-width: 34rem;
  margin-top: 1.25rem;
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--color-text-soft);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 2rem;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  align-items: center;
  margin-top: 2.25rem;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  color: var(--color-text-faint);
}

.latest {
  padding-bottom: 1rem;
}
</style>

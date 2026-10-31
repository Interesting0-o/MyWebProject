<script setup>
import { useSeo } from '@/composables/useSeo'
import { posts } from '@/data/posts'
import { formatMonthDay, groupPostsByYear } from '@/utils/format'

useSeo(() => ({
  title: '归档',
  description: `共 ${posts.length} 篇文章，按时间从新到旧排列。`,
  keywords: ['归档', '文章归档'],
}))

const groups = groupPostsByYear(posts)
</script>

<template>
  <div class="container page archive">
    <header class="page-header">
      <p class="eyebrow">Archive</p>
      <h1 class="page-title">归档</h1>
      <p class="page-description">共 {{ posts.length }} 篇文章，按时间从新到旧排列。</p>
    </header>

    <section v-for="group in groups" :key="group.year" class="archive-year">
      <h2 class="archive-year-title">{{ group.year }}</h2>
      <ul class="archive-list">
        <li v-for="post in group.posts" :key="post.slug" class="archive-item">
          <time class="archive-date" :datetime="post.date">{{ formatMonthDay(post.date) }}</time>
          <RouterLink class="archive-link" :to="{ name: 'post', params: { slug: post.slug } }">
            {{ post.title }}
          </RouterLink>
          <span class="archive-tags">{{ post.tags.join(' · ') }}</span>
        </li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.archive-year + .archive-year {
  margin-top: 3.5rem;
}

.archive-year-title {
  padding-bottom: 0.9rem;
  font-family: var(--font-mono);
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  color: var(--color-text-faint);
  border-bottom: 1px solid var(--color-border);
}

.archive-item {
  display: grid;
  grid-template-columns: 4.5rem minmax(0, 1fr) auto;
  gap: 1rem;
  align-items: baseline;
  padding-block: 0.95rem;
  border-bottom: 1px solid var(--color-border);
}

.archive-date {
  font-family: var(--font-mono);
  font-size: 0.76rem;
  color: var(--color-text-faint);
}

.archive-link {
  font-family: var(--font-serif);
  font-size: 1.02rem;
  line-height: 1.5;
  transition: color 0.2s ease;
}

.archive-link:hover {
  color: var(--color-accent);
}

.archive-tags {
  font-size: 0.74rem;
  color: var(--color-text-faint);
}

@media (max-width: 640px) {
  .archive-item {
    grid-template-columns: 3.5rem minmax(0, 1fr);
  }

  .archive-tags {
    display: none;
  }
}
</style>

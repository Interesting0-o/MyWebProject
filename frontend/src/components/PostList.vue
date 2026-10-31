<script setup>
import TagLink from '@/components/TagLink.vue'
import { formatCompactDate } from '@/utils/format'

defineProps({
  posts: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  <div class="post-list">
    <article v-for="post in posts" :key="post.slug" class="post-item">
      <time class="post-date" :datetime="post.date">{{ formatCompactDate(post.date) }}</time>

      <div class="post-body">
        <h2 class="post-title">
          <RouterLink :to="{ name: 'post', params: { slug: post.slug } }">
            {{ post.title }}
          </RouterLink>
        </h2>
        <p class="post-summary">{{ post.summary }}</p>

        <div class="post-meta">
          <span class="reading-time">{{ post.readingTime }} 分钟阅读</span>
          <div class="post-tags">
            <TagLink v-for="tag in post.tags" :key="tag" :tag="tag" />
          </div>
        </div>
      </div>
    </article>
  </div>
</template>

<style scoped>
.post-list {
  margin-top: 0.5rem;
}

.post-item {
  display: grid;
  grid-template-columns: 7.5rem minmax(0, 1fr);
  gap: 1.5rem;
  padding-block: 1.9rem;
  border-bottom: 1px solid var(--color-border);
}

.post-date {
  padding-top: 0.35rem;
  font-family: var(--font-mono);
  font-size: 0.74rem;
  letter-spacing: 0.03em;
  color: var(--color-text-faint);
}

.post-title {
  font-family: var(--font-serif);
  font-size: clamp(1.35rem, 2.4vw, 1.6rem);
  font-weight: 600;
  line-height: 1.35;
  letter-spacing: -0.01em;
}

.post-title a {
  transition: color 0.2s ease;
}

.post-title a:hover {
  color: var(--color-accent);
}

.post-summary {
  max-width: 42rem;
  margin-top: 0.55rem;
  font-size: 0.95rem;
  line-height: 1.75;
  color: var(--color-text-soft);
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem 0.85rem;
  align-items: center;
  margin-top: 0.85rem;
  font-size: 0.78rem;
  color: var(--color-text-faint);
}

.reading-time {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.02em;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.15rem;
}

@media (max-width: 640px) {
  .post-item {
    grid-template-columns: 1fr;
    gap: 0.55rem;
    padding-block: 1.5rem;
  }

  .post-date {
    padding-top: 0;
  }
}
</style>

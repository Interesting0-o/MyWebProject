<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import PostComments from '@/components/PostComments.vue'
import PostContent from '@/components/PostContent.vue'
import PostShare from '@/components/PostShare.vue'
import ReadingProgress from '@/components/ReadingProgress.vue'
import TagLink from '@/components/TagLink.vue'
import { useSeo } from '@/composables/useSeo'
import { site } from '@/config/site'
import { getPostBySlug, posts } from '@/data/posts'
import { getTableOfContents } from '@/utils/content'
import { formatDate } from '@/utils/format'

const route = useRoute()

const post = computed(() => getPostBySlug(route.params.slug))
const postIndex = computed(() => posts.findIndex((item) => item.slug === route.params.slug))
const olderPost = computed(() =>
  postIndex.value >= 0 ? (posts[postIndex.value + 1] ?? null) : null,
)
const newerPost = computed(() => (postIndex.value > 0 ? posts[postIndex.value - 1] : null))
const toc = computed(() => (post.value ? getTableOfContents(post.value.content) : []))
const canonicalUrl = computed(() =>
  post.value ? `${site.url.replace(/\/$/, '')}/posts/${post.value.slug}` : site.url,
)

useSeo(() =>
  post.value
    ? {
        title: post.value.title,
        description: post.value.summary,
        keywords: post.value.tags,
        type: 'article',
        path: `/posts/${post.value.slug}`,
      }
    : {
        title: '文章不存在',
        description: '这篇文章可能已经被移动或删除。',
        robots: 'noindex',
        path: route.path,
      },
)
</script>

<template>
  <ReadingProgress v-if="post" />

  <article v-if="post" class="post">
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

    <div class="post-body">
      <PostContent :blocks="post.content" />

      <aside v-if="toc.length" class="post-toc" aria-labelledby="toc-title">
        <p id="toc-title" class="toc-title">目录</p>
        <ol class="toc-list">
          <li v-for="item in toc" :key="item.id" :class="{ 'toc-item--sub': item.level === 3 }">
            <a :href="`#${item.id}`">{{ item.text }}</a>
          </li>
        </ol>
      </aside>
    </div>

    <footer class="post-footer">
      <PostShare :title="post.title" :summary="post.summary" />

      <section class="post-license" aria-labelledby="license-title">
        <h2 id="license-title">版权与转载</h2>
        <p>
          本文作者 {{ site.author.name }}，首发于 <a :href="canonicalUrl">{{ site.name }}</a
          >。
        </p>
        <p>
          除特别注明外，本文采用
          <a :href="site.license.url" target="_blank" rel="noreferrer">{{ site.license.name }}</a>
          许可协议，转载请注明作者与原文链接。
        </p>
      </section>

      <nav v-if="olderPost || newerPost" class="post-nav" aria-label="文章导航">
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

    <PostComments :slug="post.slug" />
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
  width: min(100% - 2.5rem, calc(var(--reading-width) + 16rem));
  padding-block: 3rem 5rem;
  margin-inline: auto;
}

.post-header {
  max-width: var(--reading-width);
  padding-bottom: 2rem;
  margin-bottom: 3rem;
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

.post-body {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 13rem;
  gap: 3rem;
  align-items: start;
}

.post-toc {
  position: sticky;
  top: 5.5rem;
  padding: 1rem 1.1rem;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.toc-title {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-text-faint);
}

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-top: 0.75rem;
}

.toc-list a {
  display: block;
  font-size: 0.82rem;
  line-height: 1.5;
  color: var(--color-text-soft);
  transition: color 0.2s ease;
}

.toc-list a:hover {
  color: var(--color-accent);
}

.toc-item--sub {
  padding-left: 0.8rem;
}

.post-footer {
  max-width: var(--reading-width);
  padding-top: 2rem;
  margin-top: 4rem;
  border-top: 1px solid var(--color-border);
}

.post-license {
  padding-top: 1.5rem;
  margin-top: 2rem;
  border-top: 1px solid var(--color-border);
}

.post-license h2 {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-faint);
}

.post-license p {
  margin-top: 0.6rem;
  font-size: 0.84rem;
  line-height: 1.8;
  color: var(--color-text-soft);
}

.post-license a {
  color: var(--color-accent);
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s ease;
}

.post-license a:hover {
  border-color: currentcolor;
}

.post-nav {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.75rem;
  margin-top: 2.5rem;
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

@media (max-width: 1040px) {
  .post {
    width: min(100% - 2.5rem, var(--reading-width));
  }

  .post-body {
    grid-template-columns: minmax(0, 1fr);
    gap: 0;
    max-width: var(--reading-width);
  }

  .post-toc {
    position: static;
    order: -1;
    margin-bottom: 2rem;
  }
}

@media (max-width: 640px) {
  .post {
    padding-block: 2rem 4rem;
  }
}
</style>

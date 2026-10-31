<script setup>
import { site } from '@/config/site'
import { useSeo } from '@/composables/useSeo'

useSeo(() => ({
  title: '关于',
  description: site.author.intro[0],
  keywords: [site.name, ...site.stack],
}))
</script>

<template>
  <div class="container page about">
    <header class="about-header">
      <div class="about-avatar" aria-hidden="true">{{ site.name.charAt(0) }}</div>
      <div>
        <p class="eyebrow">About</p>
        <h1 class="page-title">关于我</h1>
        <p class="about-role">{{ site.author.role }} · {{ site.author.location }}</p>
      </div>
    </header>

    <section class="about-section">
      <h2>简介</h2>
      <div class="about-text">
        <p v-for="paragraph in site.author.intro" :key="paragraph">{{ paragraph }}</p>
      </div>
    </section>

    <section class="about-section">
      <h2>现在</h2>
      <div class="about-text">
        <p>{{ site.author.now }}</p>
      </div>
    </section>

    <section class="about-section">
      <h2>常用技术</h2>
      <ul class="stack-list">
        <li v-for="item in site.stack" :key="item" class="stack-item">{{ item }}</li>
      </ul>
    </section>

    <section class="about-section">
      <h2>联系</h2>
      <div class="contact-list">
        <div class="contact-item">
          <span class="contact-label">Email</span>
          <a :href="`mailto:${site.author.email}`">{{ site.author.email }}</a>
        </div>
        <div class="contact-item">
          <span class="contact-label">GitHub</span>
          <a :href="site.author.github" target="_blank" rel="noreferrer">
            {{ site.author.github }}
          </a>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-header {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
  padding-bottom: 2.5rem;
  margin-bottom: 3rem;
  border-bottom: 1px solid var(--color-border);
}

.about-avatar {
  display: grid;
  flex-shrink: 0;
  width: 4.5rem;
  height: 4.5rem;
  font-family: var(--font-serif);
  font-size: 2rem;
  color: var(--color-accent);
  background-color: var(--color-accent-soft);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  place-items: center;
}

.about-role {
  margin-top: 0.6rem;
  font-size: 0.88rem;
  color: var(--color-text-soft);
}

.about-section {
  max-width: var(--reading-width);
  margin-top: 3rem;
}

.about-section:first-of-type {
  margin-top: 0;
}

.about-section h2 {
  padding-bottom: 0.75rem;
  margin-bottom: 1.25rem;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-text-faint);
  border-bottom: 1px solid var(--color-border);
}

.about-text {
  font-family: var(--font-serif);
  font-size: 1.02rem;
  line-height: 1.9;
  color: var(--color-text-soft);
}

.about-text p + p {
  margin-top: 1rem;
}

.stack-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.stack-item {
  padding: 0.35rem 0.8rem;
  font-size: 0.82rem;
  color: var(--color-text-soft);
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 999px;
}

.contact-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.contact-item {
  display: flex;
  gap: 1rem;
  align-items: baseline;
  font-size: 0.9rem;
}

.contact-label {
  width: 5rem;
  flex-shrink: 0;
  padding-top: 0.1rem;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  color: var(--color-text-faint);
}

.contact-item a {
  word-break: break-all;
  color: var(--color-accent);
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s ease;
}

.contact-item a:hover {
  border-color: currentcolor;
}

@media (max-width: 560px) {
  .about-header {
    gap: 1rem;
  }

  .about-avatar {
    width: 3.5rem;
    height: 3.5rem;
    font-size: 1.6rem;
    border-radius: var(--radius-md);
  }

  .contact-item {
    flex-direction: column;
    gap: 0.15rem;
  }
}
</style>

<script setup>
import { site } from '@/config/site'

const currentYear = new Date().getFullYear()
const yearRange =
  currentYear > site.startYear ? `${site.startYear}–${currentYear}` : `${currentYear}`
</script>

<template>
  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-info">
        <p>© {{ yearRange }} {{ site.author.name }} · {{ site.name }}</p>
        <p class="footer-note">{{ site.description }} · Vue 3 + Vite</p>
        <p class="footer-meta">
          <span>始于 {{ site.startYear }}</span>
          <span aria-hidden="true">·</span>
          <a :href="site.icp.url" target="_blank" rel="noreferrer">{{ site.icp.label }}</a>
        </p>
      </div>

      <nav class="footer-links" aria-label="页脚导航">
        <a href="/rss.xml">RSS</a>
        <RouterLink :to="{ name: 'privacy' }">隐私政策</RouterLink>
        <RouterLink :to="{ name: 'disclaimer' }">免责声明</RouterLink>
        <a :href="`mailto:${site.author.email}`">联系</a>
        <a :href="site.author.github" target="_blank" rel="noreferrer">GitHub</a>
      </nav>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  padding-block: 2rem;
  border-top: 1px solid var(--color-border);
}

.footer-inner {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--color-text-faint);
}

.footer-info {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.footer-note {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.02em;
}

.footer-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  align-items: center;
  font-size: 0.72rem;
}

.footer-meta a {
  transition: color 0.2s ease;
}

.footer-meta a:hover {
  color: var(--color-accent);
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem 1rem;
  justify-content: flex-end;
  font-size: 0.76rem;
}

.footer-links a {
  transition: color 0.2s ease;
}

.footer-links a:hover {
  color: var(--color-accent);
}

@media (max-width: 640px) {
  .footer-inner {
    flex-direction: column;
    gap: 0.9rem;
  }

  .footer-links {
    justify-content: flex-start;
  }
}
</style>

<script setup>
import { site } from '@/config/site'

const currentYear = new Date().getFullYear()
const yearRange =
  currentYear > site.startYear ? `${site.startYear}–${currentYear}` : `${currentYear}`
</script>

<template>
  <footer class="site-footer">
    <div class="container footer-inner">
      <p>© {{ yearRange }} {{ site.author.name }} · {{ site.name }}</p>
      <p class="footer-note">{{ site.description }} · Vue 3 + Vite</p>
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
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--color-text-faint);
}

.footer-note {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.02em;
}

@media (max-width: 640px) {
  .footer-inner {
    flex-direction: column;
    gap: 0.35rem;
    align-items: flex-start;
  }
}
</style>

<script setup>
import { useRoute } from 'vue-router'
import SiteLogo from '@/components/SiteLogo.vue'
import { site } from '@/config/site'

const route = useRoute()

const navItems = [
  { label: '首页', to: { name: 'home' }, match: ['home', 'post'] },
  { label: '归档', to: { name: 'archive' }, match: ['archive'] },
  { label: '标签', to: { name: 'tags' }, match: ['tags', 'tag'] },
  { label: '关于', to: { name: 'about' }, match: ['about'] },
]

function isActive(item) {
  return item.match.includes(route.name)
}
</script>

<template>
  <header class="site-header">
    <div class="container header-inner">
      <RouterLink class="brand" :to="{ name: 'home' }" :aria-label="`${site.name} 首页`">
        <SiteLogo />
        <span class="brand-name">{{ site.name }}</span>
      </RouterLink>

      <nav class="site-nav" aria-label="主导航">
        <RouterLink
          v-for="item in navItems"
          :key="item.label"
          class="nav-link"
          :class="{ 'is-active': isActive(item) }"
          :to="item.to"
          :aria-current="isActive(item) ? 'page' : undefined"
        >
          {{ item.label }}
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  position: sticky;
  top: 0;
  z-index: 20;
  background-color: var(--color-bg);
  background-color: color-mix(in srgb, var(--color-bg) 86%, transparent);
  border-bottom: 1px solid var(--color-border);
  backdrop-filter: blur(12px);
}

.header-inner {
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  padding-block: 0.9rem;
}

.brand {
  display: inline-flex;
  gap: 0.6rem;
  align-items: center;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.brand-name {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  letter-spacing: 0.04em;
}

.site-nav {
  display: flex;
  gap: 0.2rem;
  align-items: center;
}

.nav-link {
  padding: 0.4rem 0.7rem;
  font-size: 0.88rem;
  color: var(--color-text-soft);
  border-radius: 999px;
  transition:
    color 0.2s ease,
    background-color 0.2s ease;
}

.nav-link:hover {
  color: var(--color-text);
  background-color: var(--color-surface-muted);
}

.nav-link.is-active {
  font-weight: 500;
  color: var(--color-accent);
  background-color: var(--color-accent-soft);
}

@media (max-width: 480px) {
  .brand-name {
    display: none;
  }

  .nav-link {
    padding-inline: 0.55rem;
    font-size: 0.84rem;
  }
}
</style>

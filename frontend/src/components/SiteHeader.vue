<script setup>
import { useRoute } from 'vue-router'
import SiteLogo from '@/components/SiteLogo.vue'
import { useTheme } from '@/composables/useTheme'
import { site } from '@/config/site'

const route = useRoute()
const { isDark, toggleTheme } = useTheme()

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

      <div class="header-actions">
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

        <RouterLink
          class="icon-link"
          :to="{ name: 'search' }"
          aria-label="搜索文章"
          title="搜索文章"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            aria-hidden="true"
            focusable="false"
          >
            <circle cx="11" cy="11" r="6.5" />
            <path d="m16 16 4.5 4.5" />
          </svg>
        </RouterLink>

        <button
          type="button"
          class="theme-toggle"
          :aria-label="isDark ? '切换到白天模式' : '切换到夜间模式'"
          :title="isDark ? '切换到白天模式' : '切换到夜间模式'"
          @click="toggleTheme"
        >
          <svg
            v-if="isDark"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            aria-hidden="true"
            focusable="false"
          >
            <circle cx="12" cy="12" r="4.2" />
            <path
              d="M12 2.6v2.1M12 19.3v2.1M4.7 4.7l1.5 1.5M17.8 17.8l1.5 1.5M2.5 12h2.1M19.4 12h2.1M4.7 19.3l1.5-1.5M17.8 6.2l1.5-1.5"
            />
          </svg>
          <svg
            v-else
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
            focusable="false"
          >
            <path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a6.6 6.6 0 0 0 9.8 9.8Z" />
          </svg>
        </button>
      </div>
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

.header-actions {
  display: flex;
  gap: 0.6rem;
  align-items: center;
}

.site-nav {
  display: flex;
  gap: 0.2rem;
  align-items: center;
}

.icon-link,
.theme-toggle {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 2.1rem;
  height: 2.1rem;
  color: var(--color-text-soft);
  background-color: transparent;
  border: 1px solid var(--color-border);
  border-radius: 50%;
  transition:
    color 0.2s ease,
    background-color 0.2s ease,
    border-color 0.2s ease;
}

.icon-link:hover,
.theme-toggle:hover {
  color: var(--color-accent);
  background-color: var(--color-surface-muted);
  border-color: var(--color-border-strong);
}

.icon-link.router-link-active {
  color: var(--color-accent);
  background-color: var(--color-accent-soft);
  border-color: var(--color-accent);
}

.icon-link svg,
.theme-toggle svg {
  width: 1.05rem;
  height: 1.05rem;
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
  .header-inner {
    gap: 0.5rem;
  }

  .brand-name {
    display: none;
  }

  .header-actions {
    gap: 0.2rem;
  }

  .nav-link {
    padding-inline: 0.45rem;
    font-size: 0.8rem;
  }

  .icon-link,
  .theme-toggle {
    width: 1.8rem;
    height: 1.8rem;
  }
}
</style>

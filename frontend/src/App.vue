<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">连接测试</RouterLink>
      <RouterLink to="/about">关于</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  padding: 1.5rem 0;
  margin-bottom: 2.5rem;
  border-bottom: 1px solid var(--color-border);
}

nav {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

nav a {
  padding: 0.35rem 0.9rem;
  border-radius: 999px;
}

nav a.router-link-exact-active {
  color: #fff;
  background-color: hsla(160, 100%, 37%, 1);
}
</style>

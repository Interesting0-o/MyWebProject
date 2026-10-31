<script setup>
import { useSeo } from '@/composables/useSeo'

useSeo(() => ({
  title: '页面未找到',
  description: '你访问的页面不存在，或者已经被移动。',
  robots: 'noindex',
}))
</script>

<template>
  <div class="container container--narrow page empty-state">
    <p class="eyebrow">404</p>
    <h1 class="page-title">页面走丢了</h1>
    <p>你访问的页面不存在，或者已经被移动。</p>
    <RouterLink class="button" :to="{ name: 'home' }">回到首页</RouterLink>
  </div>
</template>

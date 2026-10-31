<script setup>
import BackendTester from '@/components/BackendTester.vue'
import { usePageTitle } from '@/composables/usePageTitle'

usePageTitle(() => '服务状态')
</script>

<template>
  <div class="container container--narrow page">
    <header class="page-header">
      <p class="eyebrow">Debug</p>
      <h1 class="page-title">服务状态</h1>
      <p class="page-description">这个页面不会出现在导航中，用于联调后端健康检查接口。</p>
    </header>

    <BackendTester />
  </div>
</template>

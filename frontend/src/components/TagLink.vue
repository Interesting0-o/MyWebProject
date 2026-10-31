<script setup>
defineProps({
  tag: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <RouterLink class="tag-link" :to="{ name: 'tag', params: { tag } }">
    <span class="tag-hash" aria-hidden="true">#</span>
    <span>{{ tag }}</span>
  </RouterLink>
</template>

<style scoped>
.tag-link {
  display: inline-flex;
  gap: 0.15rem;
  align-items: center;
  padding: 0.15rem 0.45rem;
  font-size: 0.78rem;
  color: var(--color-text-soft);
  border-radius: 999px;
  transition:
    color 0.2s ease,
    background-color 0.2s ease;
}

.tag-link:hover {
  color: var(--color-accent);
  background-color: var(--color-accent-soft);
}

.tag-hash {
  font-family: var(--font-mono);
  opacity: 0.5;
}
</style>

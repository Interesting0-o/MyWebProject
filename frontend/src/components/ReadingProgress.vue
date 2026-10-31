<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const progress = ref(0)
let frame = 0

function updateProgress() {
  const scrollable = document.documentElement.scrollHeight - window.innerHeight
  progress.value =
    scrollable > 0 ? Math.min(100, Math.max(0, (window.scrollY / scrollable) * 100)) : 0
}

function scheduleUpdate() {
  cancelAnimationFrame(frame)
  frame = requestAnimationFrame(updateProgress)
}

onMounted(() => {
  updateProgress()
  window.addEventListener('scroll', scheduleUpdate, { passive: true })
  window.addEventListener('resize', scheduleUpdate)
})

onBeforeUnmount(() => {
  cancelAnimationFrame(frame)
  window.removeEventListener('scroll', scheduleUpdate)
  window.removeEventListener('resize', scheduleUpdate)
})
</script>

<template>
  <div
    class="reading-progress"
    role="progressbar"
    aria-label="阅读进度"
    aria-valuemin="0"
    aria-valuemax="100"
    :aria-valuenow="Math.round(progress)"
  >
    <span class="reading-progress-bar" :style="{ width: `${progress}%` }"></span>
  </div>
</template>

<style scoped>
.reading-progress {
  position: fixed;
  inset: 0 0 auto;
  z-index: 30;
  height: 3px;
  pointer-events: none;
}

.reading-progress-bar {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, var(--color-accent), var(--color-accent-hover));
}

@media (prefers-reduced-motion: no-preference) {
  .reading-progress-bar {
    transition: width 0.1s linear;
  }
}
</style>

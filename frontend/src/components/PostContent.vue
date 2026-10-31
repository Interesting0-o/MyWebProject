<script setup>
defineProps({
  blocks: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  <div class="prose">
    <template v-for="(block, index) in blocks" :key="index">
      <p v-if="block.type === 'paragraph'">{{ block.text }}</p>

      <h2 v-else-if="block.type === 'heading' && block.level === 2">{{ block.text }}</h2>
      <h3 v-else-if="block.type === 'heading'">{{ block.text }}</h3>

      <blockquote v-else-if="block.type === 'quote'">
        <p>{{ block.text }}</p>
      </blockquote>

      <figure v-else-if="block.type === 'code'" class="code-block">
        <figcaption>{{ block.lang }}</figcaption>
        <pre><code>{{ block.code }}</code></pre>
      </figure>

      <ol v-else-if="block.type === 'list' && block.ordered">
        <li v-for="(item, itemIndex) in block.items" :key="itemIndex">{{ item }}</li>
      </ol>
      <ul v-else-if="block.type === 'list'">
        <li v-for="(item, itemIndex) in block.items" :key="itemIndex">{{ item }}</li>
      </ul>
    </template>
  </div>
</template>

<style scoped>
.prose {
  max-width: var(--reading-width);
  margin-inline: auto;
  font-family: var(--font-serif);
  font-size: 1.0625rem;
  line-height: 1.95;
  color: var(--color-text);
}

.prose > :first-child {
  margin-top: 0;
}

.prose p {
  margin-block: 1.4em;
}

.prose h2 {
  margin: 2.6em 0 1em;
  font-family: var(--font-sans);
  font-size: 1.5rem;
  line-height: 1.35;
  letter-spacing: -0.01em;
}

.prose h3 {
  margin: 2em 0 0.9em;
  font-family: var(--font-sans);
  font-size: 1.2rem;
  line-height: 1.4;
}

.prose ul,
.prose ol {
  margin-block: 1.3em;
  padding-left: 1.4em;
}

.prose ul {
  list-style: disc;
}

.prose ol {
  list-style: decimal;
}

.prose li {
  padding-left: 0.2em;
  margin-block: 0.45em;
}

.prose li::marker {
  color: var(--color-accent);
}

.prose blockquote {
  padding: 0.2em 0 0.2em 1.4em;
  margin-block: 2em;
  font-size: 1.05rem;
  color: var(--color-text-soft);
  border-left: 3px solid var(--color-accent);
}

.prose blockquote p {
  margin: 0;
}

.prose code {
  padding: 0.15em 0.38em;
  font-family: var(--font-mono);
  font-size: 0.86em;
  background-color: var(--color-surface-muted);
  border-radius: 4px;
}

.code-block {
  margin-block: 2em;
  overflow: hidden;
  background-color: var(--color-code-bg);
  border: 1px solid rgb(255 255 255 / 6%);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.code-block figcaption {
  padding: 0.6rem 1.1rem;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-code-muted);
  border-bottom: 1px solid rgb(255 255 255 / 8%);
}

.code-block pre {
  padding: 1.15rem 1.3rem 1.35rem;
  margin: 0;
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 0.83rem;
  line-height: 1.75;
  color: var(--color-code-text);
}

.code-block code {
  padding: 0;
  font-size: inherit;
  color: inherit;
  background: none;
}
</style>

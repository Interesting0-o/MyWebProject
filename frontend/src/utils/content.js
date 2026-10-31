function slugify(text) {
  return String(text)
    .toLowerCase()
    .trim()
    .replace(/[^\p{Letter}\p{Number}]+/gu, '-')
    .replace(/^-+|-+$/g, '')
}

export function withHeadingIds(blocks = []) {
  const counts = new Map()

  return blocks.map((block, index) => {
    if (block.type !== 'heading') {
      return block
    }

    const base = slugify(block.text) || `section-${index + 1}`
    const count = counts.get(base) ?? 0
    counts.set(base, count + 1)

    return {
      ...block,
      id: count === 0 ? base : `${base}-${count + 1}`,
    }
  })
}

export function getTableOfContents(blocks = []) {
  return withHeadingIds(blocks)
    .filter((block) => block.type === 'heading')
    .map(({ id, level, text }) => ({ id, level, text }))
}

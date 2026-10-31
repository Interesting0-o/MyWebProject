function normalize(value) {
  return String(value ?? '').toLowerCase()
}

function blockText(block) {
  if (block.type === 'list') {
    return block.items.join(' ')
  }
  if (block.type === 'code') {
    return block.code
  }
  return block.text ?? ''
}

export function searchPosts(collection, query = '', tag = '') {
  const terms = normalize(query).trim().split(/\s+/).filter(Boolean)
  const tagFilter = String(tag ?? '')

  return collection
    .filter((post) => !tagFilter || post.tags.includes(tagFilter))
    .map((post) => {
      const title = normalize(post.title)
      const summary = normalize(post.summary)
      const tags = normalize(post.tags.join(' '))
      const body = normalize((post.content ?? []).map(blockText).join(' '))

      const score = terms.reduce((total, term) => {
        if (title.includes(term)) return total + 10
        if (tags.includes(term)) return total + 6
        if (summary.includes(term)) return total + 4
        if (body.includes(term)) return total + 1
        return total
      }, 0)

      return { post, score }
    })
    .filter(({ score }) => terms.length === 0 || score > 0)
    .sort((a, b) => b.score - a.score || b.post.date.localeCompare(a.post.date))
    .map(({ post }) => post)
}

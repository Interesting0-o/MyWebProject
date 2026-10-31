function parseDate(value) {
  const [year, month, day] = value.split('-').map(Number)
  return { year, month, day }
}

function pad(value) {
  return String(value).padStart(2, '0')
}

export function formatDate(value) {
  const { year, month, day } = parseDate(value)
  return `${year} 年 ${month} 月 ${day} 日`
}

export function formatCompactDate(value) {
  const { year, month, day } = parseDate(value)
  return `${year}.${pad(month)}.${pad(day)}`
}

export function formatMonthDay(value) {
  const { month, day } = parseDate(value)
  return `${pad(month)}.${pad(day)}`
}

export function formatDateTime(value) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return String(value ?? '')
  }

  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

function blockToText(block) {
  if (block.type === 'list') {
    return block.items.join(' ')
  }
  if (block.type === 'code') {
    return block.code
  }
  return block.text ?? ''
}

export function estimateReadingTime(blocks = []) {
  const text = blocks.map(blockToText).join(' ')
  const cjkCount = (text.match(/[\u4e00-\u9fff]/g) ?? []).length
  const latinWords = text
    .replace(/[\u4e00-\u9fff]/g, ' ')
    .trim()
    .split(/\s+/)
    .filter(Boolean).length

  return Math.max(1, Math.round(cjkCount / 300 + latinWords / 200))
}

export function groupPostsByYear(posts) {
  const groups = new Map()

  for (const post of posts) {
    const year = post.date.slice(0, 4)
    if (!groups.has(year)) {
      groups.set(year, [])
    }
    groups.get(year).push(post)
  }

  return [...groups.entries()].map(([year, items]) => ({ year, posts: items }))
}

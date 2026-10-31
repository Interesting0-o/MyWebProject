import { describe, expect, it } from 'vitest'
import {
  estimateReadingTime,
  formatCompactDate,
  formatDate,
  formatDateTime,
  formatMonthDay,
  groupPostsByYear,
} from '../format'

describe('date formatting', () => {
  it('formats ISO dates without timezone drift', () => {
    expect(formatDate('2026-10-24')).toBe('2026 年 10 月 24 日')
    expect(formatCompactDate('2026-01-05')).toBe('2026.01.05')
    expect(formatMonthDay('2026-01-05')).toBe('01.05')
  })

  it('formats timestamps and tolerates invalid input', () => {
    expect(formatDateTime('not-a-date')).toBe('not-a-date')
    expect(formatDateTime('2026-10-24T12:30:00Z')).toContain('2026')
  })
})

describe('estimateReadingTime', () => {
  it('always returns at least one minute', () => {
    expect(estimateReadingTime([{ type: 'paragraph', text: '很短的一段话。' }])).toBe(1)
  })

  it('counts Chinese characters and latin words', () => {
    expect(estimateReadingTime([{ type: 'paragraph', text: '中'.repeat(600) }])).toBe(2)
    expect(estimateReadingTime([{ type: 'code', code: 'word '.repeat(400) }])).toBe(2)
  })
})

describe('groupPostsByYear', () => {
  it('keeps post order and groups by year', () => {
    const groups = groupPostsByYear([
      { slug: 'a', date: '2026-10-24' },
      { slug: 'b', date: '2026-05-12' },
      { slug: 'c', date: '2025-12-30' },
    ])

    expect(groups.map((group) => group.year)).toEqual(['2026', '2025'])
    expect(groups[0].posts).toHaveLength(2)
    expect(groups[0].posts[0].slug).toBe('a')
  })
})

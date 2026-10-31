import { describe, expect, it } from 'vitest'
import { getTableOfContents, withHeadingIds } from '../content'

describe('withHeadingIds', () => {
  it('creates stable unique anchors for headings', () => {
    const blocks = [
      { type: 'heading', level: 2, text: '开始' },
      { type: 'paragraph', text: '正文' },
      { type: 'heading', level: 3, text: '开始' },
      { type: 'heading', level: 2, text: 'Code & Notes' },
    ]

    const result = withHeadingIds(blocks)

    expect(result[0].id).toBe('开始')
    expect(result[1].id).toBeUndefined()
    expect(result[2].id).toBe('开始-2')
    expect(result[3].id).toBe('code-notes')
  })
})

describe('getTableOfContents', () => {
  it('only returns headings with levels', () => {
    const toc = getTableOfContents([
      { type: 'heading', level: 2, text: '第一节' },
      { type: 'quote', text: '引用' },
      { type: 'heading', level: 3, text: '细节' },
    ])

    expect(toc).toEqual([
      { id: '第一节', level: 2, text: '第一节' },
      { id: '细节', level: 3, text: '细节' },
    ])
  })
})

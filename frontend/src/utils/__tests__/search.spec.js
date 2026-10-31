import { describe, expect, it } from 'vitest'
import { searchPosts } from '../search'

const posts = [
  {
    slug: 'vue-refactor',
    title: '用 Vue 3 重构页面',
    date: '2026-10-24',
    tags: ['Vue', '前端'],
    summary: '记录一次组合式 API 重构。',
    content: [{ type: 'paragraph', text: 'ref 与 computed 的使用方式。' }],
  },
  {
    slug: 'docker-stack',
    title: '用 Docker Compose 编排环境',
    date: '2026-08-07',
    tags: ['Docker', '运维'],
    summary: '本地全栈环境与健康检查。',
    content: [{ type: 'paragraph', text: '服务之间通过服务名通信。' }],
  },
]

describe('searchPosts', () => {
  it('matches title, tag, summary and body text', () => {
    expect(searchPosts(posts, 'vue').map((post) => post.slug)).toEqual(['vue-refactor'])
    expect(searchPosts(posts, '运维').map((post) => post.slug)).toEqual(['docker-stack'])
    expect(searchPosts(posts, '健康检查').map((post) => post.slug)).toEqual(['docker-stack'])
    expect(searchPosts(posts, 'computed').map((post) => post.slug)).toEqual(['vue-refactor'])
  })

  it('filters by tag', () => {
    expect(searchPosts(posts, '', 'Vue').map((post) => post.slug)).toEqual(['vue-refactor'])
    expect(searchPosts(posts, 'docker', 'Vue')).toEqual([])
  })

  it('returns all posts in date order for an empty query', () => {
    expect(searchPosts(posts).map((post) => post.slug)).toEqual(['vue-refactor', 'docker-stack'])
  })
})

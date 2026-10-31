import { flushPromises, mount } from '@vue/test-utils'
import { afterEach, describe, expect, it, vi } from 'vitest'
import PostComments from '../PostComments.vue'

const RouterLinkStub = { template: '<a><slot /></a>' }

function mountComments() {
  return mount(PostComments, {
    props: { slug: 'demo' },
    global: { stubs: { RouterLink: RouterLinkStub } },
  })
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('PostComments', () => {
  it('loads comments and appends a submitted comment', async () => {
    const existing = [
      {
        id: 1,
        author_name: '小明',
        content: '写得好。',
        created_at: '2026-10-31T12:00:00',
      },
    ]
    const created = {
      id: 2,
      author_name: '读者',
      content: '感谢分享。',
      created_at: '2026-10-31T13:00:00',
    }
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({ ok: true, json: async () => existing })
      .mockResolvedValueOnce({ ok: true, json: async () => created })
    vi.stubGlobal('fetch', fetchMock)

    const wrapper = mountComments()
    await flushPromises()

    expect(wrapper.text()).toContain('小明')
    expect(wrapper.text()).toContain('写得好。')
    expect(wrapper.text()).toContain('1 条')

    await wrapper.find('input').setValue(' 读者 ')
    await wrapper.find('textarea').setValue(' 感谢分享。 ')
    await wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(wrapper.text()).toContain('2 条')
    expect(wrapper.text()).toContain('感谢分享。')
    expect(fetchMock).toHaveBeenLastCalledWith(
      '/api/posts/demo/comments',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ author_name: '读者', content: '感谢分享。' }),
      }),
    )
  })
})

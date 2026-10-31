import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useTheme } from '../useTheme'

let storage

beforeEach(() => {
  storage = new Map()
  vi.stubGlobal('localStorage', {
    getItem: (key) => storage.get(key) ?? null,
    setItem: (key, value) => storage.set(key, String(value)),
    removeItem: (key) => storage.delete(key),
    clear: () => storage.clear(),
  })
  document.documentElement.dataset.theme = 'light'
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('useTheme', () => {
  it('toggles between light and dark and persists the choice', () => {
    const { isDark, toggleTheme } = useTheme()

    expect(isDark.value).toBe(false)

    toggleTheme()

    expect(isDark.value).toBe(true)
    expect(document.documentElement.dataset.theme).toBe('dark')
    expect(storage.get('theme')).toBe('dark')

    toggleTheme()

    expect(isDark.value).toBe(false)
    expect(document.documentElement.dataset.theme).toBe('light')
    expect(storage.get('theme')).toBe('light')
  })
})

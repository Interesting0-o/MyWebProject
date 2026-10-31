import { computed, readonly, ref } from 'vue'

const STORAGE_KEY = 'theme'
const THEME_COLORS = {
  light: '#fbfbf8',
  dark: '#131614',
}

function resolveInitialTheme() {
  return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light'
}

const theme = ref(resolveInitialTheme())

function applyTheme(value) {
  theme.value = value
  document.documentElement.dataset.theme = value
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', THEME_COLORS[value])

  try {
    window.localStorage.setItem(STORAGE_KEY, value)
  } catch {
    return
  }
}

export function useTheme() {
  const isDark = computed(() => theme.value === 'dark')

  function toggleTheme() {
    applyTheme(isDark.value ? 'light' : 'dark')
  }

  return { theme: readonly(theme), isDark, toggleTheme }
}

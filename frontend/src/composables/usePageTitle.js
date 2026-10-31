import { watchEffect } from 'vue'
import { site } from '@/config/site'

export function usePageTitle(source = null) {
  watchEffect(() => {
    const title = typeof source === 'function' ? source() : source
    document.title = title ? `${title} · ${site.name}` : site.title
  })
}

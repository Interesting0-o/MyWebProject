import { watchEffect } from 'vue'
import { site } from '@/config/site'

function setMeta(attribute, key, content) {
  const selector = `meta[${attribute}="${key}"]`
  const existing = document.head.querySelector(selector)

  if (!content) {
    existing?.remove()
    return
  }

  const element = existing ?? document.createElement('meta')
  if (!existing) {
    element.setAttribute(attribute, key)
    document.head.append(element)
  }
  element.setAttribute('content', content)
}

function setCanonical(href) {
  const existing = document.head.querySelector('link[rel="canonical"]')
  const element = existing ?? document.createElement('link')
  if (!existing) {
    element.setAttribute('rel', 'canonical')
    document.head.append(element)
  }
  element.setAttribute('href', href)
}

function toAbsoluteUrl(path) {
  const base = site.url.replace(/\/$/, '')
  return `${base}${path.startsWith('/') ? path : `/${path}`}`
}

function normalizeKeywords(keywords) {
  if (!keywords) {
    return null
  }
  return Array.isArray(keywords) ? keywords.join(', ') : String(keywords)
}

export function useSeo(source = {}) {
  watchEffect(() => {
    const data = typeof source === 'function' ? source() : source
    const title = data.title ? `${data.title} · ${site.name}` : site.title
    const description = data.description ?? site.description
    const keywords = normalizeKeywords(data.keywords ?? site.keywords)
    const url = toAbsoluteUrl(data.path ?? window.location.pathname)

    document.title = title
    setMeta('name', 'description', description)
    setMeta('name', 'keywords', keywords)
    setMeta('name', 'robots', data.robots)
    setMeta('property', 'og:title', title)
    setMeta('property', 'og:description', description)
    setMeta('property', 'og:type', data.type ?? 'website')
    setMeta('property', 'og:url', url)
    setMeta('property', 'og:site_name', site.name)
    setMeta('property', 'og:locale', 'zh_CN')
    setMeta('name', 'twitter:card', 'summary')
    setMeta('name', 'twitter:title', title)
    setMeta('name', 'twitter:description', description)
    setCanonical(url)
  })
}

import { mkdir, writeFile } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { site } from '../src/config/site.js'
import { posts } from '../src/data/posts.js'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const publicDir = resolve(root, 'public')
const baseUrl = site.url.replace(/\/$/, '')

function escapeXml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;')
}

function toRfc822(value) {
  return new Date(`${value}T09:00:00+08:00`).toUTCString()
}

function postUrl(post) {
  return `${baseUrl}/posts/${post.slug}`
}

const items = posts
  .map((post) => {
    const categories = post.tags
      .map((tag) => `      <category>${escapeXml(tag)}</category>`)
      .join('\n')

    return `    <item>
      <title>${escapeXml(post.title)}</title>
      <link>${escapeXml(postUrl(post))}</link>
      <guid isPermaLink="true">${escapeXml(postUrl(post))}</guid>
      <pubDate>${toRfc822(post.date)}</pubDate>
      <description>${escapeXml(post.summary)}</description>
${categories}
    </item>`
  })
  .join('\n')

const lastBuildDate = toRfc822(posts[0]?.date ?? new Date().toISOString().slice(0, 10))

const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${escapeXml(site.title)}</title>
    <link>${escapeXml(baseUrl)}</link>
    <description>${escapeXml(site.description)}</description>
    <language>zh-CN</language>
    <lastBuildDate>${lastBuildDate}</lastBuildDate>
    <managingEditor>${escapeXml(`${site.author.email} (${site.author.name})`)}</managingEditor>
    <atom:link href="${escapeXml(`${baseUrl}/rss.xml`)}" rel="self" type="application/rss+xml" />
${items}
  </channel>
</rss>
`

const staticPaths = [
  { path: '/', priority: '1.0' },
  { path: '/archive', priority: '0.8' },
  { path: '/tags', priority: '0.7' },
  { path: '/about', priority: '0.7' },
  { path: '/privacy', priority: '0.3' },
  { path: '/disclaimer', priority: '0.3' },
]

const postEntries = posts.map((post) => ({
  path: `/posts/${post.slug}`,
  lastmod: post.date,
  priority: '0.9',
}))

const urlEntries = [...postEntries, ...staticPaths]
  .map(({ path, lastmod, priority }) => {
    const lastmodTag = lastmod ? `\n    <lastmod>${lastmod}</lastmod>` : ''
    return `  <url>
    <loc>${escapeXml(`${baseUrl}${path}`)}</loc>${lastmodTag}
    <priority>${priority}</priority>
  </url>`
  })
  .join('\n')

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urlEntries}
</urlset>
`

const robots = `User-agent: *
Allow: /

Sitemap: ${baseUrl}/sitemap.xml
`

await mkdir(publicDir, { recursive: true })
await Promise.all([
  writeFile(resolve(publicDir, 'rss.xml'), rss),
  writeFile(resolve(publicDir, 'sitemap.xml'), sitemap),
  writeFile(resolve(publicDir, 'robots.txt'), robots),
])

console.log('Generated public/rss.xml, public/sitemap.xml and public/robots.txt')

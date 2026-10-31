import { test, expect } from '@playwright/test'

test('renders the blog home page', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByRole('heading', { level: 1 })).toContainText('KMnO4')
  await expect(page.getByRole('heading', { name: '最新文章' })).toBeVisible()
  await expect(page.getByRole('link', { name: '用 Vue 3 组合式 API 重构一个旧页面' })).toBeVisible()
})

test('opens a post from the home page', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('link', { name: '用 Vue 3 组合式 API 重构一个旧页面' }).click()

  await expect(
    page.getByRole('heading', { level: 1, name: '用 Vue 3 组合式 API 重构一个旧页面' }),
  ).toBeVisible()
  await expect(page.getByRole('link', { name: '返回首页' })).toBeVisible()
})

test('keeps the backend tester on the hidden health page', async ({ page }) => {
  await page.route('**/api/health', (route) => route.fulfill({ json: { status: 'ok' } }))
  await page.goto('/health')

  await expect(page.getByRole('heading', { name: '后端连接测试' })).toBeVisible()
  await page.getByRole('button', { name: '测试连接' }).click()
  await expect(page.getByText('连接成功')).toBeVisible()
})

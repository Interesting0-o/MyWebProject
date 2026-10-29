import { test, expect } from '@playwright/test'

// See here how to get started:
// https://playwright.dev/docs/intro
test('visits the app root url', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { name: '后端连接测试' })).toBeVisible()
  await expect(page.getByRole('button', { name: '测试连接' })).toBeVisible()
})

test('shows the backend response after clicking the button', async ({ page }) => {
  await page.route('**/api/health', (route) => route.fulfill({ json: { status: 'ok' } }))
  await page.goto('/')
  await page.getByRole('button', { name: '测试连接' }).click()
  await expect(page.getByText('连接成功')).toBeVisible()
})

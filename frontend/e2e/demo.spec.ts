import { expect, test } from '@playwright/test'

test('record-store decision, compare, export, sandbox, and study lock', async ({ page }) => {
  await page.goto('/lab/golden_record_store_weekend_v1')
  await expect(page.getByRole('heading', { name: 'One prior calming outing' })).toBeVisible()
  await page.getByRole('button', { name: 'Run method' }).click()
  await expect(page.getByText(/browsing a record store or taking a quiet walk/i)).toBeVisible()
  await expect(page.getByText(/mem_sensitive_family_conflict/)).toBeVisible()
  const download = page.waitForEvent('download')
  await page.getByRole('button', { name: /Export run JSON/ }).click()
  await download
  await page.getByRole('link', { name: /Compare all six/ }).click()
  await page.getByRole('button', { name: 'Run comparison' }).click()
  await expect(page.locator('.comparison-card')).toHaveCount(6)
  await page.goto('/sandbox')
  await page.getByLabel('New synthetic memory').fill('A synthetic library visit felt restorative.')
  await page.getByRole('button', { name: 'Add' }).click()
  await page.getByRole('button', { name: 'Send through Reconsider-Lite' }).click()
  await expect(page.locator('.assistant-bubble')).toBeVisible()
  await page.goto('/study')
  await expect(page.getByText('Participant collection is locked.')).toBeVisible()
})

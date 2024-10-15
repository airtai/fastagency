import { expect, test } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Mesop/);
});

test('get started link', async ({ page }) => {
  await page.goto('/');

  // Click the get started link.
  await page.getByRole('link', { name: '/Student and teacher/' }).click();

  // Expects workflow to get started.
  await page.locator('p')
    .filter({ hasText: "Workflow started" })
    .isVisible()

});

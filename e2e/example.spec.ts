import { expect, test } from '@playwright/test';


test('student teacher', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Mesop/);
  const startWorkflow = await page.getByRole('button', { name: 'Student and teacher learning' })
  await startWorkflow.click()
  const started = await page.getByText("Workflow started")
  const textInput = await page.getByRole("textbox").fill("triangles")
  await page.locator('button').filter({ hasText: 'send' }).click()
  const completed = await page.getByText('Workflow copleted:')
  expect(completed)
});

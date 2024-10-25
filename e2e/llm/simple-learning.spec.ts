import { expect, test } from '@playwright/test';

test('student teacher', async ({ page }) => {
    test.setTimeout(320000)
    await page.goto('/');
    await expect(page).toHaveTitle(/Mesop/);
    const startWorkflow = await page.getByRole('button', { name: 'Student and teacher learning' })
    await startWorkflow.click()
    const started = await page.getByText("Workflow started")
    await expect(started).toBeVisible()
    await page.getByRole("textbox").fill("triangles")
    await page.locator('button').filter({ hasText: 'send' }).click()
    await expect(page.getByText('triangles', { exact: true })).toBeVisible()
    const completed = await page.getByText('Workflow completed:')
    const slowExpect = expect.configure({ timeout: 320000 });
    await slowExpect(completed, {}).toBeVisible()
});

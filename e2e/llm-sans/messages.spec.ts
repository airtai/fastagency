import { expect, test } from '@playwright/test';

test('text message', async ({ page }) => {
    await page.goto('/');
    const startWorkflow = await page.getByRole('button', { name: 'Text message test' })
    await startWorkflow.click()
    const started = await page.getByText("Workflow started")
    await expect(started).toBeVisible()
    const suggested = await page.getByText('Text message body')
    await expect(suggested).toBeVisible()
});

test('text input message', async ({ page }) => {
    await page.goto('/');
    const startWorkflow = await page.getByRole('button', { name: 'Text input message test' })
    await startWorkflow.click()
    const started = await page.getByText("Workflow started")
    await expect(started).toBeVisible()
    await page.getByRole("textbox").fill("My final answer")

    await page.locator('button').filter({ hasText: 'send' }).click()

    const result = await page.getByText('My final answer')
    await expect(result).toBeVisible()
});

test('multiple choice message - single', async ({ page }) => {
    await page.goto('/');
    const startWorkflow = await page.getByRole('button', { name: 'Multiple choice - single' })
    await startWorkflow.click()
    const started = await page.getByText("Workflow started")
    await expect(started).toBeVisible()
    await page.getByRole("button", { name: "Tests? What tests??" }).click()
    const result = await page.getByText('you have chosen: Tests? What tests??')
    await expect(result).toBeVisible()
});

test('multiple choice message - many', async ({ page }) => {
    await page.goto('/');
    const startWorkflow = await page.getByRole('button', { name: 'Multiple choice - many' })
    await startWorkflow.click()
    const started = await page.getByText("Workflow started")
    await expect(started).toBeVisible()
    await page.getByLabel('Tests? What tests??').click()
    await page.getByLabel('I am currently running them').click()
    await page.getByRole('button', { name: 'OK' }).click()

    const result = await page.getByText('you have chosen: Tests? What tests??,I am currently running them')
    await expect(result).toBeVisible()
});


test('suggested function call', async ({ page }) => {
    await page.goto('/');
    const startWorkflow = await page.getByRole('button', { name: 'Suggested Function Call Message' })
    await startWorkflow.click()
    const started = await page.getByText("Workflow started")
    await expect(started).toBeVisible()
    const suggested = await page.getByText('Suggested function call:')
    await expect(suggested).toBeVisible()
});

test('function call execution', async ({ page }) => {
    await page.goto('/');
    const startWorkflow = await page.getByRole('button', { name: 'Function Call Execution Message' })
    await startWorkflow.click()
    const started = await page.getByText("Workflow started")
    await expect(started).toBeVisible()
    const suggested = await page.getByText('Function call execution:')
    await expect(suggested).toBeVisible()
});

test('error message', async ({ page }) => {
    await page.goto('/');
    const startWorkflow = await page.getByRole('button', { name: 'Error Message' })
    await startWorkflow.click()
    const started = await page.getByText("Workflow started")
    await expect(started).toBeVisible()
    const short = await page.getByText('This is an Error in short form')
    await expect(short).toBeVisible()
    const longer = await page.getByText('This is an Error in somewhat longer form')
    await expect(longer).toBeVisible()
});

test('workflow started', async ({ page }) => {
    await page.goto('/');
    const startWorkflow = await page.getByRole('button', { name: 'Workflow started' })
    await startWorkflow.click()
    const started = await page.getByText("Workflow started")
    await expect(started).toBeVisible()
    const name = await page.getByText('_workflow_started_')
    await expect(name).toBeVisible()
    const desc = await page.getByText('The beginnings are delicate times...')
    await expect(desc).toBeVisible()
});

test('workflow completed', async ({ page }) => {
    await page.goto('/');
    const startWorkflow = await page.getByRole('button', { name: 'Workflow completed' })
    await startWorkflow.click()
    const started = await page.getByText("Workflow started")
    await expect(started).toBeVisible()
    const completed = await page.getByText('This workflow has completed')
    await expect(completed).toBeVisible()
});

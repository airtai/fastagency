// playwright setting for tests that run with unicorn
import { defineConfig } from "./e2e/playwright.base.config.ts";

export default defineConfig(
    {
        testDir: './e2e/llm',
        use: {
            /* Base URL to use in actions like `await page.goto('/')`. */
            baseURL: 'http://127.0.0.1:8000',

            /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
            trace: 'on-first-retry',
        },
        webServer: {
            command: 'gunicorn e2e.llm-sans.main:app',
            url: 'http://127.0.0.1:8000',
            reuseExistingServer: !process.env.CI,
        }
    }
)

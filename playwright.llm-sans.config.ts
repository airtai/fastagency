import { defineConfig } from "./e2e/playwright.base.config.ts";

export default defineConfig(
    {
        testDir: './e2e/llm-sans',
        webServer: {
            command: 'fastagency run e2e/llm-sans/main.py',
            url: 'http://127.0.0.1:32123',
            //        env: testEnv,
            reuseExistingServer: true,
        },
    },
)

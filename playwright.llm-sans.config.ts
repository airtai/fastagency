import { defineConfig } from "./e2e/playwright.base.config.ts";

export default defineConfig(
    {
        testDir: './e2e/llm-sans',
    }
)

import { defineConfig, devices } from '@playwright/test';

/**
 * GRANGER Level 4 UI Testing Configuration
 * Validates real browser interactions with visual regression testing
 */
export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'reports/html' }],
    ['json', { outputFile: 'reports/test-results.json' }],
    ['list']
  ],
  
  use: {
    // Base URL for all three UI modules
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    
    // Collect trace for debugging
    trace: 'on-first-retry',
    
    // Screenshot on failure
    screenshot: 'only-on-failure',
    
    // Video recording for visual validation
    video: 'retain-on-failure',
    
    // Viewport for desktop testing
    viewport: { width: 1280, height: 720 },
    
    // Emulate real user behavior
    actionTimeout: 0,
    navigationTimeout: 30000,
    
    // Style guide colors for validation
    colorScheme: 'light',
  },

  projects: [
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        // Force headed mode for visual validation
        headless: false,
        // Enable GPU for 60fps validation
        launchOptions: {
          args: ['--enable-gpu']
        }
      },
    },
    {
      name: 'firefox',
      use: { 
        ...devices['Desktop Firefox'],
        headless: false 
      },
    },
    {
      name: 'webkit',
      use: { 
        ...devices['Desktop Safari'],
        headless: false 
      },
    },
    // Mobile viewports
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  // Dev server configuration
  webServer: [
    {
      command: 'npm run dev:chat',
      port: 3000,
      reuseExistingServer: !process.env.CI,
    },
    {
      command: 'npm run dev:annotator',
      port: 3001,
      reuseExistingServer: !process.env.CI,
    },
    {
      command: 'npm run dev:terminal',
      port: 3002,
      reuseExistingServer: !process.env.CI,
    }
  ],
});
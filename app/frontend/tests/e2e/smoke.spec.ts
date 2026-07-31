import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should load the homepage', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/AI Learning/);
  });
});

test.describe('Health Check', () => {
  test('should return healthy status', async ({ request }) => {
    const response = await request.get('http://localhost:8000/api/v1/health');
    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    expect(body).toHaveProperty('status');
  });
});

test.describe('API Documentation', () => {
  test('should load Swagger UI', async ({ page }) => {
    await page.goto('http://localhost:8000/docs');
    await expect(page.locator('text=AI Learning Platform')).toBeVisible();
  });
});

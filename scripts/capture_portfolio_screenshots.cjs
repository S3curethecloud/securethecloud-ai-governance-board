const { chromium } = require("playwright");
const fs = require("fs/promises");

const baseUrl = process.env.DEMO_URL || "https://securethecloud-ai-governance-board.fly.dev";
const outDir = "docs/screenshots";

const shots = [
  ["01-executive-overview.png", "SecureTheCloud AI Governance Board", 0],
  ["02-ai-system-intake.png", "AI System Intake", 0.24],
  ["03-governance-review.png", "Governance Committee", 0.42],
  ["04-nist-eu-hipaa-mapping.png", "NIST AI RMF Mapping Console", 0.56],
  ["05-board-audit-trail.png", "Board Audit Trail", 0.74],
  ["06-evidence-export-memo.png", "Evidence Package Export", 0.88]
];

async function scrollToTextOrRatio(page, text, ratio) {
  try {
    const locator = page.getByText(text, { exact: false }).first();
    await locator.scrollIntoViewIfNeeded({ timeout: 8000 });
    await page.waitForTimeout(1200);
    return;
  } catch {
    const scrollHeight = await page.evaluate(() => document.documentElement.scrollHeight);
    const viewportHeight = await page.evaluate(() => window.innerHeight);
    const y = Math.max(0, Math.floor((scrollHeight - viewportHeight) * ratio));
    await page.evaluate((targetY) => window.scrollTo(0, targetY), y);
    await page.waitForTimeout(1200);
  }
}

(async () => {
  await fs.mkdir(outDir, { recursive: true });

  const browser = await chromium.launch({ headless: true });

  const page = await browser.newPage({
    viewport: { width: 1440, height: 1400 },
    deviceScaleFactor: 1
  });

  await page.goto(baseUrl, { waitUntil: "networkidle", timeout: 90000 });
  await page.waitForTimeout(3000);

  for (const [filename, text, ratio] of shots) {
    await scrollToTextOrRatio(page, text, ratio);
    await page.screenshot({ path: `${outDir}/${filename}`, fullPage: false });
    console.log(`Captured ${filename}`);
  }

  const mobile = await browser.newPage({
    viewport: { width: 390, height: 1400 },
    deviceScaleFactor: 2,
    isMobile: true
  });

  await mobile.goto(baseUrl, { waitUntil: "networkidle", timeout: 90000 });
  await mobile.waitForTimeout(3000);
  await mobile.screenshot({ path: `${outDir}/07-mobile-responsive.png`, fullPage: false });
  console.log("Captured 07-mobile-responsive.png");

  await browser.close();
})();

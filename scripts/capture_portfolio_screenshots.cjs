const { chromium } = require("playwright");
const fs = require("fs/promises");

const baseUrl = process.env.DEMO_URL || "https://securethecloud-ai-governance-board.fly.dev";
const outDir = "docs/screenshots";

const shots = [
  ["01-executive-overview.png", "SecureTheCloud AI Governance Board"],
  ["02-ai-system-intake.png", "Phase 3"],
  ["03-governance-review.png", "Phase 4"],
  ["04-nist-eu-hipaa-mapping.png", "Phase 5"],
  ["05-board-audit-trail.png", "Phase 7"],
  ["06-evidence-export-memo.png", "Phase 8"]
];

(async () => {
  await fs.mkdir(outDir, { recursive: true });

  const browser = await chromium.launch({ headless: true });

  const page = await browser.newPage({
    viewport: { width: 1440, height: 1400 },
    deviceScaleFactor: 1
  });

  await page.goto(baseUrl, { waitUntil: "networkidle", timeout: 90000 });
  await page.waitForTimeout(3000);

  for (const [filename, text] of shots) {
    try {
      await page.getByText(text, { exact: false }).first().scrollIntoViewIfNeeded({ timeout: 8000 });
      await page.waitForTimeout(1000);
    } catch {
      console.log(`Could not scroll to "${text}"; capturing current viewport.`);
    }

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

#!/usr/bin/env node
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";

const root = resolve(new URL("..", import.meta.url).pathname);
const configPath = resolve(root, "design-harness.config.json");
const outPath = process.argv[2]
  ? resolve(process.cwd(), process.argv[2])
  : resolve(root, "reports/qa-report.draft.json");

const config = JSON.parse(await readFile(configPath, "utf8"));

const categoryScores = Object.fromEntries(
  config.qaCategories.map((category) => [category, null])
);

const report = {
  source: {
    figmaFileKey: config.source.figmaFileKey,
    nodeId: config.source.sourceNodeId,
    screenshotPath: ""
  },
  candidate: {
    nodeId: "",
    screenshotPath: "",
    implementationPath: ""
  },
  overallScore: 0,
  categoryScores,
  issues: [],
  verdict: "needs_repair",
  nextStep: "Fill source/candidate screenshots, run Visual QA Agent, then update scores and issues."
};

await mkdir(dirname(outPath), { recursive: true });
await writeFile(outPath, `${JSON.stringify(report, null, 2)}\n`);
console.log(`Created QA report draft: ${outPath}`);


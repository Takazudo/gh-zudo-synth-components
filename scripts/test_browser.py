#!/usr/bin/env python3
"""Test the exact offline browser; no network navigation or WebGL success is assumed."""
import argparse, asyncio, json, shutil
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]

async def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chromium",default=shutil.which("chromium") or shutil.which("chromium-browser"))
    args=parser.parse_args()
    if not args.chromium:parser.error("Set --chromium to an installed Chrome/Chromium executable")
    checks=[];errors=[];requests=[];console=[]
    def check(name,value,detail=None):
        checks.append(dict(name=name,passed=bool(value),detail=detail))
    rows=json.loads((ROOT/"corpus/catalog.json").read_text())
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=args.chromium,headless=True,
            args=["--no-sandbox","--disable-dev-shm-usage"])
        page=await browser.new_page(viewport={"width":1440,"height":1050})
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.on("request",lambda r:requests.append(r.url))
        page.on("console",lambda m:console.append(m.text) if m.type=="error" else None)
        await page.set_content((ROOT/"doc/public/assets/corpus-browser.html").read_text(),wait_until="load")
        check("86 embedded profiles",await page.evaluate("window.__CORPUS_READY__.profiles")==86)
        check("25 embedded model assets",await page.evaluate("window.__CORPUS_READY__.models")==25)
        check("86 selectable profiles",await page.locator("#list [data-part]").count()==86)
        await page.locator('[data-tab="model"]').click()
        await page.wait_for_selector('#viewer[data-ready="alps-rk09l1140a5l"]',timeout=15000)
        backend=await page.locator("#viewer").get_attribute("data-backend")
        check("renderer identifies its actual backend",backend in ("WebGL","SVG fallback"),backend)
        check("retained STEP visible",await page.locator("#viewer canvas,#viewer svg").count()==1)
        first=await page.locator("#viewer").screenshot()
        await page.locator('[data-view="top"]').click()
        check("camera changes projection",first!=await page.locator("#viewer").screenshot())
        await page.locator("#wireframe").click()
        check("wireframe state",await page.locator("#wireframe").get_attribute("aria-pressed")=="true")
        await page.locator("#wireframe").click()
        await page.locator('[data-tab="sources"]').click()
        check("source links",await page.locator('#sources a[href^="https:"]').count()>0)
        check("retained file paths","Package:" in await page.locator("#sources").inner_text())
        await page.locator("#search").fill("LF398")
        check("part search",await page.locator('[data-part="sample-hold"]').count()==1)
        await page.locator("#search").fill("NO-SUCH-PART-123")
        check("empty search",await page.locator("#list .empty").count()==1)
        await page.locator("#search").fill("")
        await page.locator("#models-only").check()
        check("38 viewable profiles",await page.locator("#list [data-part]").count()==38)
        await page.locator("#models-only").uncheck()
        await page.locator("#category").select_option("controls")
        check("category filter",await page.locator("#list [data-part]").count()==sum(r["category"]=="controls" for r in rows))
        await page.locator('[data-part="bourns-ptl20"]').click()
        await page.locator('[data-tab="model"]').click()
        check("missing model explicit",await page.locator("#no-model").is_visible())
        check("previous model not shown",not await page.locator("#viewer").is_visible())
        await page.locator("#category").select_option("")
        unique={}
        for r in rows:
            m=r.get("model")
            if m:unique.setdefault((m["kind"],m["id"]),r)
        for key,r in unique.items():
            await page.locator(f'[data-part="{r["id"]}"]').click()
            await page.wait_for_selector(f'#viewer[data-ready="{r["id"]}"]',timeout=15000)
            check("model renders: "+key[1],
                  await page.locator("#viewer canvas,#viewer svg").count()==1 and
                  "Rendered via" in await page.locator("#model-status").inner_text())
        await page.set_viewport_size({"width":393,"height":852})
        await page.locator('[data-part="alps-rk09l1140a5l"]').click()
        await page.locator('[data-tab="research"]').click()
        check("mobile research width",await page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"))
        await page.locator('[data-tab="model"]').click()
        check("mobile model width",await page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"))
        check("mobile visible model",await page.locator("#viewer").is_visible())
        await browser.close()
    report={"checks":checks,"passed":sum(c["passed"] for c in checks),"failed":sum(not c["passed"] for c in checks),
            "unhandled_errors":errors,"requests":requests,"console_errors":console,"backend":backend,
            "scope":"Exact HTML bytes via set_content. Local navigation and native framework WebGL NOT TESTED."}
    (ROOT/"provenance/validation/browser-repro.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"passed":report["passed"],"failed":report["failed"],
                      "unhandled_errors":len(errors),"requests":len(requests),"backend":backend}))
    return 1 if report["failed"] or errors or requests else 0

if __name__=="__main__":raise SystemExit(asyncio.run(main()))

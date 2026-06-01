import asyncio
import json
import os
from datetime import datetime
from playwright.async_api import async_playwright

# Ensure output directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "scraped_reviews.json")

async def scrape_reviews(target_url: str, max_pages: int = 3):
    print(f"🚀 Starting scraper engine for: {target_url}")
    
    async with async_playwright() as p:
        # Launch headless Chromium browser
        browser = await p.chromium.launch(headless=True)
        # Create a new browser context mimicking a standard desktop user agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        all_reviews = []
        current_page = 1
        url = target_url

        while current_page <= max_pages and url:
            print(f"📄 Scraping Page {current_page}...")
            try:
                await page.goto(url, timeout=60000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000) # Give Trustpilot's React hydration a moment

                # Trustpilot wraps reviews in an 'article' tag
                review_elements = await page.query_selector_all("article")
                
                if not review_elements:
                    print("⚠️ No review elements found. Trustpilot may have blocked the IP or changed selectors.")
                    break

                for element in review_elements:
                    # Target Trustpilot's specific data attributes
                    name_el = await element.query_selector("[data-consumer-name-typography='true']")
                    name = await name_el.inner_text() if name_el else "Anonymous"

                    # Trustpilot rating is usually in an image alt text like "Rated 1 out of 5 stars"
                    rating_el = await element.query_selector("[data-service-review-rating] img")
                    rating = "N/A"
                    if rating_el:
                        alt_text = await rating_el.get_attribute("alt")
                        # Extract just the number (e.g., "1" from "Rated 1 out of 5 stars")
                        if alt_text:
                            rating = alt_text.split(" ")[1] if "Rated" in alt_text else alt_text

                    # The actual review text body
                    text_el = await element.query_selector("[data-service-review-text-typography='true']")
                    text = await text_el.inner_text() if text_el else ""

                    # The timestamp
                    date_el = await element.query_selector("time[data-service-review-date-time-ago='true'], time")
                    date_str = "N/A"
                    if date_el:
                        date_str = await date_el.get_attribute("datetime") or await date_el.inner_text()

                    # Only append if there's actual text (ignores star-only ratings)
                    if text.strip():
                        all_reviews.append({
                            "reviewer_name": name.strip(),
                            "rating": rating.strip(),
                            "review_text": text.strip(),
                            "date": date_str.strip(),
                            "scraped_at": datetime.utcnow().isoformat()
                        })
                print(f"✅ Extracted {len(all_reviews)} reviews so far.")

                # Trustpilot's specific Next Page button
                next_button = await page.query_selector("a[name='pagination-button-next']")
                if next_button:
                    next_url = await next_button.get_attribute("href")
                    url = f"https://www.trustpilot.com{next_url}" if next_url else None
                    current_page += 1
                else:
                    print("🏁 Reached the last page or next button not found.")
                    url = None

            except Exception as e:
                print(f"❌ Error encountered while scraping page {current_page}: {str(e)}")
                break

        # Save collected elements to a local JSON file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_reviews, f, indent=4, ensure_ascii=False)
        
        print(f"\n🎉 Scraping phase complete! Saved {len(all_reviews)} reviews to '{OUTPUT_FILE}'.")
        await browser.close()

if __name__ == "__main__":
    # Test target URL: replace with a real public business review URL for your testing
    TEST_URL = "https://www.trustpilot.com/review/www.vodafone.co.uk"
    
    # Run the asynchronous loop
    asyncio.run(scrape_reviews(TEST_URL, max_pages=2))
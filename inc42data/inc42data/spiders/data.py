import scrapy
import json

class DataSpider(scrapy.Spider):
    name = "data"
    allowed_domains = ["inc42.com"]
    
    # Adding all URLs to scrape
    start_urls = [
        "https://inc42.com/startups/can-this-jaipur-based-startups-3-in-1-bladeless-fans-take-over-indian-homes/",
        "https://inc42.com/buzz/ather-energy-fy24-revenue-declines-on-reduction-in-fame-ii-subsidy-loss-up-23-to-inr-1060-cr/",
        "https://inc42.com/features/indian-startup-fy24-financials-tracker-revenue-expense-loss-more/",
        "https://inc42.com/features/swiggy-litmus-test-ipo-food-delivery-quick-commerce/",
        "https://inc42.com/startups/can-newtrace-turbocharge-indias-push-for-green-hydrogen-dominance/"
    ]
    
    # List to store all articles data
    articles_data = []

    def parse(self, response):
        # Extract data using appropriate CSS selectors
        article_url = response.url
        title = response.css("h1.entry-title::text").get()
        author_name = response.css("span.author a::text").get()
        author_url = response.css("span.author a::attr(href)").get()
        article_content = response.css("div.single-post-content p span::text").getall()
        published_date = response.css("span.date::text").get()

        # Structure the data in a dictionary for each article
        article_data = {
            "Article URL": article_url,
            "Title": title,
            "Author Name": author_name,
            "Author URL": author_url,
            "Article Content": " ".join(article_content),
            "Published Date": published_date
        }

        # Append each article data to the articles_data list
        self.articles_data.append(article_data)
        
        # When all articles are scraped, save them into a single JSON file
        if len(self.articles_data) == len(self.start_urls):
            filename = 'all_articles.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.articles_data, f, ensure_ascii=False, indent=4)

            self.log(f"Saved all articles to {filename}")

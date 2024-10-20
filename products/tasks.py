from celery import shared_task
from .models import Brand
from .scraper import scrape_amazon_products
import logging

logger = logging.getLogger("product_logs")

@shared_task
def scrape_products_for_all_brands():
    brands = Brand.objects.all()

    for brand in brands:
        try:
            scrape_amazon_products(brand)
        except Exception as e:
            logger.info(f"Error scraping {brand.name}: {e}")
import requests, random, logging
from django.conf import settings

from bs4 import BeautifulSoup
from .models import Product


logger = logging.getLogger("product_logs")

HEADERS = [
    # List of User-Agent headers to rotate
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    # Add more headers here...
]

def scrape_amazon_products(brand):

    fetched_successfully = False
    retries = 0

    headers = {'User-Agent': random.choice(HEADERS)}
    logger.info(f"Start fetching data from {brand.name} using website_url {brand.website_url}")

    while not fetched_successfully and settings.SCRAPER_RETRIES >= retries:

        response = requests.get(brand.website_url, headers=headers)
        retries += 1

        if response.status_code == 200:
            fetched_successfully = True
            soup = BeautifulSoup(response.content, 'lxml')

            # Assuming product list is found in a specific container
            product_containers = soup.find_all('div', class_='s-result-item')

            for container in product_containers:
                try:
                    name = container.find('span', class_='a-size-base-plus').get_text()
                    asin = container['data-asin']
                    image_url = container.find('img')['src']

                    # Find SKU or other fields as needed
                    sku = container.get('data-sku', None)

                    # Save product to database
                    product, created = Product.objects.get_or_create(
                        asin=asin,
                        defaults={'name': name, 'image': image_url, 'sku': sku, 'brand': brand}
                    )

                    # If product exists, update fields
                    if not created:
                        product.name = name
                        product.image = image_url
                        product.sku = sku
                        product.save()

                except AttributeError:
                    # Skip items that don't have the required data
                    continue
            logger.info(f"All data fetched from the given web url on {retries} try")
        else:
            logger.info(f"Failed on {retries} try to retrieve page: {response.status_code}")

    if retries > settings.SCRAPER_RETRIES:
        logger.info(f"Failed to fetch the data from {brand.name} after retrying {retries} times.")


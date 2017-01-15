# mercenary
> mercenary is a function can maximize your desire

# Requirements
```bash
Python 3.5.X
```

# Installation
```bash
% pip install -r requirements.txt --upgrade
```

# Usage
```bash
# Run
% scrapy crawl furusato-tax-paging -a query="いくら"

# Debug
% scrapy crawl furusato-tax-product -a url="https://www.furusato-tax.jp/japan/prefecture/item_detail/22212/232992" -t jsonlines -o result.json
```

# Deployment
```bash
# Login to scrapinghub.com
% shub login

# Generate eggs including libraries
% shub migrate-eggs

# Deploy to scrapinghub.com
% shub deploy
```

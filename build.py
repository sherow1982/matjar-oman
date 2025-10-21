import json
import os
import urllib.parse
import random

# --- الإعدادات ---
JSON_FILE = 'products.json'
OUTPUT_DIR = 'products'
PHONE_NUMBER = '+201110760081' # !!! قم بتغيير هذا الرقم

REVIEW_TEXTS = [
    "والله منتج فنان وحل لي مشكلة كبيرة. أنصحكم فيه وبقوة.",
    "ما شاء الله على الجودة، صراحة فرق عن بو فالسوق. يستاهل كل ريال.",
    "وصلني بسرعة والتغليف كان ممتاز. المنتج نفسه نفس ما توقعت وأحسن بعد.",
    "حبيته واجد، عملي ومفيد فالبيت. كل حد يسألني عنه.",
    "لا تترددوا، منتج بطل ويستاهل التجربة. ما ندمت إني خذيته."
]

def get_stars_html(rating):
    stars = ''
    for i in range(5):
        if i < rating:
            stars += '<span style="color:gold;font-size:20px;">&#9733;</span>'
        else:
            stars += '<span style="color:#ccc;font-size:20px;">&#9733;</span>'
    return stars

def generate_reviews_html():
    reviews_html = ''
    for _ in range(random.randint(2, 4)):
        rating = random.randint(4, 5)
        review = {
            "stars": get_stars_html(rating),
            "author": "مشتري موثوق",
            "text": random.choice(REVIEW_TEXTS)
        }
        reviews_html += f"""
        <div class="review-item">
            <div class="review-stars">{review['stars']}</div>
            <p class="review-author">{review['author']}</p>
            <p class="review-text">{review['text']}</p>
        </div>
        """
    return reviews_html

PRODUCT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Cairo', sans-serif; margin: 0; padding: 20px; background-color: #f9f9f9; color: #333; }}
        .container {{ max-width: 800px; margin: 20px auto; background-color: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        img {{ max-width: 100%; border-radius: 8px; margin-bottom: 20px; }}
        h1 {{ text-align: center; font-size: 2.5rem; }}
        .price {{ text-align: center; font-size: 2rem; font-weight: bold; color: #28a745; }}
        .old-price {{ color: #999; text-decoration: line-through; font-size: 1.2rem; }}
        .description {{ line-height: 1.8; white-space: pre-wrap; margin: 20px 0; text-align: right; border-top: 1px solid #eee; padding-top: 20px;}}
        .buttons-container {{ text-align: center; margin: 30px 0; }}
        .btn {{ border-radius: 50px; border: none; padding: 12px 30px; font-size: 1.1rem; font-weight: bold; text-decoration: none; display: inline-block; background-color: #007bff; color: white; }}
        .reviews-section {{ margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }}
        .review-item {{ border-bottom: 1px solid #eee; padding-bottom: 15px; margin-bottom: 15px; }}
        .review-stars {{ margin-bottom: 5px; }}
        .review-author {{ font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <img src="{image}" alt="{title}">
        <p class="price">{new_price} <span class="old-price">{old_price}</span></p>
        <div class="buttons-container">
            <a href="{original_link}" class="btn" target="_blank">اشتريه الآن من المتجر الأصلي</a>
        </div>
        <p class="description">{description}</p>
        <div class="reviews-section">
            <h2>تقييمات المشترين</h2>
            {reviews_html}
        </div>
    </div>
</body>
</html>
"""

def build_product_pages():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)

    for product in products:
        title = product.get('العنوان', 'منتج')
        html_content = PRODUCT_TEMPLATE.format(
            title=title,
            image=product.get('رابط الصورة', ''),
            new_price=product.get('ﺎﻠﺴﻋﺭ ﺎﻠﻤﺨﻔَّﺿ', ''),
            old_price=product.get('ﺎﻠﺴﻋﺭ', ''),
            description=product.get('الوصف', '').replace('\\n', '<br>'),
            original_link=product.get('الرابط', '#'),
            reviews_html=generate_reviews_html()
        )
        
        file_path = os.path.join(OUTPUT_DIR, f"{urllib.parse.quote(title)}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"تم إنشاء: {file_path}")

if __name__ == '__main__':
    build_product_pages()
    print("\nاكتمل إنشاء جميع صفحات المنتجات.")


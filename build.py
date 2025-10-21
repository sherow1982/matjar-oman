import json
import os
import urllib.parse

# --- الإعدادات ---
JSON_FILE = 'products.json'
OUTPUT_DIR = 'products'
PHONE_NUMBER = '+201110760081' # !!! قم بتغيير هذا الرقم

# --- قالب صفحة المنتج ---
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
        .container {{ max-width: 800px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        img {{ max-width: 100%; border-radius: 8px; margin-bottom: 20px; }}
        h1 {{ text-align: center; }}
        .price {{ text-align: center; font-size: 2rem; font-weight: bold; color: #28a745; }}
        .old-price {{ color: #999; text-decoration: line-through; font-size: 1.2rem; }}
        .description {{ line-height: 1.8; white-space: pre-wrap; margin: 20px 0; text-align: right; }}
        .buttons-container {{ text-align: center; margin-top: 20px; }}
        .btn {{ cursor: pointer; border-radius: 50px; border: none; padding: 12px 25px; font-size: 1rem; font-weight: bold; margin: 5px; text-decoration: none; display: inline-block; }}
        .whatsapp-btn {{ background-color: #25D366; color: white; }}
        .details-btn, .buy-now-btn {{ background-color: #007bff; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <img src="{image}" alt="{title}">
        <p class="price">{new_price} <span class="old-price">{old_price}</span></p>
        <div class="buttons-container">
            <a href="{whatsapp_link}" class="btn whatsapp-btn" target="_blank">واتساب</a>
            <button class="btn details-btn" onclick="toggleDescription()">تفاصيل المنتج</button>
            <a href="{original_link}" class="btn buy-now-btn" target="_blank">اشتريه الآن</a>
        </div>
        <p id="description" class="description">{description}</p>
    </div>
    <script>
        function toggleDescription() {{
            const desc = document.getElementById('description');
            const btn = document.querySelector('.details-btn');
            if (desc.style.display !== 'none') {{
                desc.style.display = 'none';
                btn.innerText = 'إظهار التفاصيل';
            }} else {{
                desc.style.display = 'block';
                btn.innerText = 'إخفاء التفاصيل';
            }}
        }}
    </script>
</body>
</html>
"""

# --- السكربت الرئيسي ---
def build_product_pages():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)

    for product in products:
        title = product.get('العنوان', 'منتج')
        whatsapp_message = f"أهلاً، أرغب في طلب المنتج التالي:\n\n*المنتج:* {title}\n*السعر:* {product.get('ﺎﻠﺴﻋﺭ ﺎﻠﻤﺨﻔَّﺿ')}"
        
        html_content = PRODUCT_TEMPLATE.format(
            title=title,
            image=product.get('رابط الصورة', ''),
            new_price=product.get('ﺎﻠﺴﻋﺭ ﺎﻠﻤﺨﻔَّﺿ', ''),
            old_price=product.get('ﺎﻠﺴﻋﺭ', ''),
            description=product.get('الوصف', ''),
            whatsapp_link=f"https://wa.me/{PHONE_NUMBER}?text={urllib.parse.quote(whatsapp_message)}",
            original_link=product.get('الرابط', '#')
        )
        
        file_path = os.path.join(OUTPUT_DIR, f"{urllib.parse.quote(title)}.html")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"تم إنشاء: {file_path}")

if __name__ == '__main__':
    build_product_pages()
    print("\nاكتمل إنشاء جميع صفحات المنتجات.")


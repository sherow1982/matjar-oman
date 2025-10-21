import json
import os
import urllib.parse

# --- الإعدادات ---
JSON_FILE = 'products.json' # اسم ملف المنتجات
OUTPUT_DIR = 'products'     # اسم المجلد الذي سيحتوي على صفحات المنتجات

# --- قالب صفحة المنتج ---
def get_product_html_template(product, phone_number):
    title = product.get('العنوان', 'اسم المنتج غير متوفر')
    image_url = product.get('رابط الصورة', 'https://via.placeholder.com/500')
    description = product.get('الوصف', 'لا يوجد وصف لهذا المنتج.').replace('\n', '<br>')
    discounted_price = product.get('ﺎﻠﺴﻋﺭ ﺎﻠﻤﺨﻔَّﺿ', '')
    original_price = product.get('ﺎﻠﺴﻋﺭ', '')
    
    # رسالة الواتساب
    whatsapp_message = urllib.parse.quote(f"أهلاً، أرغب في طلب المنتج التالي:\n\n*المنتج:* {title}\n*السعر:* {discounted_price}")
    whatsapp_link = f"https://wa.me/{phone_number}?text={whatsapp_message}"

    return f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="container">
                <a href="../index.html" class="brand">متجر عمان</a>
            </div>
        </nav>
    </header>

    <main class="container">
        <section class="product-detail">
            <div class="product-image">
                <img src="{image_url}" alt="{title}">
            </div>
            <div class="product-info">
                <h1>{title}</h1>
                <p class="price-detail">{discounted_price} <span class="old-price">{original_price}</span></p>
                <div class="description">
                    <h2>وصف المنتج</h2>
                    <p>{description}</p>
                </div>
                <a href="{whatsapp_link}" class="whatsapp-btn-large" target="_blank">اطلب الآن عبر واتساب</a>
                <a href="../index.html" class="back-btn">العودة إلى جميع المنتجات</a>
            </div>
        </section>
    </main>
</body>
</html>
"""

# --- السكربت الرئيسي ---
def build_pages():
    # استبدل هذا الرقم برقمك
    whatsapp_number = '+201110760081'

    # قراءة بيانات المنتجات
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            products = json.load(f)
    except FileNotFoundError:
        print(f"خطأ: لم يتم العثور على ملف {JSON_FILE}")
        return
    except json.JSONDecodeError:
        print(f"خطأ: ملف {JSON_FILE} يحتوي على صيغة غير صالحة.")
        return
        
    # إنشاء مجلد المخرجات إذا لم يكن موجودًا
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # إنشاء صفحة لكل منتج
    for product in products:
        product_title = product.get('العنوان')
        if not product_title:
            continue

        # إنشاء اسم ملف صالح للرابط من العنوان العربي
        slug = urllib.parse.quote(product_title)
        file_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
        
        # إنشاء محتوى HTML للصفحة
        html_content = get_product_html_template(product, whatsapp_number)
        
        # كتابة المحتوى إلى الملف
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"تم إنشاء الصفحة: {file_path}")

    print("\nاكتمل بناء جميع صفحات المنتجات بنجاح!")

if __name__ == '__main__':
    build_pages()

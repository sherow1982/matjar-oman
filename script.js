document.addEventListener('DOMContentLoaded', function() {
    fetch('products.json')
        .then(response => response.json())
        .then(products => {
            const productGrid = document.querySelector('.product-grid');
            const phoneNumber = '+201110760081'; // <-- ضع رقم الواتساب الصحيح هنا

            if (!Array.isArray(products)) {
                console.error("خطأ: ملف JSON لا يحتوي على مصفوفة منتجات.");
                return;
            }

            products.forEach(product => {
                const card = document.createElement('div');
                card.className = 'product-card';

                const title = product['العنوان'] || 'منتج';
                const image = product['رابط الصورة'] || 'https://via.placeholder.com/300';
                const discountedPrice = product['ﺎﻠﺴﻋﺭ ﺎﻠﻤﺨﻔَّﺿ'];
                const originalPrice = product['ﺎﻠﺴﻋﺭ'];
                
                // تحويل اسم المنتج العربي إلى رابط صالح للاستخدام في الويب
                const productSlug = encodeURIComponent(title);
                const productPageUrl = `products/${productSlug}.html`;

                const priceHTML = `
                    <p class="price">
                        ${discountedPrice}
                        <span class="old-price">${originalPrice || ''}</span>
                    </p>
                `;

                card.innerHTML = `
                    <a href="${productPageUrl}" class="product-link">
                        <img src="${image}" alt="${title}">
                        <h3>${title}</h3>
                    </a>
                    ${priceHTML}
                    <button class="whatsapp-btn" data-product="${title}" data-price="${discountedPrice}">اطلب عبر واتساب</button>
                `;
                
                productGrid.appendChild(card);
            });

            // تفعيل أزرار الواتساب (الكود لم يتغير هنا)
            document.querySelectorAll('.whatsapp-btn').forEach(button => {
                button.addEventListener('click', function() { /* ... الكود كما هو ... */ });
            });
        })
        .catch(error => {
            console.error('حدث خطأ أثناء تحميل المنتجات:', error);
            productGrid.innerHTML = '<p>عفواً، لم نتمكن من تحميل المنتجات.</p>';
        });
});

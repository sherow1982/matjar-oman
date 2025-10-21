document.addEventListener('DOMContentLoaded', function() {
    // جلب بيانات المنتجات من ملف JSON
    fetch('products.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(products => {
            const productGrid = document.querySelector('.product-grid');
            const phoneNumber = '+201110760081'; // <-- ضع رقم الواتساب الصحيح هنا

            // التأكد من أن الملف يحتوي على مصفوفة
            if (!Array.isArray(products)) {
                console.error("خطأ: ملف JSON لا يحتوي على مصفوفة منتجات.");
                return;
            }

            // إنشاء بطاقة لكل منتج
            products.forEach(product => {
                const card = document.createElement('div');
                card.className = 'product-card';

                const title = product['العنوان'] || 'منتج غير متوفر';
                const image = product['رابط الصورة'] || 'https://via.placeholder.com/300';
                const discountedPrice = product['ﺎﻠﺴﻋﺭ ﺎﻠﻤﺨﻔَّﺿ'];
                const originalPrice = product['ﺎﻠﺴﻋﺭ'];
                
                const priceHTML = `
                    <p class="price">
                        ${discountedPrice}
                        <span class="old-price">${originalPrice || ''}</span>
                    </p>
                `;

                card.innerHTML = `
                    <a href="${product['الرابط'] || '#'}" target="_blank" class="product-link">
                        <img src="${image}" alt="${title}">
                        <h3>${title}</h3>
                    </a>
                    ${priceHTML}
                    <button class="whatsapp-btn" data-product="${title}" data-price="${discountedPrice}">اطلب عبر واتساب</button>
                `;
                
                productGrid.appendChild(card);
            });

            // تفعيل أزرار الواتساب بعد عرض المنتجات
            document.querySelectorAll('.whatsapp-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const productName = this.getAttribute('data-product');
                    const productPrice = this.getAttribute('data-price');
                    
                    const message = `أهلاً، أرغب في طلب المنتج التالي:\n\n*المنتج:* ${productName}\n*السعر:* ${productPrice}`;
                    const encodedMessage = encodeURIComponent(message);
                    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
                    
                    window.open(whatsappUrl, '_blank');
                });
            });
        })
        .catch(error => {
            console.error('حدث خطأ أثناء تحميل المنتجات:', error);
            const productGrid = document.querySelector('.product-grid');
            productGrid.innerHTML = '<p>عفواً، لم نتمكن من تحميل المنتجات. يرجى المحاولة مرة أخرى لاحقاً.</p>';
        });
});

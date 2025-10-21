document.addEventListener('DOMContentLoaded', function() {
    const whatsappButtons = document.querySelectorAll('.whatsapp-btn');
    const phoneNumber = '+201110760081'; //  <-- ضع رقم الواتساب الخاص بك هنا

    whatsappButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productName = this.getAttribute('data-product');
            const productPrice = this.getAttribute('data-price');
            
            // إنشاء رسالة الطلب
            const message = `أهلاً، أرغب في طلب المنتج التالي:\n\n*المنتج:* ${productName}\n*السعر:* ${productPrice}`;
            
            // ترميز الرسالة لتكون صالحة في الرابط
            const encodedMessage = encodeURIComponent(message);
            
            // إنشاء رابط واتساب
            const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
            
            // فتح الرابط في نافذة جديدة
            window.open(whatsappUrl, '_blank');
        });
    });
});

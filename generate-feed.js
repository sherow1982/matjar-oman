const fetch = require('node-fetch');
const fs = require('fs').promises;

const productsUrl = 'https://raw.githubusercontent.com/sherow1982/matjar-oman/main/products.json';

async function generateFeed() {
  try {
    console.log('Fetching products...');
    const response = await fetch(productsUrl);
    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.statusText}`);
    }
    const products = await response.json();
    console.log(`Found ${products.length} products.`);
    
    let xmlItems = '';

    products.forEach(product => {
      const productId = String(product.id || product.العنوان).replace(/&/g, '&amp;');
      const productLink = `https://sherow1982.github.io/matjar-oman/product-detail.html?name=${encodeURIComponent(product.العنوان)}`;
      const price = `${String(product['ﺎﻠﺴﻋﺭ ﺎﻠﻤﺨﻔَّﺿ']).replace(/[^0-9.]/g, '')} OMR`;

      xmlItems += `
    <item>
      <g:id>${productId}</g:id>
      <title><![CDATA[${product.العنوان}]]></title>
      <description><![CDATA[${product.الوصف}]]></description>
      <link>${productLink}</link>
      <g:image_link>${product['رابط الصورة']}</g:image_link>
      <g:availability>in_stock</g:availability>
      <g:price>${price}</g:price>
      <g:brand><![CDATA[متجر عمان]]></g:brand>
      <g:condition>new</g:condition>
    </item>`;
    });

    const fullFeed = `<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">
<channel>
  <title>متجر عمان</title>
  <link>https://sherow1982.github.io/matjar-oman/</link>
  <description>قائمة منتجات متجر عمان</description>${xmlItems}
</channel>
</rss>`;

    await fs.writeFile('google-feed.xml', fullFeed);
    console.log('Google Merchant feed file generated successfully.');

  } catch (error) {
    console.error('Error generating feed:', error);
    process.exit(1); // إنهاء العملية مع رمز خطأ
  }
}

generateFeed();

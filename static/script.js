document.addEventListener('DOMContentLoaded', function () {
    console.log("Script loaded");

    const qtyInput = document.getElementById('qty');
    const priceInput = document.getElementById('price');
    const totalDisplay = document.getElementById('total');

    function updateTotal() {
        const qty = parseFloat(qtyInput.value) || 0;
        const price = parseFloat(priceInput.value) || 0;
        const total = qty * price;
        totalDisplay.textContent = total.toFixed(2);
    }

    qtyInput.addEventListener('input', updateTotal);
    priceInput.addEventListener('input', updateTotal);

    updateTotal();
    
});

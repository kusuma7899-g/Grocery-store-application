// ================= GLOBAL =================
let productPrices = {};
let productOptions = "";

// ================= PAGE LOAD =================
$(document).ready(function () {

    // Load products with token
    $.ajax({
        method: "GET",
        url: productListApiUrl,
        headers: authHeaders(),
        success: function (products) {
            let options = '<option value="">-- Select Product --</option>';

            products.forEach(p => {
                options += `<option value="${p.product_id}">${p.product_name}</option>`;
                productPrices[p.product_id] = p.price_per_unit;
            });

            productOptions = options;

            // add first row
            addRow();
        },
        error: function (xhr) {
            if (xhr.status === 401) {
                alert("Session expired! Please login again.");
                window.location.href = "login.html";
            }
        }
    });

    $("#addMoreButton").click(addRow);

    $(document).on("click", ".remove-row", function () {
        $(this).closest(".product-item").remove();
        calculateTotal();
    });

    $(document).on("change", ".cart-product", function () {
        const productId = $(this).val();
        const price = productPrices[productId] || 0;

        $(this).closest(".product-item")
            .find(".product-price")
            .val(price);

        calculateTotal();
    });

    $(document).on("input", ".product-qty", calculateTotal);

    $("#saveOrder").click(saveOrder);
});

// ================= FUNCTIONS =================

function addRow() {
    const row = $("#productTemplate").html();
    $("#itemsInOrder").append(row);
    $("#itemsInOrder .cart-product:last").html(productOptions);
}

function calculateTotal() {
    let grandTotal = 0;

    $(".product-item").each(function () {
        const price = parseFloat($(this).find(".product-price").val()) || 0;
        const qty   = parseInt($(this).find(".product-qty").val()) || 0;
        const total = price * qty;

        $(this).find(".product-total").val(total.toFixed(2));
        grandTotal += total;
    });

    $("#product_grand_total").val(grandTotal.toFixed(2));
}

function saveOrder() {

    const payload = {
        customer_name: $("#customerName").val().trim(),
        grand_total: parseFloat($("#product_grand_total").val()) || 0,
        order_details: []
    };

    // Only validate rows where product is selected
    $(".product-item").each(function () {

        const productId = $(this).find(".cart-product").val();
        const qty       = parseInt($(this).find(".product-qty").val());
        const total     = parseFloat($(this).find(".product-total").val());

        // ignore empty rows
        if (!productId) return;

        // product selected but qty missing
        if (isNaN(qty) || qty <= 0) {
            alert("⚠️ Quantity required for selected product");
            throw "stop";
        }

        payload.order_details.push({
            product_id: parseInt(productId),
            quantity: qty,
            total_price: total
        });
    });

    if (payload.order_details.length === 0) {
        alert("⚠️ Please add at least one product");
        return;
    }

    $.ajax({
        url: orderSaveApiUrl,
        method: "POST",
        headers: authHeaders(),
        data: JSON.stringify(payload),
        contentType: "application/json",
        success: function () {
            alert("✅ Order saved successfully");
            window.location.href = "index.html";
        },
        error: function (xhr) {
            if (xhr.status === 401) {
                alert("Session expired! Please login again.");
                window.location.href = "login.html";
            } else {
                console.error(xhr.responseText);
                alert("❌ Failed to save order");
            }
        }
    });
}
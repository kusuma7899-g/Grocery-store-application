var productModal = $("#productModal");

function loadProducts() {
    $.get(productListApiUrl, function (response) {
        let rows = "";

        response.forEach(function (product) {
            rows += `
                <tr data-id="${product.product_id}">
                    <td>${product.product_name}</td>

                    <td>${product.uom_name}</td>
                    <td>${product.price_per_unit}</td>
                    <td>
                        <button class="btn btn-danger btn-sm delete-product">
                            Delete
                        </button>
                    </td>
                </tr>
            `;
        });

        $("#productsTableBody").html(rows);
    });
}

$(document).ready(function () {

    // Load products on page load
    loadProducts();

    // Load UOMs when modal opens
    productModal.on("show.bs.modal", function () {
        $.get(uomListApiUrl, function (response) {
            let options = `<option value="">-- Select --</option>`;
            response.forEach(function (uom) {
                options += `
                    <option value="${uom.uom_id}">
                        ${uom.uom_name}
                    </option>
                `;
            });
            $("#uoms").html(options);
        });
    });

    // Reset modal on close
    productModal.on("hidden.bs.modal", function () {
        $("#productForm")[0].reset();
        $("#id").val(0);
    });

    // Save Product
    $("#saveProduct").on("click", function () {

        let payload = {
            product_name: $("#name").val(),
            uom_id: $("#uoms").val(),
            price_per_unit: $("#price").val()
        };

        if (!payload.product_name || !payload.uom_id || !payload.price_per_unit) {
            alert("Please fill all fields");
            return;
        }

        let formData = new FormData();
        formData.append("data", JSON.stringify(payload));

        $.ajax({
            method: "POST",
            url: productSaveApiUrl,
            data: formData,
            processData: false,
            contentType: false,
            success: function () {
                productModal.modal("hide");
                loadProducts();
            }
        });
    });

    // Delete Product
    $(document).on("click", ".delete-product", function () {
        let productId = $(this).closest("tr").data("id");

        if (!confirm("Are you sure you want to delete this product?")) {
            return;
        }

        let formData = new FormData();
        formData.append("product_id", productId);

        $.ajax({
            method: "POST",
            url: productDeleteApiUrl,
            data: formData,
            processData: false,
            contentType: false,
            success: loadProducts
        });
    });

});

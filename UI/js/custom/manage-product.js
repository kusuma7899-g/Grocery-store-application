var productModal = $("#productModal");

function loadProducts() {
    $.ajax({
        method: "GET",
        url: productListApiUrl,
        headers: authHeaders(),
        success: function (response) {
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
        },
        error: function (xhr) {
            if (xhr.status === 401) {
                alert("Session expired! Please login again.");
                window.location.href = "login.html";
            }
        }
    });
}

$(document).ready(function () {

    // Load products on page load
    loadProducts();

    // Load UOMs when modal opens
    productModal.on("show.bs.modal", function () {
        $.ajax({
            method: "GET",
            url: uomListApiUrl,
            headers: authHeaders(),
            success: function (response) {
                let options = `<option value="">-- Select --</option>`;
                response.forEach(function (uom) {
                    options += `
                        <option value="${uom.uom_id}">
                            ${uom.uom_name}
                        </option>
                    `;
                });
                $("#uoms").html(options);
            },
            error: function (xhr) {
                if (xhr.status === 401) {
                    alert("Session expired! Please login again.");
                    window.location.href = "login.html";
                }
            }
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

        $.ajax({
            method: "POST",
            url: productSaveApiUrl,
            headers: authHeaders(),
            data: JSON.stringify(payload),
            contentType: "application/json",
            success: function () {
                productModal.modal("hide");
                loadProducts();
            },
            error: function (xhr) {
                if (xhr.status === 401) {
                    alert("Session expired! Please login again.");
                    window.location.href = "login.html";
                } else {
                    alert("Error saving product!");
                }
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
            headers: authHeaders(),
            data: formData,
            processData: false,
            contentType: false,
            success: loadProducts,
            error: function (xhr) {
                if (xhr.status === 401) {
                    alert("Session expired! Please login again.");
                    window.location.href = "login.html";
                } else {
                    alert("Error deleting product!");
                }
            }
        });
    });

});
// ================= API URLs =================
var productListApiUrl   = "http://127.0.0.1:8000/getProducts";
var uomListApiUrl       = "http://127.0.0.1:8000/getUOM";
var productSaveApiUrl   = "http://127.0.0.1:8000/insertProduct";
var productDeleteApiUrl = "http://127.0.0.1:8000/deleteProduct";
var orderSaveApiUrl     = "http://127.0.0.1:8000/insertOrder";
var orderListApiUrl     = "http://127.0.0.1:8000/getAllOrders";

// ================= COMMON AJAX =================
function callApi(method, url, data, isFormData, successCb) {
    $.ajax({
        method: method,
        url: url,
        data: data,
        processData: !isFormData,
        contentType: isFormData ? false : "application/json",
        success: function (response) {
            if (successCb) successCb(response);
        },
        error: function (xhr) {
            console.error(xhr.responseText);
            alert("API Error");
        }
    });
}


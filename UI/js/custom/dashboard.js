// ── Redirect to login if no token ──
if (!localStorage.getItem("access_token")) {
    window.location.href = "login.html";
}

// ── Load all orders into the table ──
function loadOrders() {
    $.ajax({
        method: "GET",
        url: orderListApiUrl,
        headers: authHeaders(),
        success: function (data) {
            const tableBody = document.getElementById("ordersTableBody");

            if (!tableBody) {
                console.error("ordersTableBody not found in HTML");
                return;
            }

            tableBody.innerHTML = "";

            if (data.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4" class="text-center text-muted">No orders found</td>
                    </tr>
                `;
                return;
            }

            data.forEach(function (order) {
                const row = `
                    <tr>
                        <td>${order.date ? order.date.split("T")[0] : ""}</td>
                        <td>#${order.order_id}</td>
                        <td>${order.customer_name || ""}</td>
                        <td>₹ ${parseFloat(order.total_cost ?? 0).toFixed(2)}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        },
        error: function (xhr) {
            if (xhr.status === 401) {
                alert("Session expired! Please login again.");
                window.location.href = "login.html";
            } else {
                console.error("Error loading orders:", xhr.responseText);
            }
        }
    });
}

// ── Run on page load ──
$(document).ready(function () {
    loadOrders();
});
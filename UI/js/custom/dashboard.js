function loadOrders() {
    fetch("http://127.0.0.1:8000/getAllOrders")
        .then(response => response.json())
        .then(data => {

            const tableBody = document.getElementById("ordersTableBody");

            if (!tableBody) {
                console.error("ordersTableBody not found in HTML");
                return;
            }

            tableBody.innerHTML = "";

            data.forEach(order => {
                const row = `
                    <tr>
                        <td>${order.date ? order.date.split("T")[0] : ""}</td>
                        <td>${order.order_id}</td>
                        <td>${order.customer_name || ""}</td>
                        <td>${order.total_cost ?? 0}</td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        })
        .catch(err => console.error("Error loading orders:", err));
}

document.addEventListener("DOMContentLoaded", loadOrders);

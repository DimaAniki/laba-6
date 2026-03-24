const orderItems = document.getElementById("order-items");
let cart = JSON.parse(localStorage.getItem("cart")) || [];

function renderOrderItems() {
    if (cart.length === 0) {
        orderItems.innerHTML = "<p>Корзина пуста</p>";
        return;
    }

    orderItems.innerHTML = "";

    cart.forEach(book => {
        const div = document.createElement("div");
        div.className = "card";

        div.innerHTML = `
            <img src="${book.image}" alt="${book.title}" class="book-cover">
            <h4>${book.title}</h4>
            <p>${book.author}</p>
        `;

        orderItems.appendChild(div);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    renderOrderItems();

    const form = document.getElementById("checkout-form");
    const successMessage = document.getElementById("success-message");

    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            const name = document.getElementById("name").value;
            const email = document.getElementById("email").value;
            const phone = document.getElementById("phone").value;
            const address = document.getElementById("address").value;

            console.log("Заказ:", { name, email, phone, address, books: cart });

            successMessage.style.display = "block";
            form.reset();
        });
    }
});
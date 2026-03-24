const cartItems = document.getElementById("cart-items");
const emptyText = document.getElementById("empty-cart");

let cart = JSON.parse(localStorage.getItem("cart")) || [];

function renderCart() {
    cartItems.innerHTML = "";
    emptyText.textContent = "";

    if (cart.length === 0) {
        emptyText.textContent = "Корзина пуста";
        return;
    }

    cart.forEach(book => {
        const div = document.createElement("div");
        div.className = "card";

        div.innerHTML = `
            <img src="${book.image}" alt="${book.title}" class="book-cover">
            <h4>${book.title}</h4>
            <p>${book.author}</p>
        `;

        const button = document.createElement("button");
        button.textContent = "Удалить";
        button.addEventListener("click", () => removeFromCart(book.id));

        div.appendChild(button);
        cartItems.appendChild(div);
    });
}

function removeFromCart(id) {
    cart = cart.filter(book => book.id !== id);
    localStorage.setItem("cart", JSON.stringify(cart));
    renderCart();
}

function clearCart() {
    localStorage.removeItem("cart");
    cart = [];
    renderCart();
}

document.addEventListener("DOMContentLoaded", () => {
    renderCart();
});
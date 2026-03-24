let cart = JSON.parse(localStorage.getItem("cart")) || [];

const bookList = document.getElementById("book-list");
const genreFilter = document.getElementById("genreFilter");
const searchInput = document.getElementById("searchInput");
const cartCount = document.getElementById("cart-count");

const books = [
    {
        id: 1,
        title: "Война и мир",
        author: "Л. Толстой",
        genre: "classic",
        image: "images/war-and-peace.jpg"
    },
    {
        id: 2,
        title: "1984",
        author: "Дж. Оруэлл",
        genre: "dystopia",
        image: "images/1984.jpg"
    },
    {
        id: 3,
        title: "Гарри Поттер",
        author: "Дж. Роулинг",
        genre: "fantasy",
        image: "images/HarryPoter.jpg"
    },
    {
        id: 4,
        title: "Мастер и Маргарита",
        author: "М. Булгаков",
        genre: "classic",
        image: "images/mastermargar.jpg"
    },
    {
        id: 5,
        title: "WoW Artas",
        author: "Голден Кристофер",
        genre: "fantasy",
        image: "images/artas.jpg"
    },
    {
        id: 6,
        title: "МЫ",
        author: "Замятин Евгений",
        genre: "dystopia",
        image: "images/me.jpg"
    }
];

function renderBooks() {
    const searchTerm = searchInput?.value.toLowerCase().trim() || "";
    const selectedGenre = genreFilter?.value || "all";

    bookList.innerHTML = "";

    const filteredBooks = books.filter(book => {
        const matchesGenre = selectedGenre === "all" || book.genre === selectedGenre;
        const matchesSearch = 
            book.title.toLowerCase().includes(searchTerm) ||
            book.author.toLowerCase().includes(searchTerm);
        return matchesGenre && matchesSearch;
    });

    if (filteredBooks.length === 0) {
        bookList.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: #777;">Книги не найдены</p>`;
        return;
    }

    filteredBooks.forEach(book => {
        const div = document.createElement("div");
        div.className = "card";

        div.innerHTML = `
            <img src="${book.image}" alt="${book.title}" class="book-cover">
            <h4>${book.title}</h4>
            <p>${book.author}</p>
        `;

        const button = document.createElement("button");
        button.textContent = "Корзина";
        button.addEventListener("click", () => addToCart(book.id));

        div.appendChild(button);
        bookList.appendChild(div);
    });
}

function addToCart(id) {
    const book = books.find(b => b.id === id);
    if (!book) return;

    cart.push(book);
    localStorage.setItem("cart", JSON.stringify(cart));
    updateCartCount();
}

function updateCartCount() {
    if (cartCount) {
        cartCount.textContent = cart.length;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    updateCartCount();

    if (genreFilter) {
        genreFilter.addEventListener("change", renderBooks);
    }

    if (searchInput) {
        searchInput.addEventListener("input", renderBooks);
    }

    renderBooks();
});
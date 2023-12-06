document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const addBookForm = document.getElementById('add-book-form');
    const addBooksForm = document.getElementById('add-books-form');
    const noteList = document.getElementById('book-list');
    const pageInfoContainer = document.getElementById('page-info-container');
    const userInfo = document.getElementById('user-info');
    let currentPage = 1;
    let allPages = 1;

    registerForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const username = document.getElementById('register-username').value;
        const password = document.getElementById('register-password').value;

        fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                location.reload();
            })
            .catch(error => console.error('Error:', error));
    });

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                localStorage.setItem('access_token', data.access_token);
                location.reload();
            })
            .catch(error => console.error('Error:', error));
    });

    addBookForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const title = document.getElementById('book_title').value;
        const author = document.getElementById('author').value;
        const token = localStorage.getItem('access_token');

        fetch('http://localhost:5000/books', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({ title, author }),
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                location.reload();
            })
            .catch(error => console.error('Error:', error));
    });

    function getBooks(page) {
        const token = localStorage.getItem('access_token');
    
        fetch(`http://localhost:5000/books?page=${page}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                displayBooks(data.books, data.current_page, data.total_pages);
                allPages = data.total_pages;
                currentPage = data.current_page;
            })
            .catch(error => {
                userInfo.innerHtml = '';
                const userI = document.createElement('h2');
                userI.textContent = "Unautorized";
                userInfo.appendChild(userI);
                console.error('Error:', error);
            });
    }   
    
    function deleteBook(bookId) {
        const token = localStorage.getItem('access_token');
    
        fetch(`http://localhost:5000/books/${bookId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                location.reload();
            })
            .catch(error => console.error('Error:', error));
    }

    function displayBooks(books, currentPage, totalPages) {
        noteList.innerHTML = '';
        pageInfoContainer.innerHTML = '';
    
        books.forEach(book => {
            const listItem = document.createElement('li');
            listItem.textContent = `${book.title} by ${book.author}`;
            
            // Add a delete button for each book
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', () => deleteBook(book.id));
    
            listItem.appendChild(deleteButton);
            noteList.appendChild(listItem);
        });
    
        // Display current page and total pages
        const pageInfo = document.createElement('p');
        pageInfo.textContent = `${currentPage} of ${totalPages}`;
        pageInfoContainer.appendChild(pageInfo);
    }

    function loadNextPage() {
        if (currentPage < allPages){
            getBooks(currentPage + 1);
        }
    }

    function loadPreviousPage() {
        if (currentPage > 1) {
            getBooks(currentPage - 1);
        }
    }

    // Load books when the page loads
    getBooks(currentPage);

    function logout() {
        localStorage.removeItem('access_token');
        location.reload();
    }
    
    document.getElementById('next-page-btn').addEventListener('click', loadNextPage);
    document.getElementById('prev-page-btn').addEventListener('click', loadPreviousPage);
    document.getElementById('logout-btn').addEventListener('click', logout);
});

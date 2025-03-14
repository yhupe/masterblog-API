// Function that runs once the window is fully loaded
window.onload = function() {
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
}

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    fetch(baseUrl + '/posts')
        .then(response => response.json())
        .then(data => {
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `
                    <h2>${post.title}</h2>
                    <p>${post.content}</p>
                    <p><strong>Author:</strong> ${post.author || 'Unknown'}</p>
                    <p><strong>Date:</strong> ${post.date || 'No date'}</p>
                    <button onclick="deletePost(${post.id})">Delete</button>
                    <button onclick="showUpdateForm(${post.id}, '${post.title}', '${post.content}', '${post.author}', '${post.date}')">Edit</button>
                `;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Function to send a POST request to the API to add a new post
function addPost() {
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value;

    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: postTitle,
            content: postContent,
            author: postAuthor,
            date: new Date().toISOString().split('T')[0]
        })
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post added:', post);
        loadPosts();
    })
    .catch(error => console.error('Error:', error));
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    fetch(baseUrl + '/posts/' + postId, { method: 'DELETE' })
        .then(response => {
            console.log('Post deleted:', postId);
            loadPosts();
        })
        .catch(error => console.error('Error:', error));
}

// Function to update a post
function updatePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;
    var updatedTitle = document.getElementById('update-title').value;
    var updatedContent = document.getElementById('update-content').value;
    var updatedAuthor = document.getElementById('update-author').value;
    var updatedDate = document.getElementById('update-date').value;

    fetch(baseUrl + '/posts/' + postId, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: updatedTitle,
            content: updatedContent,
            author: updatedAuthor,
            date: updatedDate
        })
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post updated:', post);
        loadPosts();
        document.getElementById('update-form').style.display = 'none';
    })
    .catch(error => console.error('Error:', error));
}

// Function to show update form with existing values
function showUpdateForm(postId, title, content, author, date) {
    document.getElementById('update-form').style.display = 'block';
    document.getElementById('update-id').value = postId;
    document.getElementById('update-title').value = title;
    document.getElementById('update-content').value = content;
    document.getElementById('update-author').value = author;
    document.getElementById('update-date').value = date;
}

// Function to search posts by title or content
function searchPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    var searchTitle = document.getElementById('search-title').value;
    var searchContent = document.getElementById('search-content').value;

    var url = baseUrl + '/posts/search?';
    if (searchTitle) url += `title=${searchTitle}&`;
    if (searchContent) url += `content=${searchContent}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';

            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `
                    <h2>${post.title}</h2>
                    <p>${post.content}</p>
                    <p><strong>Author:</strong> ${post.author || 'Unknown'}</p>
                    <p><strong>Date:</strong> ${post.date || 'No date'}</p>
                    <button onclick="deletePost(${post.id})">Delete</button>
                    <button onclick="showUpdateForm(${post.id}, '${post.title}', '${post.content}', '${post.author}', '${post.date}')">Edit</button>
                `;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Error:', error));
}

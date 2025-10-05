console.log("✅ JS loaded");

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const displayNameInput = document.getElementById('display-name-input');
    const joinForumBtn = document.getElementById('join-forum-btn');
    const authModal = document.getElementById('auth-modal');
    const mainContent = document.getElementById('main-content');
    const userInfo = document.getElementById('user-info');

    const postsContainer = document.getElementById('posts-container');

    const createPostBtn = document.getElementById('create-post-btn');
    const cancelPostBtn = document.getElementById('cancel-post-btn');
    const createPostForm = document.getElementById('create-post-form');
    const postTitleInput = document.getElementById('post-title');
    const postContentInput = document.getElementById('post-content');
    const postLinkInput = document.getElementById('post-link');

    // State
    let displayName = '';

    // Join forum handler
    joinForumBtn.addEventListener('click', () => {
        const name = displayNameInput.value.trim();

        if (!name) {
            alert('Please enter a display name.');
            return;
        }

        displayName = name;

        // Hide auth modal, show main content
        authModal.classList.add('hidden');
        mainContent.classList.remove('hidden');

        if (userInfo) {
            userInfo.textContent = `Logged in as: ${displayName}`;
        }

        fetchPosts();
    });

    // Show Create Post Form
    createPostBtn.addEventListener('click', () => {
        createPostForm.classList.remove('hidden');
        createPostBtn.classList.add('hidden');
    });

    // Cancel Post Form
    cancelPostBtn.addEventListener('click', () => {
        createPostForm.classList.add('hidden');
        createPostBtn.classList.remove('hidden');
        createPostForm.reset();
    });

    // Fetch posts from API and render
    async function fetchPosts() {
        postsContainer.innerHTML = '<p>Loading posts...</p>';

        try {
            const res = await fetch('/api/listings');
            if (!res.ok) throw new Error('Failed to fetch posts');

            const posts = await res.json();

            if (posts.length === 0) {
                postsContainer.innerHTML = '<p>No posts yet. Be the first!</p>';
                return;
            }

            postsContainer.innerHTML = '';
            posts.forEach(post => {
                const postEl = document.createElement('div');
                postEl.className = 'post-card bg-white p-6 rounded-lg forum-card';
                postEl.innerHTML = `
          <h2 class="text-xl font-bold">${escapeHTML(post.name)}</h2>
          <p>${escapeHTML(post.description)}</p>
          ${post.link ? `<a href="${escapeHTML(post.link)}" target="_blank" class="text-blue-600 underline block mt-2">View Listing</a>` : ''}
          <p class="text-sm text-gray-600 mt-2">Posted by <strong>${escapeHTML(post.seller)}</strong></p>
        `;
                postsContainer.appendChild(postEl);
            });
        } catch (err) {
            console.error(err);
            postsContainer.innerHTML = '<p class="text-red-500">Error loading posts.</p>';
        }
    }

    // Escape HTML helper
    function escapeHTML(str) {
        return str.replace(/[&<>"']/g, (m) => {
            switch (m) {
                case '&': return '&amp;';
                case '<': return '&lt;';
                case '>': return '&gt;';
                case '"': return '&quot;';
                case "'": return '&#39;';
                default: return m;
            }
        });
    }

    // Handle post creation
    createPostForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = postTitleInput.value.trim();
        const description = postContentInput.value.trim();
        const link = postLinkInput.value.trim();
        const seller = displayName || 'Anonymous';

        if (!name || !description) {
            alert('Please fill out both title and description.');
            return;
        }

        try {
            const res = await fetch('/api/create_listing', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, description, link, seller }),
            });

            if (!res.ok) throw new Error('Failed to create post');

            const result = await res.json();

            if (result.success) {
                alert('Post created successfully!');
                createPostForm.reset();
                createPostForm.classList.add('hidden');
                createPostBtn.classList.remove('hidden');
                fetchPosts();
            } else {
                alert(result.error || 'Failed to create post.');
            }
        } catch (err) {
            console.error(err);
            alert('Error creating post. Please try again.');
        }
    });

    // Auto-load posts if already joined
    if (!authModal.classList.contains('hidden')) {
        // Waiting for user to join
    } else {
        fetchPosts();
    }
});
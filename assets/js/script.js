// Global data store
let profileData = null;
let publicationsData = null;
let blogData = null;

function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark-mode');
  localStorage.setItem('dark-mode', body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
}

function loadComponent(id, url, callback) {
  const container = document.getElementById(id);
  if (container) {
    fetch(url)
      .then(response => response.text())
      .then(html => {
        container.innerHTML = html;
        if (callback) callback();
      })
      .catch(error => console.error(`Error loading component ${url}:`, error));
  }
}

function loadProfileData() {
  return fetch('data/profile.json')
    .then(response => response.json())
    .then(data => {
      profileData = data;
      return data;
    })
    .catch(error => {
      console.error('Error loading profile data:', error);
      return null;
    });
}

function loadPublicationsData() {
  return fetch('data/publications.json')
    .then(response => response.json())
    .then(data => {
      publicationsData = data;
      return data;
    })
    .catch(error => {
      console.error('Error loading publications data:', error);
      return null;
    });
}

function loadBlogData() {
  return fetch('data/blog.json')
    .then(response => response.json())
    .then(data => {
      blogData = data;
      return data;
    })
    .catch(error => {
      console.error('Error loading blog data:', error);
      return null;
    });
}

function updateProfileElements() {
  if (!profileData) return;
  
  const nameElement = document.getElementById('profile-name');
  if (nameElement) {
    nameElement.textContent = profileData.personal.name;
  }
  
  const contactElement = document.getElementById('profile-contact');
  if (contactElement) {
    contactElement.innerHTML = `${profileData.personal.email}<br>${profileData.personal.location}`;
  }
  
  const profileImage = document.getElementById('profile-image');
  if (profileImage) {
    profileImage.src = profileData.personal.profileImage;
    profileImage.alt = `${profileData.personal.name} Profile Picture`;
  }
  
  const aboutText = document.getElementById('about-text');
  if (aboutText) {
    const interests = profileData.personal.researchInterests
      .map(interest => `<span class="highlight-text">${interest}</span>`)
      .join(', ');
    
    aboutText.innerHTML = `
      Hi there! Welcome to ${profileData.personal.name.split(' ')[0]}'s homepage.<br><br>
      I am a ${profileData.personal.title} in the ${profileData.personal.department} at Texas A&M University, advised by ${profileData.personal.advisor}. I began my doctoral studies in ${profileData.personal.startDate}.<br><br>
      My research interests are focused on ${interests},
      and their intersections.<br><br>
      I serve as a reviewer for ${profileData.personal.reviewer}.<br>
    `;
  }

  // Update education list
  const educationList = document.getElementById('education-list');
  if (educationList && profileData.education) {
    educationList.innerHTML = profileData.education.map(edu => `
      <div class="box11">
        <div class="bio">
          ${edu.degree}
        </div>
        <div class="bio1">
          ${edu.institution}, ${edu.location}<br>
          ${edu.period}
        </div>
      </div>
    `).join('');
  }
}

function updatePublications() {
  const publicationsList = document.getElementById('publications-list');
  if (publicationsList && publicationsData) {
    publicationsList.innerHTML = publicationsData.publications.map(pub => `
      <a href="${pub.url}" style="text-decoration: none;">
        <div class="box11">
          <div class="bio">
            ${pub.title}
          </div>
          <div class="bio1">
            ${pub.authors}<br>
            <i>${pub.venue}</i>
          </div>
        </div>
      </a>
    `).join('');
  }
}

function updateBlogPosts() {
  const blogPostsList = document.getElementById('blog-posts-list');
  if (blogPostsList && blogData) {
    blogPostsList.innerHTML = blogData.blogPosts.map(post => `
      <a href="${post.url}" style="text-decoration: none;">
        <div class="box11">
          <div class="bio">
            ${post.title}
          </div>
        </div>
      </a>
    `).join('');
  }
}

window.addEventListener('DOMContentLoaded', () => {
  if (localStorage.getItem('dark-mode') === 'enabled') {
    document.body.classList.add('dark-mode');
  }

  // Load all data first, then load components
  Promise.all([loadProfileData(), loadPublicationsData(), loadBlogData()]).then(() => {
    // Load navigation
    loadComponent('nav-container', 'includes/nav.html', () => {
      const currentPage = window.location.pathname.split('/').pop() || 'index.html';
      document.querySelectorAll('#nav-container nav button[data-link]').forEach(btn => {
        const link = btn.getAttribute('data-link');
        btn.addEventListener('click', () => { window.location.href = link; });
        if (link === currentPage) {
          btn.classList.add('active');
        }
      });
      const toggleButton = document.getElementById('dark-mode-toggle');
      if (toggleButton) {
        toggleButton.addEventListener('click', toggleDarkMode);
      }
    });

    // Load footer
    loadComponent('footer-container', 'includes/footer.html', () => {
      const year = document.getElementById('copyright-year');
      if (year) {
        year.textContent = new Date().getFullYear();
      }
      const lastUpdate = document.getElementById('last-update');
      if (lastUpdate) {
        if (profileData && profileData.lastUpdated) {
          const date = new Date(profileData.lastUpdated);
          lastUpdate.textContent = date.toLocaleString('default', { month: 'long', year: 'numeric' });
        } else {
          const date = new Date(document.lastModified);
          lastUpdate.textContent = date.toLocaleString('default', { month: 'long', year: 'numeric' });
        }
      }
    });

    // Load publications with dynamic content
    loadComponent('publications-container', 'includes/publications.html', updatePublications);
    
    // Load blog posts with dynamic content
    loadComponent('blog-posts-container', 'includes/blog-posts.html', updateBlogPosts);
    
    // Load profile header (for home page)
    loadComponent('profile-header-container', 'includes/profile-header.html', updateProfileElements);
    
    // Load about summary (for home page)
    loadComponent('about-summary-container', 'includes/about-summary.html', updateProfileElements);
    
    // Load education (for about page)
    loadComponent('education-container', 'includes/education.html', updateProfileElements);
    
    // Load social links
    loadComponent('social-links-container', 'includes/social-links.html');
    
    // Update any profile elements that are already loaded
    updateProfileElements();
  });
});

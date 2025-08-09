# Modular Website Structure

This website has been refactored to use a modular architecture that separates content from presentation and makes updates easier.

## Structure

### Data Files (`data/`)
- `profile.json` - Personal information, education, and contact details
- `publications.json` - Research publications list
- `blog.json` - Blog posts and project updates

### Modular Components (`includes/`)
- `nav.html` - Navigation menu
- `footer.html` - Footer with copyright and last update
- `profile-header.html` - Profile information display
- `about-summary.html` - About me summary
- `education.html` - Education history
- `social-links.html` - Social media links
- `publications.html` - Publications list container
- `blog-posts.html` - Blog posts container

### Pages
- `index.html` - Home page (uses profile-header, about-summary, publications, social-links)
- `aboutMe.html` - About page (uses education component)
- `contact.html` - Contact page (uses social-links)
- `research.html` - Research page (uses publications)
- `blog.html` - Blog page (uses blog-posts)

### JavaScript (`script.js`)
- Loads all data files
- Renders components dynamically
- Updates content automatically
- Handles dark mode and navigation

## Benefits

1. **DRY (Don't Repeat Yourself)**: Common elements like navigation, footer, and social links are defined once
2. **Easy Updates**: Content can be updated by modifying JSON files without touching HTML
3. **Consistent Data**: Profile information is centralized and used across all pages
4. **Automatic Updates**: Copyright year and last modified dates update automatically
5. **Maintainable**: Clear separation between data, presentation, and behavior

## To Update Content

### Personal Information
Edit `data/profile.json`:
- Update email, location, research interests
- Modify education history
- Change social media links

### Publications
Edit `data/publications.json`:
- Add new publications
- Update existing entries
- Remove outdated items

### Blog Posts/Projects
Edit `data/blog.json`:
- Add news announcements
- Include new projects
- Update links and descriptions

### Navigation or Footer
Edit the respective files in `includes/` directory.

## Auto-Updating Features

- Copyright year updates automatically each year
- Last modified date updates based on profile data or file modification
- Profile information is consistent across all pages
- Research interests are automatically highlighted on the home page

This modular approach makes the website much easier to maintain while preserving the original design and functionality.

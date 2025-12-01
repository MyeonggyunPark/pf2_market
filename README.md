# Podo Market – Second-hand Marketplace with Django & TailwindCSS

A fully featured second-hand marketplace where users can buy, sell, and interact with items.
Built with **Django**, **Tailwind CSS**, **django-allauth**, and optimized with **AJAX** for a seamless user experience. Deployable via **Docker** (gunicorn + uv).

---

## 🌐 Features

### 🛍️ Marketplace Core

- **CRUD for Items:** Create, read, update, and delete listings with image uploads.
- **Advanced Search:** - Filter items by title or description using Django `Q` objects (OR logic).
  - **Client-side Validation:** JavaScript prevents empty search queries and displays styling errors (red border/message) instantly.
  - **Search Persistence:** Search terms are retained in the input field across pagination and results.
- **Sold Status:** Toggle items as SALE / SOLD; sold items are automatically hidden from the main feed but remain visible on user profiles.

### 💬 Interaction & Community (New!)

- **Comment System:** Users can leave comments on items.
  - **In-Place Editing:** Edit or delete comments directly on the detail page without reloading (JS-based toggle form).
- **Like System:** Users can like/unlike items and comments.
  - **AJAX-Powered:** Likes are processed asynchronously without page refreshes.
  - **Real-time UI Updates:** Heart icon state (filled/outline) and count numbers update instantly upon interaction.
  - **Generic Relation:** Scalable architecture using Django's `GenericForeignKey` to support likes on any content type.

### 👤 User & Profile

- **Custom User Model:** Extended with nickname, address, city, intro, and seller rating.
- **Profile Dashboard (Tabbed UI):** - Organized into three tabs: **[Listings]**, **[Liked Items]**, and **[Commented Items]**.
  - **AJAX-free Tab Switching:** Uses JavaScript to toggle visibility of content sections instantly without server requests.
  - **Deduplication:** "Commented Items" tab automatically removes duplicates if a user commented multiple times on the same post.
  - Public seller profiles display rating stars and location info.
- **Authentication:** - Email-based signup/login with `django-allauth`.
  - Social login support (Google, GitHub, Kakao, Naver).
  - **Profile Completion Gate:** Middleware redirects authenticated users with incomplete profiles to the setup page.

### 🎨 UI/UX

- **Responsive Design:** Fully responsive layout optimized for mobile and desktop using Tailwind CSS.
- **Modern UX:** - **Custom Modals:** Replaced browser default alerts with styled modals for delete confirmations.
  - **Form Validation:** Custom error styling matches the site theme, replacing default HTML5 popups.
  - **SVG Icons:** Consistent iconography for likes, comments, and navigation.

---

## 🛠️ Tech Stack

| Layer        | Tech                                                      |
|--------------|-----------------------------------------------------------|
| **Backend**  | Python, Django 5                                          |
| **Frontend** | HTML, Tailwind CSS, Vanilla JavaScript (AJAX/Fetch API)   |
| **Database** | SQLite (dev)                                              |
| **Auth**     | `django-allauth` (Email + Social), Custom Middleware      |
| **Media**    | `Pillow` for image processing                             |
| **DevOps**   | Docker, Gunicorn, `uv` (Package Manager), `python-dotenv` |

---

## 🐳 Run with Docker

> Dockerfile uses **uv** for fast dependency management and runs Django with **gunicorn**.

```bash
# Build image
docker build -t podo-market .

# Run container
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=127.0.0.1 \
  -e EMAIL_HOST_USER=your-gmail@gmail.com \
  -e EMAIL_HOST_PASSWORD=your-gmail-app-password \
  podo-market
```

---

## 📂 Routes Overview

| Route / Page                   | Description                                       |
|--------------------------------|---------------------------------------------------|
| `/`                            | Main market index (Search + Filtered Listings)    |
| `/login/`                      | Login page (Email + Social providers)             |
| `/signup/`                     | Signup page                                       |
| `/email-confirmation-required/`| Notice for unverified email accounts              |
| `/password/reset/`             | Password reset request page                       |
| `/password/change/`            | Change password (logged-in users)                 |
| `/item/create/`                | Create new item listing                           |
| `/item/<id>/`                  | Item detail page (with Comments & Likes)          |
| `/item/<id>/edit/`             | Edit listing (Author only)                        |
| `/item/<id>/delete/`           | Delete listing (Author only)                      |
| `/users/<id>/`                 | User profile page (Tabs: Listings, Likes, Comments)|
| `/user/<id>/items/`            | User-specific full item list                      |
| `/set-profile/`                | Initial profile setup (Required after signup)     |
| `/update-profile/`             | Edit profile details and avatar                   |
| `/comment/<id>/edit/`          | Comment edit endpoint (POST only)                 |
| `/comment/<id>/delete/`        | Comment delete endpoint (POST only)               |
| `/like/<type>/<id>/`           | Like toggle endpoint (AJAX/JSON)                  |

---

## ✨ Key Implementation Details

### 1. Generic Relations for Likes

The `Like` model uses `GenericForeignKey` to connect with both `PostItem` and `Comment` models efficiently. This allows the application to scale and support "likes" on any future content types (e.g., reviews, replies) without schema changes.

- **Data Integrity:** A `UniqueConstraint` ensures a user can only like a specific object once.

### 2. AJAX & In-Place Editing

Instead of traditional page reloads, the application uses JavaScript `fetch` API and DOM manipulation to:

- Toggle like status and update counts instantly.
- Swap comment view mode with an edit form dynamically.
- Provide a smooth, app-like experience ("SPA-feel") within a Django Template ("MPA") architecture.

### 3. Search Logic & Validation

- **Backend:** Uses `Q` objects to perform OR lookups across multiple fields (`item_title`, `item_detail`).
- **Frontend:** JavaScript intercepts form submission to prevent empty queries and applies custom CSS classes (`.error`) to highlight the input field.

### 4. Defensive Design

- **Views:** `CommentUpdateView` and `CommentDeleteView` block direct `GET` requests to prevent accidental access or abuse, redirecting users back to the item detail page.
- **Forms:** Custom validation removes HTML5 `required` attributes to allow server-side error messages to be styled consistently with the UI theme.

---

## 👨‍💻 Author

Built with ❤️ by **Myeonggyun Park** This project is a portfolio-ready Django application demonstrating full-stack capabilities, from database design to frontend interactivity.
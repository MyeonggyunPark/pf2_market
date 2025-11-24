# Podo Market – Second-hand Marketplace with Django & TailwindCSS

A simple second-hand marketplace where users can sign up, complete a profile and post items for sale.  
Built with **Django**, **Tailwind CSS**, **django-allauth**, and deployable via **Docker** (gunicorn + uv).

---

## 🌐 Features

- 👤 Email-based authentication with **custom User model**
- ✉️ Email verification required before posting items (signup & password reset flows)
- 🔑 Social login support (Google, GitHub, Kakao, Naver) via `django-allauth`
- 🧾 Profile setup & edit pages (nickname, city, address, intro, avatar, seller rating)
- 🛒 CRUD for marketplace items (create, detail, edit, delete)
- ✅ SALE / SOLD toggle and hiding sold items on the main index
- 🧑‍💼 Public seller profile with rating stars and user-specific item list
- 🎨 Tailwind-based responsive layout with custom buttons, inputs and cards
- 📧 Branded HTML emails using the Podo Market logo for:
  - signup confirmation  
  - general email confirmation  
  - password reset

---

## 🛠️ Tech Stack

| Layer        | Tech                                                      |
|-------------|-----------------------------------------------------------|
| Backend     | Python, Django 5                                          |
| Frontend    | HTML, Tailwind CSS, vanilla JS                            |
| Auth        | `django-allauth` (email + social providers)               |
| Forms/Utils | Custom validators, middleware, `django-braces`            |
| DB (dev)    | SQLite                                                    |
| Media       | `ImageField` uploads (Pillow), static default avatar      |
| Email       | Gmail SMTP, custom HTML templates                         |
| Packaging   | `uv` + `pyproject.toml`                                   |
| Deployment  | Docker, gunicorn, Railway-ready                           |

---

## 🐳 Run with Docker

> Dockerfile uses **uv** for dependency management and runs Django with **gunicorn**.

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
| `/`                            | Main market index (latest items, SOLD hidden)     |
| `/login/`                      | Login page (email + social login buttons)         |
| `/signup/`                     | Signup page                                       |
| `/email/confirm/`              | Email confirmation links (django-allauth)         |
| `/password/reset/`             | Request password reset email                      |
| `/password/change/`            | Change password (logged-in users)                 |
| `/item/<id>/`                  | Item detail page                                  |
| `/item/create/`                | Create new item                                   |
| `/item/<id>/edit/`             | Edit existing item                                |
| `/item/<id>/delete/`           | Delete item with confirmation                     |
| `/user/id//`                   | Current user profile page                         |
| `/user/<id>/items/`            | User-specific item list                           |
| `/set-profile/`                | Initial profile setup (required after signup)     |
| `/update-profile/`             | Edit profile info and avatar                      |

---

## ✨ Notable Features

### Custom User & Profile

- Nickname, address, city, intro and seller rating
- Static default profile image with template fallback

### Profile-required middleware

- Redirects authenticated users with incomplete profiles  
  to the profile setup page before they can use the site fully

### Sold item UX

- Sold flag across model, forms and templates
- Sold items hidden on the home page but still accessible via detail

### Email customization

- Subject lines and body text tailored for signup and password reset
- HTML templates with inline styles and Podo Market logo image

### Tailwind UI

- Entire index page refactored to Tailwind-based card layout
- Reusable button, input, notification and layout components

### Environment-based config

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, SMTP credentials and email logo URL  
  all loaded from environment variables via `python-dotenv`

---

## 📦 Deployment Notes

- Dependencies are managed via **uv**:
  - `pyproject.toml` and `uv.lock` are tracked for reproducible environments.

### Static files

- `STATIC_ROOT` is configured as `staticfiles/`
- Dockerfile runs:

```bash
python manage.py collectstatic --noinput
```

---

### Media & DB

- `media/` and `db.sqlite3` are ignored by Git and excluded from the Docker context.

### Email

Gmail account + app password required:

- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

Optional:

- `EMAIL_LOGO_URL` – allows using the deployed domain in email templates.

### Typical production command (inside Docker)

```dockerfile
CMD ["uv", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```
---

## 👨‍💻 Author

Built with ❤️ by **Myeonggyun Park**  
This project is part of a backend web development learning journey and serves as a portfolio-ready Django application.


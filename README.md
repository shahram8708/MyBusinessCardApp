# MyBusinessCardApp

MyBusinessCardApp is a Flask-based web application that allows users to create and manage digital business cards (vCards).
It provides user authentication, detailed business profile creation, image uploads, service listings, working hours management, gallery support, and sharable vCard preview with QR code generation.

---

## Overview

Users can register, log in, build a personalized digital business card, upload media, and preview their vCard.
The application stores data using SQLAlchemy and supports editing and updating of existing vCards.

---

## Key Features

* User registration and login with secure authentication
* Create and edit personal digital business cards
* Business information fields including:

  * Full name
  * Company name
  * Designation
  * Contact details
  * Business address
* Social media links support
* “About” section for business description
* Working hours for all days of the week
* Banner image upload
* Profile photo upload
* Service listing with title and description fields
* Image gallery upload
* vCard preview page
* QR code generation for sharing vCard links
* SQLite database integration

---

## Tech Stack

**Backend**

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Login
* Flask-WTF
* WTForms
* Flask-Bcrypt

**Utilities**

* Pillow
* qrcode

**Database**

* SQLite (default configuration)

**Frontend**

* HTML (Jinja2 templates)
* Static assets

---

## Project Structure

```
MyBusinessCardApp-main/
├── app.py                 # Main application
├── config.py              # App configuration
├── models.py              # Database models
├── forms.py               # WTForms definitions
├── requirements.txt       # Dependencies
│
├── instance/
│   └── MyBusinessCardApp.db   # SQLite database
│
├── static/
│   ├── images/
│   └── uploads/
│       └── uploads.txt
│
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── create_vcard.html
    ├── edit_vcard.html
    └── vcard_preview.html
```

---

## Installation

1. Extract the project.

2. Create and activate a virtual environment (recommended).

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Ensure the `instance` folder and database file exist (already included).
   SQLite is used by default via `config.py`.

5. Ensure upload directories exist:

```
static/uploads
```

---

## Configuration

Application configuration is set in `config.py`, including:

* Secret key
* SQLite database path
* SQLAlchemy settings

No additional configuration is required for basic usage.

---

## Running the Application

Run the application:

```
python app.py
```

Then open in your browser:

```
http://127.0.0.1:5000/
```

---

## Usage

* Register a new account
* Log in
* Create your vCard using the provided form
* Upload banner, profile photo, and gallery images if desired
* Add services and working hours
* Save and preview your digital business card
* Use the QR code on the preview page to share your vCard

---

## Notes

* Uploaded images are stored in `static/uploads`.
* Database uses SQLite by default and is stored in the `instance` directory.

---

## License

No license file is included in this repository.

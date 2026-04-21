# TicketApp

A small internal support ticket application built with Django.  
It allows users to create, assign, and track support tickets with priorities and statuses.

## Built With

- [Python 3.14](https://www.python.org/)
- [Django 6.0](https://www.djangoproject.com/)
- [Unfold](https://unfoldadmin.com/)
- SQLite

## Features

**Ticket Management**
- Create support tickets with a title, description, status, and priority level (High / Medium / Low)
- Track ticket lifecycle through three statuses: New, In Progress, Resolved
- Tickets are ordered by priority then creation date
- Requester is automatically set to the logged-in user on creation
- Able to assign to a user

**Bulk Actions**
- Bulk resolve selected tickets
- Bulk assign selected tickets to a user

**Ticket Notes**
- Add notes to tickets inline from the ticket detail page, or via a standalone notes changelist
- Notes track their author and both created/updated timestamps

**Search & Filtering**
- Search tickets by title, requester name, or requester email
- Filter tickets by status and priority
- Search notes by ticket title or author username
- Filter notes by author

## Prerequisites

- [Python 3.14+](https://www.python.org/downloads/) must be installed on your machine.

## Installation & Setup

> **macOS / Linux:** Before activating the virtual environment, use `python3`/`pip3` instead of `python`/`pip`

### 1. Clone the repository

```bash
git clone https://github.com/btruong178/TicketApp
cd TicketApp
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Load seed data

```bash
python manage.py loaddata seed.json
```

### 7. Run the development server

```bash
python manage.py runserver
```

## Accessing the Admin Panel

Navigate to: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Any of the seeded credentials below will work to log in.

## Seeded User Accounts

All users are configured as superusers and have full admin access.

| Username | Password |
|---|---|
| `alice.johnson` | `adminpassword` |
| `bob.smith` | `adminpassword` |
| `carol.nguyen` | `adminpassword` |
| `dev.support` | `adminpassword` |
| `admin` | `adminpassword` |


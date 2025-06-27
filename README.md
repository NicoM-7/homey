# Homey

A comprehensive roommate and home management application designed to streamline shared living experiences for both tenants and landlords.

## Features

### For Tenants & Roommates
- **Chore Management**: Assign, track, and complete household chores with due dates
- **Expense Tracking**: Split bills, track shared expenses, and manage payments between roommates  
- **Calendar Integration**: Shared calendar for household events and scheduling
- **Inventory Management**: Track shared household items and supplies
- **Messaging System**: Group chat and direct messaging with roommates
- **Property Search**: Browse and review rental properties
- **Review System**: Rate and review properties and landlords

### For Landlords
- **Property Management**: Add, edit, and manage rental properties with image galleries
- **Group Management**: Create and manage household groups with multiple tenants
- **Tenant Communication**: Direct messaging with tenants
- **Review Monitoring**: View tenant feedback and property reviews

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MySQL 8.0
- **Authentication**: JWT with bcrypt password hashing
- **Email**: SMTP integration for notifications
- **Security**: SSL/TLS encryption support

### Frontend  
- **Framework**: React Native with Expo
- **Navigation**: React Navigation v7
- **HTTP Client**: Axios
- **UI Components**: React Native Elements, Vector Icons

### Infrastructure
- **Containerization**: Docker
- **SSL/TLS**: OpenSSL certificate generation
- **Database**: MySQL with persistent volumes
- **Development**: Hot reload for both frontend and backend

## Prerequisites

- **Python**
- **pip**
- **Node.js**
- **npm**
- **Docker**
- **Git Bash** (for Windows users)

## Installation & Setup

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/NicoM-7/homey-flask-refactor.git
   cd homey
   ```

2. **Set up environment variables**

   You need to configure environment variables for both the frontend and backend:

   - **Frontend:**
     ```bash
     cp ./frontend/.env.development.dist ./frontend/.env.development
     ```
     Edit the `.env.development` file and provide the required values such as:
     - `EXPO_PUBLIC_BACKEND_URL`

   - **Backend:**
     ```bash
     cp ./backend/docker/.env.development.dist ./backend/docker/.env.development
     ```
     Edit the `.env.development` file and fill in values such as:
     - `MYSQL_ROOT_PASSWORD`
     - `MYSQL_USER`
     - `MYSQL_PASSWORD`
     - `MYSQL_DATABASE`
     - `JWT_SECRET`

   To generate secure random values for secrets like `JWT_SECRET` or database passwords, use:
   ```bash
   openssl rand -hex 32
   ```

   To find your local IPv4 address (for networking or DB access), use:
   - `ipconfig` (Windows)
   - `ifconfig` or `ip a` (Linux/macOS)

3. **Run the application**
   ```bash
   chmod +x ./run.sh
   ./run.sh
   ```
   This script will:
   - Check and install required dependencies (e.g., OpenSSL)
   - Generate SSL certificates for HTTPS
   - Install frontend dependencies
   - Start the Expo development server
   - Build and run the Docker containers for backend and database

4. **Access the application**
   - **Frontend**: Automatically served via Expo development tools
   - **Backend API**: `http://localhost:8080` or your configured port
   - **Database**: MySQL accessible at port `3306`

### Syncing the Database

Run the following script:

```bash
chmod +x ./syncModels.sh
./syncModels.sh
```

This will:

- Delete the current MySQL Docker volume (all data will be lost)
- Start the backend containers using Docker Compose
- Wait for MySQL to be fully ready
- Dump the schema (no data) into `./backend/docker/dumps/init.sql` using `mysqldump`
- Shut down and clean up all running containers

### Schema Validation with Perl

To ensure your models are properly defined, the script `summarizeSchema.pl` will:

- Scan all model files in `backend/models/` (excluding `__init__.py`)
- Extract the `__tablename__` for each SQLAlchemy model
- Verify each one exists in the generated `init.sql`

If a model is defined but missing from the SQL dump, the script will exit with an error and tell you which table is missing — helping catch issues early.

## Project Structure

```
homey/
├── backend/                     # Flask API server
│   ├── controllers/            # Business logic controllers
│   ├── models/                 # Database models (SQLAlchemy)
│   ├── routes/                 # API route definitions
│   ├── middleware/             # Authentication & logging middleware
│   ├── docker/                 # Docker configuration
│   │   ├── docker-compose.yml
│   │   ├── dockerfile
│   │   └── dumps/init.sql      # Database initialization
│   ├── main.py                 # Flask application entry point
│   ├── db.py                   # Database configuration
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # React Native Expo app
│   ├── app/                    # App screens and navigation
│   │   ├── components/         # Reusable UI components
│   │   ├── context/           # React context providers
│   │   ├── hooks/             # Custom React hooks
│   │   ├── redux/             # Redux store and slices
│   │   ├── stacks/            # Navigation stack definitions
│   │   └── theme/             # App styling and theme
│   ├── package.json           # Node.js dependencies
│   └── app.json              # Expo configuration
│
├── run.sh                     # Main setup and run script
├── syncModels.sh             # Database model synchronization
```

## About This Repository

This repository is a complete backend **refactor** of the original Homey capstone project.

The original backend was built using:
- Node.js
- Express
- Sequelize ORM
- PostgreSQL

To better align with job requirements and showcase my Python/Flask experience, the backend was rebuilt from scratch using:
- Python
- Flask
- SQLAlchemy ORM
- MySQL

All original features have been migrated, and testing/debugging is ongoing to ensure full functional parity. I refactored this to demonstrate my flexibility and my ability to adapt to different tech stacks.
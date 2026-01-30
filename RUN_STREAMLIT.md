# Running the Streamlit Application

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the application:**
   ```bash
   python -m streamlit run app.py
   ```

   Or use the batch file:
   ```bash
   run_streamlit.bat
   ```
   
   **Note:** If `streamlit` command is not recognized, always use `python -m streamlit` instead.

3. **The application will open in your browser automatically** at `http://localhost:8501`

## Prerequisites

- Python 3.8 or higher
- MySQL running in XAMPP (if using MySQL)
- Database `hospital_system` created
- Dependencies installed: `pip install -r requirements.txt`

## Features

The Streamlit application includes:

- ✅ **Patient Management** - Full CRUD operations
  - Add new patients
  - Edit existing patients
  - Delete patients
  - Search and filter
  - View statistics

- 🚧 **Queue Management** - Coming soon
- 🚧 **Doctor Management** - Coming soon
- 🚧 **Appointments** - Coming soon
- 🚧 **Reports & Analytics** - Coming soon

## Troubleshooting

### Database Connection Error

If you see a database connection error:

1. **Check XAMPP MySQL is running**
   - Open XAMPP Control Panel
   - Start MySQL service

2. **Verify database exists**
   - Open phpMyAdmin (http://localhost/phpmyadmin)
   - Check if `hospital_system` database exists

3. **Check credentials**
   - Edit `src/config.py`
   - Verify MySQL credentials match your XAMPP setup

### Port Already in Use

If port 8501 is already in use:

```bash
python -m streamlit run app.py --server.port 8502
```

### Module Not Found

If you get import errors:

1. Make sure you're in the project root directory
2. Install dependencies: `pip install -r requirements.txt`
3. Check that `src/` directory structure is correct

## Configuration

Edit `src/config.py` to switch between MySQL and SQLite:

```python
USE_MYSQL = True  # Set to False for SQLite
```

## Development

To run in development mode with auto-reload:

```bash
python -m streamlit run app.py --server.runOnSave true
```

This will automatically reload when you save changes.

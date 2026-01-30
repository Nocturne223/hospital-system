# Quick Test Guide - Hospital Management System

## 🚀 Quick Start Testing

### 1. Test Database Connection (30 seconds)

```bash
python test_mysql_connection.py
```

**Expected**: `[SUCCESS] MySQL connection test completed successfully!`

---

### 2. Test PatientService (1 minute)

```bash
python tests/test_patient_service.py
```

**Expected**: All tests pass with `[SUCCESS]` message

---

### 3. Interactive Testing (Recommended)

```bash
python interactive_test.py
```

**Features**:
- View all patients
- Search patients
- Create new patient
- Update patient
- Delete patient
- Filter by status
- View statistics

**Menu-driven interface** - Easy to use!

---

### 4. View Data in Database

#### Option A: phpMyAdmin
1. Open: http://localhost/phpmyadmin
2. Select: `hospital_system` database
3. Click: `patients` table
4. Browse: View all data

#### Option B: Navicat
1. Connect to MySQL
2. Open `hospital_system` database
3. Browse `patients` table

#### Option C: Command Line
```bash
python src/database/view_db.py --table patients
```

---

## 📋 Test Checklist

- [ ] Database connection works
- [ ] Can create patient
- [ ] Can retrieve patient
- [ ] Can update patient
- [ ] Can search patients
- [ ] Can filter patients
- [ ] Validation works
- [ ] Data persists in database

---

## 🎯 Quick Test Commands

```bash
# Test everything
python test_mysql_connection.py
python tests/test_patient_service.py

# Interactive testing
python interactive_test.py

# View database
python src/database/view_db.py --table patients

# Add more sample data
python src/database/add_sample_patients.py
```

---

## 💡 Testing Tips

1. **Start with interactive_test.py** - Easiest way to test
2. **Check database** - Verify data in phpMyAdmin/Navicat
3. **Run test suite** - Verify all automated tests pass
4. **Try edge cases** - Test with invalid data, empty fields, etc.

---

## 🐛 Troubleshooting

**Can't connect?**
- Check XAMPP MySQL is running
- Verify credentials in `src/config.py`

**Tests fail?**
- Check database has tables
- Run `test_mysql_connection.py` first

**Import errors?**
- Make sure you're in project root directory
- Check Python path includes `src/`

---

**Ready to test?** Run `python interactive_test.py` for the easiest testing experience!

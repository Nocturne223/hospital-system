# Hospital Management System - Code Documentation Standards

## Overview

This document defines the code documentation standards and conventions for the Hospital Management System project. All code should follow these standards for consistency and maintainability.

---

## Documentation Requirements

### 1. Module-Level Documentation

Every Python module should begin with a docstring describing its purpose.

```python
"""
Patient Service Module

This module provides business logic for patient management operations
including creation, retrieval, updating, and deletion of patient records.

Classes:
    PatientService: Main service class for patient operations
"""

# Module code here...
```

### 2. Class Documentation

Every class must have a comprehensive docstring.

```python
class PatientService:
    """
    Service class for patient management operations.
    
    This class encapsulates all business logic related to patient management,
    including validation, data processing, and database operations.
    
    Attributes:
        db_manager (DatabaseManager): Database manager instance
        
    Example:
        >>> service = PatientService(DatabaseManager())
        >>> patient_id = service.create_patient({'full_name': 'John Doe', ...})
    """
    
    def __init__(self, db_manager):
        """Initialize PatientService with database manager."""
        self.db_manager = db_manager
```

### 3. Method Documentation

All public methods must have docstrings following Google-style format.

```python
def create_patient(self, patient_data: dict) -> int:
    """
    Create a new patient record.
    
    This method validates patient data, applies business rules, and saves
    the patient to the database.
    
    Args:
        patient_data (dict): Dictionary containing patient information.
            Required keys:
                - full_name (str): Patient's full name
                - date_of_birth (str): Date of birth in YYYY-MM-DD format
            Optional keys:
                - gender (str): 'Male', 'Female', or 'Other'
                - phone_number (str): Contact phone number
                - email (str): Email address
                - status (int): Priority status (0=Normal, 1=Urgent, 2=Super-Urgent)
    
    Returns:
        int: The ID of the newly created patient record.
    
    Raises:
        ValidationError: If required fields are missing or invalid.
        DatabaseError: If database operation fails.
    
    Example:
        >>> patient_data = {
        ...     'full_name': 'John Doe',
        ...     'date_of_birth': '1990-01-01',
        ...     'status': 0
        ... }
        >>> patient_id = service.create_patient(patient_data)
        >>> print(patient_id)
        1
    """
    # Method implementation
```

### 4. Function Documentation

Standalone functions should also have docstrings.

```python
def calculate_age(date_of_birth: str) -> int:
    """
    Calculate age from date of birth.
    
    Args:
        date_of_birth (str): Date of birth in YYYY-MM-DD format.
    
    Returns:
        int: Age in years.
    
    Raises:
        ValueError: If date format is invalid.
    
    Example:
        >>> age = calculate_age('1990-01-01')
        >>> print(age)
        34
    """
    # Function implementation
```

### 5. Inline Comments

Use inline comments to explain complex logic, not obvious code.

```python
# Good: Explains why, not what
# Sort by priority: Super-Urgent (2) > Urgent (1) > Normal (0)
patients.sort(key=lambda p: p.status, reverse=True)

# Bad: States the obvious
# Sort the patients list
patients.sort()
```

---

## Documentation Format Standards

### Google-Style Docstrings

We use Google-style docstrings for consistency.

#### Sections

1. **Summary**: One-line description
2. **Description**: Detailed explanation (if needed)
3. **Args**: Parameter descriptions
4. **Returns**: Return value description
5. **Raises**: Exceptions that may be raised
6. **Example**: Usage examples

### Type Hints

Always use type hints for function/method signatures.

```python
def get_patient(self, patient_id: int) -> Optional[dict]:
    """
    Retrieve patient by ID.
    
    Args:
        patient_id: Unique patient identifier.
    
    Returns:
        Patient data dictionary or None if not found.
    """
    pass
```

---

## Code Comments

### When to Comment

1. **Complex Algorithms**: Explain non-obvious logic
2. **Business Rules**: Document business logic decisions
3. **Workarounds**: Explain temporary solutions or hacks
4. **TODOs**: Mark incomplete features
5. **Performance**: Explain performance optimizations

### Comment Style

```python
# Single-line comment for brief explanations

# Multi-line comment for detailed explanations
# This section handles priority-based queue ordering.
# Patients are sorted by status (Super-Urgent > Urgent > Normal),
# then by time added to queue within the same status level.

def process_queue(self):
    """Process queue with priority ordering."""
    # TODO: Add support for custom priority rules
    # FIXME: Handle edge case when queue is empty
    pass
```

---

## Documentation Examples

### Complete Example: Service Class

```python
"""
Queue Service Module

Provides business logic for queue management operations.
"""

from typing import List, Optional, Dict
from src.database import DatabaseManager


class QueueService:
    """
    Service class for queue management operations.
    
    This class handles all queue-related business logic including
    adding patients to queues, processing next patients, and managing
    queue capacity.
    
    Attributes:
        db_manager (DatabaseManager): Database manager for data operations
        
    Example:
        >>> db = DatabaseManager()
        >>> service = QueueService(db)
        >>> entry_id = service.add_to_queue(patient_id=1, specialization_id=1)
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize QueueService.
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
    
    def add_to_queue(self, patient_id: int, specialization_id: int) -> int:
        """
        Add a patient to a specialization queue.
        
        The patient is automatically positioned in the queue based on
        their priority status. Queue capacity is checked before adding.
        
        Args:
            patient_id: ID of the patient to add
            specialization_id: ID of the target specialization
        
        Returns:
            Queue entry ID of the newly added entry
        
        Raises:
            ValueError: If queue is at maximum capacity
            DatabaseError: If database operation fails
        
        Example:
            >>> entry_id = service.add_to_queue(patient_id=1, specialization_id=1)
            >>> print(f"Added to queue with entry ID: {entry_id}")
        """
        # Check queue capacity
        # Get patient status for priority
        # Insert into queue
        # Return entry ID
        pass
```

### Complete Example: Model Class

```python
"""
Patient Model

Data model representing a patient in the system.
"""

from datetime import date
from typing import Optional


class Patient:
    """
    Represents a patient in the hospital management system.
    
    Attributes:
        patient_id (int): Unique patient identifier
        full_name (str): Patient's full name
        date_of_birth (date): Date of birth
        gender (Optional[str]): Gender ('Male', 'Female', 'Other')
        status (int): Priority status (0=Normal, 1=Urgent, 2=Super-Urgent)
    
    Example:
        >>> patient = Patient(
        ...     patient_id=1,
        ...     full_name='John Doe',
        ...     date_of_birth=date(1990, 1, 1),
        ...     status=0
        ... )
        >>> print(patient.age)
        34
    """
    
    def __init__(self, patient_id: int, full_name: str, 
                 date_of_birth: date, status: int = 0,
                 gender: Optional[str] = None):
        """
        Initialize Patient instance.
        
        Args:
            patient_id: Unique patient identifier
            full_name: Patient's full name
            date_of_birth: Date of birth
            status: Priority status (default: 0 for Normal)
            gender: Gender (optional)
        """
        self.patient_id = patient_id
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.status = status
        self.gender = gender
    
    @property
    def age(self) -> int:
        """
        Calculate patient's age from date of birth.
        
        Returns:
            Age in years
        """
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
```

---

## Documentation Tools

### Generating Documentation

#### Sphinx (Recommended)
```bash
pip install sphinx
sphinx-quickstart
sphinx-build -b html docs/ docs/_build/
```

#### pydoc
```bash
python -m pydoc src.services.patient_service
```

### Documentation Review Checklist

- [ ] All modules have docstrings
- [ ] All classes have docstrings
- [ ] All public methods have docstrings
- [ ] Type hints are used
- [ ] Examples are provided where helpful
- [ ] Complex logic is commented
- [ ] TODOs are documented
- [ ] No obvious comments (stating the obvious)

---

## Best Practices

### Do's

✅ **Do** write clear, concise docstrings  
✅ **Do** use type hints  
✅ **Do** provide examples for complex methods  
✅ **Do** document exceptions  
✅ **Do** keep documentation up-to-date with code  
✅ **Do** explain why, not what (in comments)

### Don'ts

❌ **Don't** write obvious comments  
❌ **Don't** leave undocumented public APIs  
❌ **Don't** use outdated documentation  
❌ **Don't** write novels in docstrings  
❌ **Don't** forget to update documentation when code changes

---

## Documentation Maintenance

### When to Update Documentation

1. **Adding New Features**: Document new classes/methods
2. **Changing APIs**: Update method signatures and docstrings
3. **Fixing Bugs**: Update if documentation was incorrect
4. **Refactoring**: Ensure documentation reflects changes

### Documentation Review Process

1. Code review includes documentation review
2. Documentation is part of pull request checklist
3. Regular documentation audits
4. Update documentation with each release

---

## Conclusion

Following these documentation standards ensures:
- ✅ Code is maintainable
- ✅ APIs are understandable
- ✅ Onboarding is easier
- ✅ Project quality is maintained
- ✅ Academic standards are met

**Last Updated**: January 30, 2026  
**Version**: 1.0

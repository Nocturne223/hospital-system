-- =============================================================================
-- Hospital Management System — MySQL test / seed data
-- =============================================================================
-- Prerequisites:
--   1. CREATE DATABASE hospital_system CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
--   2. USE hospital_system;
--   3. Run schema_mysql.sql (creates empty tables + indexes).
--   4. Run this script (loads reference + demo data).
--
-- Clears all application tables and reloads consistent rows. FK-safe order.
-- Demo logins (users.password_hash = SHA2('demo123', 256)):
--   admin / demo123   (Administrator)
--   reception / demo123 (Receptionist)
--
-- SQLite: use seed_test_data_sqlite.sql after schema.sql (regenerate from this
-- file with: python src/database/materialize_sqlite_seed.py).
-- =============================================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE audit_logs;
TRUNCATE TABLE queue_entries;
TRUNCATE TABLE appointments;
TRUNCATE TABLE doctor_specializations;
TRUNCATE TABLE doctors;
TRUNCATE TABLE patients;
TRUNCATE TABLE users;
TRUNCATE TABLE specializations;

SET FOREIGN_KEY_CHECKS = 1;

-- -----------------------------------------------------------------------------
-- Specializations (queue capacity drives QueueService validation)
-- -----------------------------------------------------------------------------
INSERT INTO specializations (specialization_id, name, description, max_capacity, is_active) VALUES
(1, 'Internal Medicine', 'Primary and chronic adult care, preventive visits.', 15, 1),
(2, 'Pediatrics', 'Care for infants, children, and adolescents.', 12, 1),
(3, 'Cardiology', 'Heart and vascular conditions.', 10, 1),
(4, 'Orthopedics', 'Bones, joints, and musculoskeletal injuries.', 10, 1),
(5, 'Emergency Medicine', 'Acute and urgent presentations.', 20, 1),
(6, 'Dermatology', 'Skin, hair, and nail disorders.', 8, 1),
(7, 'Obstetrics and Gynecology', 'Womens health and maternity care.', 10, 1),
(8, 'Psychiatry', 'Mental health assessment and treatment.', 8, 1),
(9, 'Ophthalmology', 'Eye disease, vision, and surgical eye care.', 10, 1),
(10, 'Otolaryngology', 'Ear, nose, and throat disorders.', 8, 1),
(11, 'Nephrology', 'Kidney disease and hypertension renal workup.', 6, 1),
(12, 'Pulmonology', 'Lung disease, asthma, and sleep-disordered breathing.', 8, 1),
(13, 'Sports Medicine', 'Athletic injury clinic - seasonally paused.', 12, 0);

-- -----------------------------------------------------------------------------
-- Doctors (status + unique license_number; mix Active / Inactive / On Leave)
-- -----------------------------------------------------------------------------
INSERT INTO doctors (doctor_id, full_name, title, license_number, phone_number, email, office_address, medical_degree, years_of_experience, certifications, status, bio, hire_date) VALUES
(1, 'Elena Ruiz', 'MD', 'LIC-IM-2010-001', '+63-917-100-0001', 'e.ruiz@gmail.com', 'Building A, Room 101', 'MD Internal Medicine', 14, 'ABIM Internal Medicine', 'Active', 'Focus on diabetes and hypertension.', '2018-03-12'),
(2, 'Marcus Tan', 'MD', 'LIC-IM-2011-002', '+63-917-100-0002', 'm.tan@outlook.com', 'Building A, Room 102', 'MD Internal Medicine', 12, 'ABIM; Geriatrics board eligible', 'Active', 'Geriatric primary care.', '2019-06-01'),
(3, 'Sofia Reyes', 'MD', 'LIC-PED-2008-003', '+63-917-100-0003', 's.reyes@yahoo.com', 'Building B, Room 201', 'MD Pediatrics', 18, 'AAP; PALS', 'Active', 'Developmental pediatrics interest.', '2015-01-15'),
(4, 'James Ocampo', 'DO', 'LIC-PED-2015-004', '+63-917-100-0004', 'j.ocampo@icloud.com', 'Building B, Room 202', 'DO Pediatrics', 9, 'AAP', 'Active', 'General pediatrics.', '2020-08-10'),
(5, 'Anna Villarin', 'MD', 'LIC-CAR-2005-005', '+63-917-100-0005', 'a.villarin@hotmail.com', 'Building C, Suite 301', 'MD Cardiology', 22, 'ABIM Cardiology; Echo certified', 'Active', 'Heart failure clinic lead.', '2012-04-22'),
(6, 'David Cruz', 'MD', 'LIC-CAR-2014-006', '+63-917-100-0006', 'd.cruz@proton.me', 'Building C, Suite 302', 'MD Cardiology', 11, 'ABIM Cardiology', 'Active', 'Interventional cardiology.', '2018-11-05'),
(7, 'Luis Mendoza', 'MD', 'LIC-ORT-2009-007', '+63-917-100-0007', 'l.mendoza@live.com', 'Building D, OR Wing', 'MD Orthopedic Surgery', 16, 'Sports medicine fellowship', 'Active', 'Knee and shoulder surgery.', '2014-02-17'),
(8, 'Priya Nair', 'MD', 'LIC-ER-2012-008', '+63-917-100-0008', 'p.nair@aol.com', 'ER Pod 1', 'MD Emergency Medicine', 13, 'ATLS; ACLS', 'Active', 'Trauma team.', '2016-07-30'),
(9, 'Kenji Yamamoto', 'MD', 'LIC-DER-2016-009', '+63-917-100-0009', 'k.yamamoto@gmail.com', 'Building E, Room 401', 'MD Dermatology', 8, 'AAD', 'Active', 'Dermatopathology interest.', '2021-01-11'),
(10, 'Rosa Almario', 'MD', 'LIC-OBG-2007-010', '+63-917-100-0010', 'r.almario@outlook.com', 'Maternity Wing 2F', 'MD OB-GYN', 19, 'ACOG', 'Active', 'High-risk pregnancy clinic.', '2013-09-09'),
(11, 'Noah Bautista', 'MD', 'LIC-OBG-2018-011', '+63-917-100-0011', 'n.bautista@yahoo.com', 'Maternity Wing 2F', 'MD OB-GYN', 7, 'ACOG', 'Active', 'General OB-GYN.', '2019-05-20'),
(12, 'Clara Santos', 'MD', 'LIC-PSY-2013-012', '+63-917-100-0012', 'c.santos@icloud.com', 'Behavioral Health Center', 'MD Psychiatry', 11, 'ABPN', 'Active', 'Adult outpatient psychiatry.', '2017-10-02'),
(13, 'Victor Ramos', 'MD', 'LIC-IM-1999-013', '+63-917-100-0013', 'v.ramos@hotmail.com', 'Building A, Room 105', 'MD Internal Medicine', 25, 'ABIM', 'Inactive', 'Retired from clinical schedule.', '2010-01-04'),
(14, 'Grace Lim', 'MD', 'LIC-CAR-2010-014', '+63-917-100-0014', 'g.lim@proton.me', 'Building C, Suite 303', 'MD Cardiology', 15, 'ABIM Cardiology', 'On Leave', 'Sabbatical.', '2015-08-14'),
(15, 'Amara Okonkwo', 'MD', 'LIC-OPH-2019-015', '+63-917-100-0015', 'a.okonkwo@live.com', 'Eye Center Wing 1F', 'MD Ophthalmology', 6, 'AAO', 'Active', 'Cataract and glaucoma.', '2022-04-18'),
(16, 'Jonas Lindstrom', 'MD', 'LIC-ENT-2016-016', '+63-917-100-0016', 'j.lindstrom@aol.com', 'ENT Suite 3B', 'MD Otolaryngology', 9, 'ABOHNS eligible', 'Active', 'Pediatric ENT focus.', '2019-01-07'),
(17, 'Mei-Lin Huang', 'MD', 'LIC-NEP-2011-017', '+63-917-100-0017', 'm.huang@gmail.com', 'Renal Clinic 2F', 'MD Nephrology', 14, 'ABIM Nephrology', 'Active', 'Dialysis coordination.', '2014-09-23'),
(18, 'Omar Haddad', 'MD', 'LIC-PUL-2013-018', '+63-917-100-0018', 'o.haddad@outlook.com', 'Pulmonary Lab B', 'MD Pulmonology', 12, 'ABIM Pulmonary', 'Active', 'ILD and COPD programs.', '2016-05-11'),
(19, 'Priya Kapoor', 'MD', 'LIC-IM-2020-019', '+63-917-100-0019', 'p.kapoor@yahoo.com', 'Ward Tower 4', 'MD Internal Medicine', 5, 'ABIM', 'Active', 'Hospitalist rotations.', '2021-07-01'),
(20, 'Diego Ferreira', 'MD', 'LIC-ER-2021-020', '+63-917-100-0020', 'd.ferreira@icloud.com', 'ER Pod 2', 'MD Emergency Medicine', 4, 'ATLS', 'Active', 'Night shift lead.', '2022-11-14'),
(21, 'Yuki Taneda', 'MD', 'LIC-DER-2004-021', '+63-917-100-0021', 'y.taneda@hotmail.com', 'Building E Room 405', 'MD Dermatology', 21, 'AAD', 'Inactive', 'Research leave.', '2009-02-28'),
(22, 'Helena Costa', 'MD', 'LIC-OPH-2008-022', '+63-917-100-0022', 'h.costa@proton.me', 'Eye Center Wing 1F', 'MD Ophthalmology', 17, 'AAO', 'On Leave', 'Family leave.', '2011-08-16'),
(23, 'Robert Kaminski', 'MD', 'LIC-IMCAR-2015-023', '+63-917-100-0023', 'r.kaminski@live.com', 'Building C Suite 305', 'MD Cardiology', 10, 'ABIM IM and Cardiology', 'Active', 'Dual clinic IM and cardiology.', '2017-12-04');

-- -----------------------------------------------------------------------------
-- Doctor ↔ specialization (every practicing doctor matches appointment rows)
-- -----------------------------------------------------------------------------
INSERT INTO doctor_specializations (doctor_id, specialization_id) VALUES
(1, 1), (2, 1),
(3, 2), (4, 2),
(5, 3), (6, 3),
(7, 4),
(8, 5),
(9, 6),
(10, 7), (11, 7),
(12, 8),
(13, 1),
(14, 3),
(15, 9), (16, 10), (17, 11), (18, 12),
(19, 1), (20, 5), (21, 6), (22, 9),
(23, 1), (23, 3);

-- -----------------------------------------------------------------------------
-- Patients (status 0–2; varied gender, registration_date for report windows)
-- -----------------------------------------------------------------------------
INSERT INTO patients (patient_id, full_name, date_of_birth, gender, phone_number, email, address, emergency_contact_name, emergency_contact_relationship, emergency_contact_phone, blood_type, allergies, medical_history, status, registration_date) VALUES
(1, 'Andrea Magbanua', '1992-04-18', 'Female', '+63-918-200-0001', 'a.magbanua@aol.com', 'Quezon City', 'Luis Magbanua', 'Spouse', '+63-918-200-0101', 'O+', 'Penicillin', 'Asthma childhood', 0, DATE_SUB(NOW(), INTERVAL 2 DAY)),
(2, 'Brian Flores', '1985-11-02', 'Male', '+63-918-200-0002', 'b.flores@gmail.com', 'Makati', 'Cara Flores', 'Spouse', '+63-918-200-0102', 'A+', NULL, 'Hypertension', 1, DATE_SUB(NOW(), INTERVAL 5 DAY)),
(3, 'Carmen Dela Cruz', '1978-07-29', 'Female', '+63-918-200-0003', 'c.delacruz@outlook.com', 'Manila', 'Rico Dela Cruz', 'Brother', '+63-918-200-0103', 'B+', 'Sulfa drugs', 'Type 2 diabetes', 2, DATE_SUB(NOW(), INTERVAL 12 DAY)),
(4, 'Daniel Navarro', '2001-03-14', 'Male', '+63-918-200-0004', 'd.navarro@yahoo.com', 'Pasig', 'Mila Navarro', 'Mother', '+63-918-200-0104', 'O-', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 1 DAY)),
(5, 'Elise Gomez', '2016-09-21', 'Female', '+63-918-200-0005', 'parent.egomez@icloud.com', 'Taguig', 'Paul Gomez', 'Father', '+63-918-200-0105', 'A-', NULL, 'Eczema', 0, DATE_SUB(NOW(), INTERVAL 8 DAY)),
(6, 'Felix Herrera', '1969-12-05', 'Male', '+63-918-200-0006', 'f.herrera@hotmail.com', 'Paranaque', 'Rita Herrera', 'Wife', '+63-918-200-0106', 'AB+', 'Shellfish', 'CAD post-stent', 1, DATE_SUB(NOW(), INTERVAL 20 DAY)),
(7, 'Gina Torres', '1995-06-30', 'Female', '+63-918-200-0007', 'g.torres@proton.me', 'Mandaluyong', 'Mara Torres', 'Sister', '+63-918-200-0107', 'B-', NULL, 'Migraine', 0, DATE_SUB(NOW(), INTERVAL 35 DAY)),
(8, 'Hector Salazar', '1988-01-17', 'Male', '+63-918-200-0008', 'h.salazar@live.com', 'Las Pinas', 'Ivy Salazar', 'Wife', '+63-918-200-0108', 'O+', NULL, 'GERD', 0, DATE_SUB(NOW(), INTERVAL 45 DAY)),
(9, 'Iris Castillo', '2008-05-08', 'Female', '+63-918-200-0009', 'i.castillo@aol.com', 'Marikina', 'Ben Castillo', 'Father', '+63-918-200-0109', 'A+', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 3 DAY)),
(10, 'Julian Morales', '1962-10-26', 'Male', '+63-918-200-0010', 'j.morales@gmail.com', 'Caloocan', 'Nora Morales', 'Wife', '+63-918-200-0110', 'B+', 'NSAIDs', 'COPD', 2, DATE_SUB(NOW(), INTERVAL 60 DAY)),
(11, 'Karen Pascual', '1990-02-11', 'Female', '+63-918-200-0011', 'k.pascual@outlook.com', 'San Juan', 'Leo Pascual', 'Husband', '+63-918-200-0111', 'O+', NULL, 'Hypothyroid', 0, DATE_SUB(NOW(), INTERVAL 7 DAY)),
(12, 'Leo Fernandez', '1974-08-19', 'Male', '+63-918-200-0012', 'l.fernandez@yahoo.com', 'Valenzuela', 'Amy Fernandez', 'Wife', '+63-918-200-0112', 'A-', NULL, 'Hyperlipidemia', 0, DATE_SUB(NOW(), INTERVAL 90 DAY)),
(13, 'Mia Rosario', '2012-12-01', 'Female', '+63-918-200-0013', 'parent.mrosario@icloud.com', 'Cavite', 'Tess Rosario', 'Mother', '+63-918-200-0113', 'B-', NULL, 'Allergic rhinitis', 0, DATE_SUB(NOW(), INTERVAL 15 DAY)),
(14, 'Nico Valdez', '1981-04-07', 'Male', '+63-918-200-0014', 'n.valdez@hotmail.com', 'Laguna', 'Joy Valdez', 'Wife', '+63-918-200-0114', 'AB-', NULL, 'CKD stage 2', 1, DATE_SUB(NOW(), INTERVAL 25 DAY)),
(15, 'Olivia Ramos', '1999-09-15', 'Female', '+63-918-200-0015', 'o.ramos@proton.me', 'Batangas', 'Dan Ramos', 'Brother', '+63-918-200-0115', 'O+', 'Latex', NULL, 0, DATE_SUB(NOW(), INTERVAL 4 DAY)),
(16, 'Paolo Ignacio', '2005-07-22', 'Male', '+63-918-200-0016', 'p.ignacio@live.com', 'Rizal', 'Sara Ignacio', 'Mother', '+63-918-200-0116', 'A+', NULL, 'Sports injury follow-up', 0, DATE_SUB(NOW(), INTERVAL 10 DAY)),
(17, 'Quinn Mercado', '1971-03-03', 'Other', '+63-918-200-0017', 'q.mercado@aol.com', 'Bulacan', 'Alex Mercado', 'Partner', '+63-918-200-0117', 'B+', NULL, 'Depression in remission', 0, DATE_SUB(NOW(), INTERVAL 55 DAY)),
(18, 'Rina Aquino', '1987-11-28', 'Female', '+63-918-200-0018', 'r.aquino@gmail.com', 'Pampanga', 'Mark Aquino', 'Husband', '+63-918-200-0118', 'O-', NULL, 'Anemia', 0, DATE_SUB(NOW(), INTERVAL 18 DAY)),
(19, 'Sam Villanueva', '2010-06-06', 'Male', '+63-918-200-0019', 'parent.svillanueva@outlook.com', 'Cebu', 'Ella Villanueva', 'Mother', '+63-918-200-0119', 'A+', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 6 DAY)),
(20, 'Tessa Romero', '1994-01-25', 'Female', '+63-918-200-0020', 't.romero@yahoo.com', 'Iloilo', 'Jake Romero', 'Friend', '+63-918-200-0120', 'AB+', 'Iodine', 'Thyroid nodule', 1, DATE_SUB(NOW(), INTERVAL 33 DAY)),
(21, 'Ulysses Bautista', '1958-05-14', 'Male', '+63-918-200-0021', 'u.bautista@icloud.com', 'Davao', 'Lita Bautista', 'Wife', '+63-918-200-0121', 'B-', NULL, 'Atrial fibrillation', 2, DATE_SUB(NOW(), INTERVAL 70 DAY)),
(22, 'Vera Concepcion', '2003-10-10', 'Female', '+63-918-200-0022', 'v.concepcion@hotmail.com', 'Baguio', 'Miguel Concepcion', 'Father', '+63-918-200-0122', 'O+', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 9 DAY)),
(23, 'Wayne Padilla', '1983-02-02', 'Male', '+63-918-200-0023', 'w.padilla@proton.me', 'Zamboanga', 'Irene Padilla', 'Wife', '+63-918-200-0123', 'A-', 'Contrast dye', 'Kidney stones history', 0, DATE_SUB(NOW(), INTERVAL 42 DAY)),
(24, 'Xara Domingo', '2015-08-08', 'Female', '+63-918-200-0024', 'parent.xdomingo@live.com', 'Cagayan de Oro', 'Noel Domingo', 'Father', '+63-918-200-0124', 'B+', NULL, 'Vaccinations up to date', 0, DATE_SUB(NOW(), INTERVAL 11 DAY)),
(25, 'Yves Santiago', '1991-12-19', 'Male', '+63-918-200-0025', 'y.santiago@aol.com', 'General Santos', 'Pat Santiago', 'Sister', '+63-918-200-0125', 'O+', NULL, 'Lower back pain', 0, DATE_SUB(NOW(), INTERVAL 16 DAY)),
(26, 'Zoe Manalo', '1976-06-07', 'Female', '+63-918-200-0026', 'z.manalo@gmail.com', 'Naga', 'Ron Manalo', 'Husband', '+63-918-200-0126', 'A+', 'Aspirin', 'Breast cancer survivor', 1, DATE_SUB(NOW(), INTERVAL 80 DAY)),
(27, 'Aaron Espino', '2007-04-04', 'Male', '+63-918-200-0027', 'a.espino@outlook.com', 'Lucena', 'Lyn Espino', 'Mother', '+63-918-200-0127', 'B-', NULL, 'ADHD follow-up', 0, DATE_SUB(NOW(), INTERVAL 14 DAY)),
(28, 'Bianca Lorenzo', '1989-09-09', 'Female', '+63-918-200-0028', 'b.lorenzo@yahoo.com', 'Tarlac', 'Ken Lorenzo', 'Husband', '+63-918-200-0128', 'AB+', NULL, 'PCOS', 0, DATE_SUB(NOW(), INTERVAL 28 DAY)),
(29, 'Carlo Medina', '1967-01-31', 'Male', '+63-918-200-0029', 'c.medina@icloud.com', 'Bacolod', 'Grace Medina', 'Wife', '+63-918-200-0129', 'O+', NULL, 'Stroke recovery', 2, DATE_SUB(NOW(), INTERVAL 50 DAY)),
(30, 'Dina Fabian', '1998-07-07', 'Female', '+63-918-200-0030', 'd.fabian@hotmail.com', 'Ilocos', 'Jo Fabian', 'Mother', '+63-918-200-0130', 'A-', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 22 DAY)),
(31, 'Erwin Castillo', '1982-03-20', 'Male', '+63-918-200-0031', 'e.castillo2@proton.me', 'Antipolo', 'May Castillo', 'Wife', '+63-918-200-0131', 'B+', NULL, 'Sleep apnea', 0, DATE_SUB(NOW(), INTERVAL 36 DAY)),
(32, 'Faith Ong', '2013-11-11', 'Female', '+63-918-200-0032', 'parent.fong@live.com', 'Muntinlupa', 'Tim Ong', 'Father', '+63-918-200-0132', 'O-', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 5 DAY)),
(33, 'Gabe Trinidad', '1973-05-25', 'Male', '+63-918-200-0033', 'g.trinidad@aol.com', 'Pasay', 'Liza Trinidad', 'Wife', '+63-918-200-0133', 'A+', 'Statins intolerance', 'Gout', 0, DATE_SUB(NOW(), INTERVAL 65 DAY)),
(34, 'Hannah Sy', '1996-10-16', 'Female', '+63-918-200-0034', 'h.sy@gmail.com', 'Mandaluyong', 'Jon Sy', 'Brother', '+63-918-200-0134', 'B-', NULL, 'Anxiety', 0, DATE_SUB(NOW(), INTERVAL 13 DAY)),
(35, 'Ian Chua', '2000-02-28', 'Male', '+63-918-200-0035', 'i.chua@outlook.com', 'Binondo', 'Helen Chua', 'Mother', '+63-918-200-0135', 'AB-', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 0 DAY)),
(36, 'Jade Vergara', '1986-08-08', 'Female', '+63-918-200-0036', 'j.vergara@yahoo.com', 'Alabang', 'Pat Vergara', 'Husband', '+63-918-200-0136', 'O+', NULL, 'Pregnancy 28 weeks', 1, DATE_SUB(NOW(), INTERVAL 17 DAY)),
(37, 'Kurt Angeles', '1955-12-12', 'Male', '+63-918-200-0037', 'k.angeles@icloud.com', 'Ermita', 'Nina Angeles', 'Daughter', '+63-918-200-0137', 'A+', NULL, 'CHF', 2, DATE_SUB(NOW(), INTERVAL 75 DAY)),
(38, 'Lara Dizon', '2011-01-01', 'Female', '+63-918-200-0038', 'parent.ldizon@hotmail.com', 'Fairview', 'Kim Dizon', 'Mother', '+63-918-200-0138', 'B+', NULL, 'Asthma', 0, DATE_SUB(NOW(), INTERVAL 19 DAY)),
(39, 'Miguel Soriano', '1993-05-05', 'Male', '+63-918-200-0039', 'm.soriano@proton.me', 'Ortigas', 'Ella Soriano', 'Partner', '+63-918-200-0139', 'O+', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 27 DAY)),
(40, 'Nina Laurel', '1979-09-09', 'Female', '+63-918-200-0040', 'n.laurel@live.com', 'BGC', 'Omar Laurel', 'Husband', '+63-918-200-0140', 'A-', 'Codeine', 'Fibromyalgia', 0, DATE_SUB(NOW(), INTERVAL 48 DAY)),
(41, 'Chijioke Nwosu', '1984-02-14', 'Male', '+63-918-301-0041', 'c.nwosu@aol.com', 'Iloilo City', 'Ada Nwosu', 'Spouse', '+63-918-301-0141', 'O+', NULL, 'Seasonal allergies', 0, DATE_SUB(NOW(), INTERVAL 100 DAY)),
(42, 'Ewa Kowalczyk', '1997-11-30', 'Female', '+63-918-301-0042', 'e.kowalczyk@gmail.com', 'Cebu IT Park', 'Tomasz Kowalczyk', 'Brother', '+63-918-301-0142', 'A+', 'Peanuts', NULL, 1, DATE_SUB(NOW(), INTERVAL 3 DAY)),
(43, 'Hiroshi Sato', '1951-06-21', 'Male', '+63-918-301-0043', 'h.sato@outlook.com', 'Mandaue', 'Yuki Sato', 'Wife', '+63-918-301-0143', 'B+', NULL, 'Pacemaker 2019', 2, DATE_SUB(NOW(), INTERVAL 120 DAY)),
(44, 'Carmen Valdez-Miranda', '2002-08-09', 'Female', '+63-918-301-0044', 'c.valdez@yahoo.com', 'Dumaguete', 'Rosa Miranda', 'Mother', '+63-918-301-0144', 'AB+', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 14 DAY)),
(45, 'Adeola Okafor', '1991-01-05', 'Female', '+63-918-301-0045', 'a.okafor@icloud.com', 'Lagos Village QC', 'Tunde Okafor', 'Husband', '+63-918-301-0145', 'O-', 'Eggs', 'Sickle trait carrier', 0, DATE_SUB(NOW(), INTERVAL 77 DAY)),
(46, 'Erik Lindqvist', '1970-09-19', 'Male', '+63-918-301-0046', 'e.lindqvist@hotmail.com', 'Rockwell', 'Ingrid Lindqvist', 'Wife', '+63-918-301-0146', 'A-', NULL, 'Psoriasis', 0, DATE_SUB(NOW(), INTERVAL 95 DAY)),
(47, 'Linh Nguyen', '1988-04-27', 'Female', '+63-918-301-0047', 'l.nguyen@proton.me', 'Saigon St Parañaque', 'Minh Nguyen', 'Father', '+63-918-301-0147', 'B-', NULL, 'Gestational DM prior', 1, DATE_SUB(NOW(), INTERVAL 29 DAY)),
(48, 'Arjun Mehta', '2014-12-12', 'Male', '+63-918-301-0048', 'parent.mehta@live.com', 'Kapitolyo', 'Sunita Mehta', 'Mother', '+63-918-301-0148', 'O+', NULL, 'Tonsillectomy 2023', 0, DATE_SUB(NOW(), INTERVAL 8 DAY)),
(49, 'Greta Mueller', '1965-03-03', 'Female', '+63-918-301-0049', 'g.mueller@aol.com', 'Bonifacio Global City', 'Klaus Mueller', 'Husband', '+63-918-301-0149', 'A+', 'Morphine', 'Rheumatoid arthritis', 2, DATE_SUB(NOW(), INTERVAL 110 DAY)),
(50, 'Kwame Asante', '1999-07-16', 'Male', '+63-918-301-0050', 'k.asante@gmail.com', 'Eastwood', 'Ama Asante', 'Mother', '+63-918-301-0150', 'B+', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 21 DAY)),
(51, 'Svetlana Petrov', '1977-12-01', 'Female', '+63-918-301-0051', 's.petrov@outlook.com', 'Makati CBD', NULL, NULL, NULL, 'O+', 'Dairy', 'Migraine with aura', 0, DATE_SUB(NOW(), INTERVAL 52 DAY)),
(52, 'Mateo Silva', '2009-05-20', 'Male', '+63-918-301-0052', 'parent.silva@yahoo.com', 'Las Piñas', 'Carla Silva', 'Mother', '+63-918-301-0152', 'A-', NULL, 'Scoliosis watch', 0, DATE_SUB(NOW(), INTERVAL 17 DAY)),
(53, 'Amira El-Sayed', '1994-10-10', 'Female', '+63-918-301-0053', 'a.elsayed@icloud.com', 'New Manila', 'Omar El-Sayed', 'Brother', '+63-918-301-0153', 'AB-', NULL, 'Iron deficiency', 0, DATE_SUB(NOW(), INTERVAL 41 DAY)),
(54, 'Bjorn Andersen', '1981-01-28', 'Male', '+63-918-301-0054', 'b.andersen@hotmail.com', 'Tagaytay', 'Freja Andersen', 'Wife', '+63-918-301-0154', 'B+', NULL, 'Sleep apnea on CPAP', 1, DATE_SUB(NOW(), INTERVAL 66 DAY)),
(55, 'Baby Girl Reyes', '2024-06-01', 'Female', '+63-918-301-0055', 'parent.breyes@proton.me', 'Sta Mesa', 'Lara Reyes', 'Mother', '+63-918-301-0155', 'O-', NULL, 'Newborn follow-up', 0, DATE_SUB(NOW(), INTERVAL 30 DAY)),
(56, 'Teodoro Agbayani', '1940-03-15', 'Male', '+63-918-301-0056', 't.agbayani@live.com', 'San Fernando Pampanga', 'Lourdes Agbayani', 'Daughter', '+63-918-301-0156', 'A+', NULL, 'BPH, hearing loss', 2, DATE_SUB(NOW(), INTERVAL 140 DAY)),
(57, 'Rowan Blake', '2000-09-09', NULL, '+63-918-301-0057', 'r.blake@aol.com', 'Katipunan', 'Jordan Blake', 'Parent', '+63-918-301-0157', 'Unknown', NULL, 'Preferred name on file', 0, DATE_SUB(NOW(), INTERVAL 6 DAY)),
(58, 'Fatima Al-Rashid', '1986-04-04', 'Female', NULL, 'f.alrashid@gmail.com', 'Ortigas Center', 'Hassan Al-Rashid', 'Spouse', '+63-918-301-0158', 'B-', 'Bee venom', 'Pregnancy 12 weeks', 1, DATE_SUB(NOW(), INTERVAL 2 DAY)),
(59, 'Chen Wei', '1973-11-11', 'Male', '+63-918-301-0059', NULL, 'Chinatown Manila', 'Li Na Chen', 'Wife', '+63-918-301-0159', 'O+', NULL, 'Hep B carrier monitoring', 0, DATE_SUB(NOW(), INTERVAL 88 DAY)),
(60, 'Zara Hussen', '2011-02-22', 'Female', '+63-918-301-0060', 'parent.zhussen@outlook.com', 'Cainta', 'Samira Hussen', 'Mother', '+63-918-301-0160', 'A+', NULL, 'Type 1 diabetes', 2, DATE_SUB(NOW(), INTERVAL 24 DAY)),
(61, 'Luca Romano', '1992-06-06', 'Male', '+63-918-301-0061', 'l.romano@yahoo.com', 'Forbes Town', 'Giulia Romano', 'Sister', '+63-918-301-0161', 'AB+', 'Sulfa', 'Celiac disease', 0, DATE_SUB(NOW(), INTERVAL 39 DAY)),
(62, 'Naledi Mokoena', '1989-08-18', 'Female', '+63-918-301-0062', 'n.mokoena@icloud.com', 'Muntinlupa', 'Thabo Mokoena', 'Partner', '+63-918-301-0162', 'O+', NULL, 'Lupus stable', 1, DATE_SUB(NOW(), INTERVAL 58 DAY)),
(63, 'Oskar Nilsson', '1968-10-31', 'Male', '+63-918-301-0063', 'o.nilsson@hotmail.com', 'Alabang West', 'Elin Nilsson', 'Wife', '+63-918-301-0163', 'B-', NULL, 'AAA surveillance', 2, DATE_SUB(NOW(), INTERVAL 72 DAY)),
(64, 'Priya Sundaram', '2004-01-25', 'Female', '+63-918-301-0064', 'p.sundaram@proton.me', 'Circuit Makati', 'Venkat Sundaram', 'Father', '+63-918-301-0164', 'A-', NULL, 'Menorrhagia workup', 0, DATE_SUB(NOW(), INTERVAL 11 DAY)),
(65, 'Quentin Brooks', '1975-05-05', 'Male', '+63-918-301-0065', 'q.brooks@live.com', 'Ayala West', 'Mel Brooks', 'Wife', '+63-918-301-0165', 'O+', 'Ibuprofen', 'ACL repair 2022', 0, DATE_SUB(NOW(), INTERVAL 47 DAY)),
(66, 'Rosa Delgado', '1998-12-24', 'Female', '+63-918-301-0066', 'r.delgado@aol.com', 'Las Casas', 'Miguel Delgado', 'Father', '+63-918-301-0166', 'B+', NULL, NULL, 0, DATE_SUB(NOW(), INTERVAL 19 DAY)),
(67, 'Sanjay Krishnan', '1959-07-07', 'Male', '+63-918-301-0067', 's.krishnan@gmail.com', 'White Plains', 'Anita Krishnan', 'Wife', '+63-918-301-0167', 'A+', NULL, 'Parkinson disease', 2, DATE_SUB(NOW(), INTERVAL 103 DAY)),
(68, 'Talia Ben-David', '1993-03-17', 'Female', '+63-918-301-0068', 't.bendavid@outlook.com', 'Legaspi Village', 'Noam Ben-David', 'Husband', '+63-918-301-0168', 'O-', NULL, 'PTSD therapy ongoing', 0, DATE_SUB(NOW(), INTERVAL 33 DAY)),
(69, 'Ugochi Eze', '2017-09-09', 'Female', '+63-918-301-0069', 'parent.ueze@yahoo.com', 'Antipolo', 'Chidi Eze', 'Father', '+63-918-301-0169', 'B+', NULL, 'Febrile seizure history', 0, DATE_SUB(NOW(), INTERVAL 9 DAY)),
(70, 'Viktor Popov', '1982-11-29', 'Male', '+63-918-301-0070', 'v.popov@icloud.com', 'Capitol Commons', 'Irina Popova', 'Wife', '+63-918-301-0170', 'A-', NULL, 'Hyperthyroid treated', 0, DATE_SUB(NOW(), INTERVAL 54 DAY)),
(71, 'Wanda Kaczmarek', '1961-04-08', 'Female', '+63-918-301-0071', 'w.kaczmarek@hotmail.com', 'Warsaw St QC', NULL, NULL, NULL, 'B+', 'Warfarin interaction notes', 'Breast CA remission', 1, DATE_SUB(NOW(), INTERVAL 91 DAY)),
(72, 'Xavier Lo', '2006-02-02', 'Male', '+63-918-301-0072', 'x.lo@proton.me', 'Greenhills', 'Jen Lo', 'Mother', '+63-918-301-0172', 'O+', NULL, 'ACL sports screening', 0, DATE_SUB(NOW(), INTERVAL 16 DAY)),
(73, 'Yelena Volkov', '1990-08-08', NULL, '+63-918-301-0073', 'y.volkov@live.com', 'McKinley West', 'Ivan Volkov', 'Brother', '+63-918-301-0173', 'AB+', NULL, 'Chronic kidney disease stage 3', 1, DATE_SUB(NOW(), INTERVAL 44 DAY)),
(74, 'Zain Abbasi', '1972-12-25', 'Male', '+63-918-301-0074', 'z.abbasi@aol.com', 'Filinvest', 'Hira Abbasi', 'Wife', '+63-918-301-0174', 'A+', 'Contrast', 'Diabetic nephropathy', 2, DATE_SUB(NOW(), INTERVAL 68 DAY)),
(75, 'Aiko Morimoto', '2013-06-30', 'Female', '+63-918-301-0075', 'parent.amorimoto@gmail.com', 'Mall of Asia area', 'Ken Morimoto', 'Father', '+63-918-301-0175', 'B-', NULL, 'Myopia progression', 0, DATE_SUB(NOW(), INTERVAL 12 DAY)),
(76, 'Bruno Carvalho', '1987-01-19', 'Male', '+63-918-301-0076', 'b.carvalho@outlook.com', 'Acacia Estates', 'Isabel Carvalho', 'Wife', '+63-918-301-0176', 'O+', NULL, 'OSA on APAP', 0, DATE_SUB(NOW(), INTERVAL 37 DAY)),
(77, 'Chioma Nwankwo', '1996-05-14', 'Female', '+63-918-301-0077', 'c.nwankwo@yahoo.com', 'Kapitolyo Pasig', 'Obi Nwankwo', 'Husband', '+63-918-301-0177', 'O-', NULL, 'Fibroids', 0, DATE_SUB(NOW(), INTERVAL 26 DAY)),
(78, 'Dmitri Volkov', '2001-10-01', 'Male', '+63-918-301-0078', 'd.volkov@icloud.com', 'McKinley West', 'Yelena Volkov', 'Sister', '+63-918-301-0178', 'B+', NULL, 'Hearing test referral', 0, DATE_SUB(NOW(), INTERVAL 7 DAY)),
(79, 'Esperanza Cruz', '1954-02-29', 'Female', '+63-918-301-0079', 'e.cruz@hotmail.com', 'Taft Avenue', 'Ramon Cruz', 'Son', '+63-918-301-0179', 'A-', NULL, 'Osteoporosis', 2, DATE_SUB(NOW(), INTERVAL 125 DAY)),
(80, 'Finn OConnell', '1995-07-04', 'Male', '+63-918-301-0080', 'f.oconnell@proton.me', 'Kerry St BGC', 'Siobhan OConnell', 'Sister', '+63-918-301-0180', 'AB-', 'Latex', 'Occupational asthma', 0, DATE_SUB(NOW(), INTERVAL 34 DAY));

-- -----------------------------------------------------------------------------
-- Appointments (all statuses + types; dates relative to CURDATE() for analytics)
-- -----------------------------------------------------------------------------
INSERT INTO appointments (appointment_id, patient_id, doctor_id, specialization_id, appointment_date, appointment_time, duration, appointment_type, reason, notes, status, cancelled_at, cancellation_reason) VALUES
(1, 1, 1, 1, DATE_SUB(CURDATE(), INTERVAL 45 DAY), '09:00:00', 30, 'Regular', 'Annual physical', NULL, 'Completed', NULL, NULL),
(2, 2, 5, 3, DATE_SUB(CURDATE(), INTERVAL 40 DAY), '10:30:00', 45, 'Follow-up', 'Post-MI follow-up', NULL, 'Completed', NULL, NULL),
(3, 3, 1, 1, DATE_SUB(CURDATE(), INTERVAL 35 DAY), '11:00:00', 30, 'Regular', 'Diabetes review', NULL, 'Completed', NULL, NULL),
(4, 6, 5, 3, DATE_SUB(CURDATE(), INTERVAL 30 DAY), '14:00:00', 30, 'Follow-up', 'Echo review', NULL, 'No-Show', NULL, NULL),
(5, 7, 3, 2, DATE_SUB(CURDATE(), INTERVAL 28 DAY), '08:30:00', 30, 'Regular', 'Well child visit', NULL, 'Completed', NULL, NULL),
(6, 10, 2, 1, DATE_SUB(CURDATE(), INTERVAL 25 DAY), '15:15:00', 30, 'Regular', 'COPD exacerbation', 'Bring inhaler', 'Cancelled', DATE_SUB(NOW(), INTERVAL 24 DAY), 'Patient requested reschedule'),
(7, 11, 9, 6, DATE_SUB(CURDATE(), INTERVAL 22 DAY), '13:00:00', 20, 'Regular', 'Rash evaluation', NULL, 'Completed', NULL, NULL),
(8, 14, 6, 3, DATE_SUB(CURDATE(), INTERVAL 20 DAY), '09:45:00', 30, 'Follow-up', 'BP check', NULL, 'Completed', NULL, NULL),
(9, 15, 10, 7, DATE_SUB(CURDATE(), INTERVAL 18 DAY), '10:00:00', 40, 'Regular', 'Prenatal visit', NULL, 'Completed', NULL, NULL),
(10, 17, 12, 8, DATE_SUB(CURDATE(), INTERVAL 15 DAY), '16:00:00', 45, 'Follow-up', 'Medication review', NULL, 'Completed', NULL, NULL),
(11, 18, 7, 4, DATE_SUB(CURDATE(), INTERVAL 12 DAY), '11:30:00', 30, 'Regular', 'Knee pain', NULL, 'Completed', NULL, NULL),
(12, 20, 11, 7, DATE_SUB(CURDATE(), INTERVAL 10 DAY), '09:30:00', 30, 'Follow-up', 'OB follow-up', NULL, 'Completed', NULL, NULL),
(13, 21, 5, 3, DATE_SUB(CURDATE(), INTERVAL 8 DAY), '08:00:00', 30, 'Emergency', 'Palpitations', 'Stabilized in ER', 'Completed', NULL, NULL),
(14, 22, 4, 2, DATE_SUB(CURDATE(), INTERVAL 6 DAY), '14:30:00', 25, 'Regular', 'Vaccination', NULL, 'Completed', NULL, NULL),
(15, 23, 1, 1, DATE_SUB(CURDATE(), INTERVAL 5 DAY), '13:15:00', 30, 'Regular', 'Lab review', NULL, 'Completed', NULL, NULL),
(16, 25, 7, 4, DATE_SUB(CURDATE(), INTERVAL 4 DAY), '10:45:00', 30, 'Regular', 'Back strain', NULL, 'Completed', NULL, NULL),
(17, 26, 10, 7, DATE_SUB(CURDATE(), INTERVAL 3 DAY), '11:00:00', 35, 'Follow-up', 'Oncology surveillance', NULL, 'Confirmed', NULL, NULL),
(18, 28, 11, 7, DATE_SUB(CURDATE(), INTERVAL 2 DAY), '15:00:00', 30, 'Regular', 'PCOS management', NULL, 'Scheduled', NULL, NULL),
(19, 29, 2, 1, DATE_SUB(CURDATE(), INTERVAL 1 DAY), '09:00:00', 45, 'Follow-up', 'Stroke rehab coordination', NULL, 'Completed', NULL, NULL),
(20, 30, 8, 5, CURDATE(), '07:30:00', 20, 'Emergency', 'Laceration repair', NULL, 'Confirmed', NULL, NULL),
(21, 31, 6, 3, CURDATE(), '10:00:00', 30, 'Regular', 'Stress test discussion', NULL, 'Scheduled', NULL, NULL),
(22, 32, 3, 2, CURDATE(), '11:30:00', 25, 'Regular', 'School physical', NULL, 'Scheduled', NULL, NULL),
(23, 33, 1, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:15:00', 30, 'Follow-up', 'Gout flare', NULL, 'Confirmed', NULL, NULL),
(24, 34, 12, 8, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '14:00:00', 40, 'Regular', 'CBT intake', NULL, 'Scheduled', NULL, NULL),
(25, 35, 2, 1, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '09:30:00', 30, 'Regular', 'New patient intake', NULL, 'Scheduled', NULL, NULL),
(26, 36, 10, 7, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '13:30:00', 30, 'Follow-up', 'Prenatal glucose', NULL, 'Confirmed', NULL, NULL),
(27, 37, 6, 3, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '08:45:00', 30, 'Follow-up', 'CHF meds', NULL, 'Scheduled', NULL, NULL),
(28, 38, 4, 2, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '15:45:00', 20, 'Regular', 'Asthma action plan', NULL, 'Scheduled', NULL, NULL),
(29, 39, 9, 6, DATE_ADD(CURDATE(), INTERVAL 4 DAY), '10:20:00', 25, 'Regular', 'Acne follow-up', NULL, 'Scheduled', NULL, NULL),
(30, 40, 7, 4, DATE_ADD(CURDATE(), INTERVAL 5 DAY), '11:00:00', 30, 'Follow-up', 'Post-op check', NULL, 'Scheduled', NULL, NULL),
(31, 5, 3, 2, DATE_SUB(CURDATE(), INTERVAL 50 DAY), '09:00:00', 30, 'Regular', 'Eczema', NULL, 'Completed', NULL, NULL),
(32, 8, 1, 1, DATE_SUB(CURDATE(), INTERVAL 55 DAY), '14:00:00', 30, 'Regular', 'GERD', NULL, 'Cancelled', DATE_SUB(NOW(), INTERVAL 54 DAY), 'Clinic closed holiday'),
(33, 9, 4, 2, DATE_SUB(CURDATE(), INTERVAL 7 DAY), '10:00:00', 25, 'Regular', 'Sports clearance', NULL, 'Completed', NULL, NULL),
(34, 12, 2, 1, DATE_SUB(CURDATE(), INTERVAL 14 DAY), '11:15:00', 30, 'Regular', 'Lipid panel review', NULL, 'No-Show', NULL, NULL),
(35, 13, 3, 2, DATE_SUB(CURDATE(), INTERVAL 9 DAY), '08:45:00', 30, 'Follow-up', 'Allergic rhinitis', NULL, 'Completed', NULL, NULL),
(36, 16, 7, 4, DATE_SUB(CURDATE(), INTERVAL 11 DAY), '13:30:00', 30, 'Regular', 'Ankle sprain', NULL, 'Completed', NULL, NULL),
(37, 19, 4, 2, DATE_SUB(CURDATE(), INTERVAL 16 DAY), '15:00:00', 25, 'Regular', 'Annual check', NULL, 'Completed', NULL, NULL),
(38, 24, 3, 2, DATE_SUB(CURDATE(), INTERVAL 13 DAY), '09:30:00', 20, 'Regular', 'Immunization', NULL, 'Completed', NULL, NULL),
(39, 27, 4, 2, DATE_SUB(CURDATE(), INTERVAL 21 DAY), '10:30:00', 30, 'Follow-up', 'ADHD meds', NULL, 'Completed', NULL, NULL),
(40, 4, 1, 1, DATE_SUB(CURDATE(), INTERVAL 17 DAY), '16:00:00', 30, 'Regular', 'College physical', NULL, 'Completed', NULL, NULL),
(41, 1, 2, 1, DATE_ADD(CURDATE(), INTERVAL 6 DAY), '09:00:00', 30, 'Follow-up', 'HTN follow-up', NULL, 'Scheduled', NULL, NULL),
(42, 2, 5, 3, DATE_ADD(CURDATE(), INTERVAL 7 DAY), '11:00:00', 45, 'Regular', 'Cardiology consult', NULL, 'Confirmed', NULL, NULL),
(43, 6, 8, 5, DATE_SUB(CURDATE(), INTERVAL 2 DAY), '06:00:00', 15, 'Emergency', 'Chest pain rule-out', 'Resolved', 'Completed', NULL, NULL),
(44, 15, 10, 7, DATE_SUB(CURDATE(), INTERVAL 60 DAY), '10:00:00', 30, 'Regular', 'First prenatal', NULL, 'Completed', NULL, NULL),
(45, 36, 11, 7, DATE_SUB(CURDATE(), INTERVAL 19 DAY), '14:00:00', 30, 'Regular', 'Routine OB', NULL, 'Completed', NULL, NULL),
(46, 17, 12, 8, DATE_SUB(CURDATE(), INTERVAL 44 DAY), '15:30:00', 45, 'Regular', 'Initial psych eval', NULL, 'Completed', NULL, NULL),
(47, 23, 2, 1, DATE_SUB(CURDATE(), INTERVAL 38 DAY), '13:00:00', 30, 'Regular', 'Metabolic panel', NULL, 'Completed', NULL, NULL),
(48, 29, 6, 3, DATE_SUB(CURDATE(), INTERVAL 31 DAY), '09:15:00', 30, 'Follow-up', 'Holter results', NULL, 'Completed', NULL, NULL),
(49, 33, 1, 1, DATE_SUB(CURDATE(), INTERVAL 26 DAY), '10:45:00', 30, 'Regular', 'Gout management', NULL, 'Completed', NULL, NULL),
(50, 40, 9, 6, DATE_SUB(CURDATE(), INTERVAL 23 DAY), '11:15:00', 25, 'Regular', 'Patch testing discussion', NULL, 'Completed', NULL, NULL),
(51, 22, 8, 5, DATE_SUB(CURDATE(), INTERVAL 1 DAY), '19:00:00', 20, 'Emergency', 'Minor burn', NULL, 'Completed', NULL, NULL),
(52, 35, 1, 1, DATE_ADD(CURDATE(), INTERVAL 10 DAY), '08:30:00', 30, 'Regular', 'New patient labs', NULL, 'Scheduled', NULL, NULL),
(53, 41, 15, 9, DATE_SUB(CURDATE(), INTERVAL 88 DAY), '09:15:00', 25, 'Regular', 'Diabetic eye screening', NULL, 'Completed', NULL, NULL),
(54, 42, 16, 10, DATE_SUB(CURDATE(), INTERVAL 85 DAY), '10:00:00', 30, 'Regular', 'Chronic sinusitis', NULL, 'Completed', NULL, NULL),
(55, 43, 17, 11, DATE_SUB(CURDATE(), INTERVAL 82 DAY), '11:30:00', 45, 'Follow-up', 'CKD stage 4 labs', NULL, 'Completed', NULL, NULL),
(56, 44, 18, 12, DATE_SUB(CURDATE(), INTERVAL 79 DAY), '14:00:00', 30, 'Regular', 'Asthma action plan', NULL, 'No-Show', NULL, NULL),
(57, 45, 19, 1, DATE_SUB(CURDATE(), INTERVAL 76 DAY), '08:45:00', 20, 'Regular', 'Pre-op clearance', NULL, 'Completed', NULL, NULL),
(58, 46, 20, 5, DATE_SUB(CURDATE(), INTERVAL 73 DAY), '22:15:00', 15, 'Emergency', 'Foreign body eye', NULL, 'Completed', NULL, NULL),
(59, 47, 11, 7, DATE_SUB(CURDATE(), INTERVAL 70 DAY), '13:20:00', 35, 'Follow-up', 'Second trimester visit', NULL, 'Completed', NULL, NULL),
(60, 48, 4, 2, DATE_SUB(CURDATE(), INTERVAL 67 DAY), '15:45:00', 25, 'Regular', 'ADHD medication check', NULL, 'Completed', NULL, NULL),
(61, 49, 12, 8, DATE_SUB(CURDATE(), INTERVAL 64 DAY), '16:30:00', 50, 'Regular', 'Medication adjustment lithium', NULL, 'Cancelled', DATE_SUB(NOW(), INTERVAL 63 DAY), 'Transport issue'),
(62, 50, 23, 3, DATE_SUB(CURDATE(), INTERVAL 61 DAY), '09:00:00', 40, 'Regular', 'New cardiology referral', NULL, 'Completed', NULL, NULL),
(63, 51, 1, 1, DATE_SUB(CURDATE(), INTERVAL 58 DAY), '12:10:00', 30, 'Follow-up', 'Vitamin D deficiency', NULL, 'Completed', NULL, NULL),
(64, 52, 7, 4, DATE_SUB(CURDATE(), INTERVAL 55 DAY), '07:00:00', 30, 'Emergency', 'Fracture clinic overflow', NULL, 'Completed', NULL, NULL),
(65, 53, 9, 6, DATE_SUB(CURDATE(), INTERVAL 52 DAY), '10:50:00', 20, 'Regular', 'Psoriasis biologics', NULL, 'Completed', NULL, NULL),
(66, 54, 6, 3, DATE_SUB(CURDATE(), INTERVAL 49 DAY), '11:40:00', 30, 'Follow-up', 'Post-cath follow-up', NULL, 'Completed', NULL, NULL),
(67, 55, 3, 2, DATE_SUB(CURDATE(), INTERVAL 46 DAY), '09:30:00', 20, 'Regular', 'Two-month well baby', NULL, 'Completed', NULL, NULL),
(68, 56, 2, 1, DATE_SUB(CURDATE(), INTERVAL 43 DAY), '13:00:00', 45, 'Regular', 'Polypharmacy review', NULL, 'Completed', NULL, NULL),
(69, 57, 10, 7, DATE_SUB(CURDATE(), INTERVAL 40 DAY), '14:15:00', 30, 'Regular', 'Contraception consult', NULL, 'Completed', NULL, NULL),
(70, 58, 10, 7, DATE_SUB(CURDATE(), INTERVAL 37 DAY), '08:20:00', 30, 'Follow-up', 'Early OB intake', NULL, 'Confirmed', NULL, NULL),
(71, 59, 17, 11, DATE_SUB(CURDATE(), INTERVAL 34 DAY), '15:00:00', 30, 'Regular', 'Proteinuria workup', NULL, 'Completed', NULL, NULL),
(72, 60, 5, 3, DATE_SUB(CURDATE(), INTERVAL 31 DAY), '10:05:00', 30, 'Emergency', 'Chest tightness', NULL, 'Completed', NULL, NULL),
(73, 61, 8, 5, DATE_SUB(CURDATE(), INTERVAL 28 DAY), '18:30:00', 25, 'Emergency', 'Anaphylaxis observation', NULL, 'Completed', NULL, NULL),
(74, 62, 18, 12, DATE_SUB(CURDATE(), INTERVAL 25 DAY), '11:15:00', 30, 'Follow-up', 'Home O2 titration', NULL, 'Completed', NULL, NULL),
(75, 63, 23, 1, DATE_SUB(CURDATE(), INTERVAL 22 DAY), '09:50:00', 30, 'Regular', 'Pre-dialysis education', NULL, 'Completed', NULL, NULL),
(76, 64, 11, 7, DATE_SUB(CURDATE(), INTERVAL 19 DAY), '16:00:00', 25, 'Regular', 'GYN ultrasound discuss', NULL, 'No-Show', NULL, NULL),
(77, 65, 7, 4, DATE_SUB(CURDATE(), INTERVAL 16 DAY), '12:30:00', 30, 'Follow-up', 'Meniscus post-PT', NULL, 'Completed', NULL, NULL),
(78, 66, 2, 1, DATE_SUB(CURDATE(), INTERVAL 13 DAY), '14:45:00', 30, 'Regular', 'Lipid recheck', NULL, 'Completed', NULL, NULL),
(79, 67, 12, 8, DATE_SUB(CURDATE(), INTERVAL 10 DAY), '13:30:00', 60, 'Regular', 'ECT coordination meeting', NULL, 'Scheduled', NULL, NULL),
(80, 68, 12, 8, DATE_SUB(CURDATE(), INTERVAL 7 DAY), '17:00:00', 45, 'Follow-up', 'Group therapy intake', NULL, 'Completed', NULL, NULL),
(81, 69, 4, 2, DATE_SUB(CURDATE(), INTERVAL 4 DAY), '08:00:00', 20, 'Regular', 'Febrile illness follow-up', NULL, 'Completed', NULL, NULL),
(82, 70, 23, 3, CURDATE(), '07:15:00', 15, 'Follow-up', 'Quick BP check', NULL, 'Confirmed', NULL, NULL),
(83, 71, 1, 1, CURDATE(), '12:00:00', 30, 'Regular', 'Warfarin bridging plan', NULL, 'Scheduled', NULL, NULL),
(84, 72, 16, 10, CURDATE(), '15:30:00', 25, 'Regular', 'Hearing test results', NULL, 'Scheduled', NULL, NULL),
(85, 73, 17, 11, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '09:40:00', 30, 'Follow-up', 'Creatinine trend', NULL, 'Confirmed', NULL, NULL),
(86, 74, 18, 12, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '11:10:00', 40, 'Regular', 'PFT review', NULL, 'Scheduled', NULL, NULL),
(87, 75, 15, 9, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '08:30:00', 20, 'Regular', 'Strabismus eval', NULL, 'Scheduled', NULL, NULL),
(88, 76, 18, 12, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '14:20:00', 30, 'Follow-up', 'CPAP compliance', NULL, 'Confirmed', NULL, NULL),
(89, 77, 10, 7, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '10:25:00', 35, 'Regular', 'IUD placement discuss', NULL, 'Scheduled', NULL, NULL),
(90, 78, 16, 10, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '16:45:00', 20, 'Regular', 'Tinnitus eval', NULL, 'Scheduled', NULL, NULL),
(91, 79, 7, 4, DATE_ADD(CURDATE(), INTERVAL 4 DAY), '09:05:00', 30, 'Regular', 'Fall risk bone clinic', NULL, 'Scheduled', NULL, NULL),
(92, 80, 8, 5, DATE_ADD(CURDATE(), INTERVAL 4 DAY), '20:00:00', 15, 'Emergency', 'Workplace chemical splash', NULL, 'Scheduled', NULL, NULL),
(93, 41, 22, 9, DATE_SUB(CURDATE(), INTERVAL 92 DAY), '13:15:00', 30, 'Regular', 'Glaucoma field test', NULL, 'Completed', NULL, NULL),
(94, 42, 21, 6, DATE_SUB(CURDATE(), INTERVAL 89 DAY), '11:00:00', 25, 'Regular', 'Melanoma surveillance', NULL, 'Completed', NULL, NULL),
(95, 43, 5, 3, DATE_SUB(CURDATE(), INTERVAL 15 DAY), '08:30:00', 60, 'Follow-up', 'AFib cardioversion plan', NULL, 'Completed', NULL, NULL),
(96, 44, 23, 1, DATE_SUB(CURDATE(), INTERVAL 12 DAY), '15:15:00', 30, 'Regular', 'Dual clinic IM slot', NULL, 'Completed', NULL, NULL),
(97, 45, 14, 3, DATE_SUB(CURDATE(), INTERVAL 99 DAY), '10:30:00', 30, 'Regular', 'Cardiology before leave', NULL, 'Completed', NULL, NULL),
(98, 46, 19, 1, DATE_ADD(CURDATE(), INTERVAL 5 DAY), '06:30:00', 15, 'Emergency', 'Ward consult overflow', NULL, 'Scheduled', NULL, NULL),
(99, 47, 6, 3, DATE_ADD(CURDATE(), INTERVAL 6 DAY), '12:45:00', 30, 'Follow-up', 'Stent anniversary visit', NULL, 'Confirmed', NULL, NULL),
(100, 48, 3, 2, DATE_ADD(CURDATE(), INTERVAL 7 DAY), '14:00:00', 25, 'Regular', 'Travel vaccines', NULL, 'Scheduled', NULL, NULL),
(101, 49, 9, 6, DATE_ADD(CURDATE(), INTERVAL 8 DAY), '09:20:00', 30, 'Regular', 'Biologic infusion scheduling', NULL, 'Scheduled', NULL, NULL),
(102, 50, 20, 5, DATE_ADD(CURDATE(), INTERVAL 9 DAY), '23:30:00', 20, 'Emergency', 'Night minor trauma', NULL, 'Scheduled', NULL, NULL),
(103, 51, 15, 9, DATE_ADD(CURDATE(), INTERVAL 11 DAY), '13:00:00', 25, 'Follow-up', 'Post-cataract day 1', NULL, 'Scheduled', NULL, NULL),
(104, 52, 4, 2, DATE_ADD(CURDATE(), INTERVAL 12 DAY), '08:15:00', 30, 'Regular', 'Scoliosis brace check', NULL, 'Scheduled', NULL, NULL),
(105, 53, 17, 11, DATE_ADD(CURDATE(), INTERVAL 13 DAY), '11:50:00', 45, 'Regular', 'Renal transplant listing talk', NULL, 'Scheduled', NULL, NULL),
(106, 54, 18, 12, DATE_ADD(CURDATE(), INTERVAL 14 DAY), '15:05:00', 30, 'Follow-up', 'ILD prednisone taper', NULL, 'Scheduled', NULL, NULL),
(107, 55, 3, 2, DATE_ADD(CURDATE(), INTERVAL 15 DAY), '09:00:00', 20, 'Regular', 'Four-month vaccines', NULL, 'Confirmed', NULL, NULL),
(108, 56, 2, 1, DATE_ADD(CURDATE(), INTERVAL 16 DAY), '10:40:00', 45, 'Regular', 'Geriatric assessment', NULL, 'Scheduled', NULL, NULL),
(109, 57, 12, 8, DATE_ADD(CURDATE(), INTERVAL 17 DAY), '16:15:00', 50, 'Regular', 'DBT skills group screen', NULL, 'Scheduled', NULL, NULL),
(110, 58, 11, 7, DATE_ADD(CURDATE(), INTERVAL 18 DAY), '08:50:00', 40, 'Follow-up', 'Second trimester labs', NULL, 'Scheduled', NULL, NULL),
(111, 59, 1, 1, DATE_SUB(CURDATE(), INTERVAL 2 DAY), '17:30:00', 30, 'Regular', 'After-work clinic slot', NULL, 'Completed', NULL, NULL),
(112, 60, 5, 3, DATE_SUB(CURDATE(), INTERVAL 1 DAY), '12:20:00', 30, 'Follow-up', 'T1D pump settings', NULL, 'Completed', NULL, NULL),
(113, 61, 14, 3, DATE_SUB(CURDATE(), INTERVAL 200 DAY), '09:00:00', 30, 'Regular', 'Historical visit before leave', NULL, 'Completed', NULL, NULL),
(114, 62, 23, 3, DATE_SUB(CURDATE(), INTERVAL 95 DAY), '14:30:00', 30, 'Regular', 'STEMI survivor clinic', NULL, 'Completed', NULL, NULL),
(115, 63, 17, 11, DATE_SUB(CURDATE(), INTERVAL 18 DAY), '08:00:00', 30, 'Emergency', 'Hyperkalemia ED follow', NULL, 'Completed', NULL, NULL),
(116, 64, 10, 7, DATE_SUB(CURDATE(), INTERVAL 9 DAY), '13:45:00', 25, 'Regular', 'Pap follow-up', NULL, 'Completed', NULL, NULL),
(117, 65, 7, 4, DATE_SUB(CURDATE(), INTERVAL 6 DAY), '11:05:00', 30, 'Follow-up', 'Knee injection', NULL, 'Completed', NULL, NULL),
(118, 66, 8, 5, DATE_SUB(CURDATE(), INTERVAL 3 DAY), '19:45:00', 15, 'Emergency', 'Migraine IV protocol', NULL, 'Completed', NULL, NULL);

-- -----------------------------------------------------------------------------
-- Queue: active (served_at IS NULL, removed_at IS NULL), served history, removed
-- -----------------------------------------------------------------------------
INSERT INTO queue_entries (queue_entry_id, patient_id, specialization_id, status, position, joined_at, served_at, removed_at, removal_reason, estimated_wait_time) VALUES
-- Active waiting (QueueService active_only uses served_at/removed_at)
(1, 2, 1, 1, 1, DATE_SUB(NOW(), INTERVAL 25 MINUTE), NULL, NULL, NULL, 20),
(2, 6, 3, 2, 1, DATE_SUB(NOW(), INTERVAL 40 MINUTE), NULL, NULL, NULL, 15),
(3, 10, 1, 0, 2, DATE_SUB(NOW(), INTERVAL 50 MINUTE), NULL, NULL, NULL, 35),
(4, 14, 3, 0, 2, DATE_SUB(NOW(), INTERVAL 55 MINUTE), NULL, NULL, NULL, 40),
(5, 5, 2, 0, 1, DATE_SUB(NOW(), INTERVAL 15 MINUTE), NULL, NULL, NULL, 25),
(6, 13, 2, 1, 2, DATE_SUB(NOW(), INTERVAL 20 MINUTE), NULL, NULL, NULL, 30),
(7, 21, 3, 0, 3, DATE_SUB(NOW(), INTERVAL 10 MINUTE), NULL, NULL, NULL, 45),
(8, 8, 5, 2, 1, DATE_SUB(NOW(), INTERVAL 5 MINUTE), NULL, NULL, NULL, 10),
(9, 15, 7, 0, 1, DATE_SUB(NOW(), INTERVAL 30 MINUTE), NULL, NULL, NULL, 20),
(10, 17, 8, 0, 1, DATE_SUB(NOW(), INTERVAL 12 MINUTE), NULL, NULL, NULL, 30),
(11, 25, 4, 0, 1, DATE_SUB(NOW(), INTERVAL 8 MINUTE), NULL, NULL, NULL, 25),
(12, 34, 6, 1, 1, DATE_SUB(NOW(), INTERVAL 18 MINUTE), NULL, NULL, NULL, 15),
-- Served (historical — status 3 + served_at set)
(13, 3, 1, 3, 1, DATE_SUB(NOW(), INTERVAL 3 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 3 DAY), INTERVAL 45 MINUTE), NULL, NULL, NULL),
(14, 7, 2, 3, 1, DATE_SUB(NOW(), INTERVAL 3 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 3 DAY), INTERVAL 30 MINUTE), NULL, NULL, NULL),
(15, 11, 1, 3, 2, DATE_SUB(NOW(), INTERVAL 2 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 2 DAY), INTERVAL 20 MINUTE), NULL, NULL, NULL),
(16, 12, 1, 3, 1, DATE_SUB(NOW(), INTERVAL 5 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 5 DAY), INTERVAL 60 MINUTE), NULL, NULL, NULL),
(17, 16, 4, 3, 1, DATE_SUB(NOW(), INTERVAL 4 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 4 DAY), INTERVAL 25 MINUTE), NULL, NULL, NULL),
(18, 18, 4, 3, 2, DATE_SUB(NOW(), INTERVAL 6 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 6 DAY), INTERVAL 40 MINUTE), NULL, NULL, NULL),
(19, 19, 2, 3, 1, DATE_SUB(NOW(), INTERVAL 7 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 7 DAY), INTERVAL 35 MINUTE), NULL, NULL, NULL),
(20, 20, 7, 3, 1, DATE_SUB(NOW(), INTERVAL 8 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 8 DAY), INTERVAL 50 MINUTE), NULL, NULL, NULL),
(21, 23, 5, 3, 1, DATE_SUB(NOW(), INTERVAL 1 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 1 DAY), INTERVAL 90 MINUTE), NULL, NULL, NULL),
(22, 26, 7, 3, 1, DATE_SUB(NOW(), INTERVAL 9 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 9 DAY), INTERVAL 55 MINUTE), NULL, NULL, NULL),
(23, 28, 7, 3, 2, DATE_SUB(NOW(), INTERVAL 10 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 10 DAY), INTERVAL 30 MINUTE), NULL, NULL, NULL),
(24, 29, 3, 3, 1, DATE_SUB(NOW(), INTERVAL 11 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 11 DAY), INTERVAL 70 MINUTE), NULL, NULL, NULL),
(25, 30, 1, 3, 3, DATE_SUB(NOW(), INTERVAL 12 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 12 DAY), INTERVAL 15 MINUTE), NULL, NULL, NULL),
(26, 31, 4, 3, 2, DATE_SUB(NOW(), INTERVAL 14 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 14 DAY), INTERVAL 22 MINUTE), NULL, NULL, NULL),
(27, 33, 1, 3, 4, DATE_SUB(NOW(), INTERVAL 15 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 15 DAY), INTERVAL 18 MINUTE), NULL, NULL, NULL),
(28, 37, 3, 3, 3, DATE_SUB(NOW(), INTERVAL 16 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 16 DAY), INTERVAL 120 MINUTE), NULL, NULL, NULL),
(29, 39, 1, 3, 5, DATE_SUB(NOW(), INTERVAL 18 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 18 DAY), INTERVAL 12 MINUTE), NULL, NULL, NULL),
(30, 40, 6, 3, 1, DATE_SUB(NOW(), INTERVAL 20 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 20 DAY), INTERVAL 28 MINUTE), NULL, NULL, NULL),
-- Removed without serve (left voluntarily / error)
(31, 4, 2, 0, NULL, DATE_SUB(NOW(), INTERVAL 1 DAY), NULL, DATE_ADD(DATE_SUB(NOW(), INTERVAL 1 DAY), INTERVAL 20 MINUTE), 'Patient left before intake', 20),
(32, 9, 5, 1, NULL, DATE_SUB(NOW(), INTERVAL 2 DAY), NULL, DATE_ADD(DATE_SUB(NOW(), INTERVAL 2 DAY), INTERVAL 10 MINUTE), 'Referred to inpatient', 10),
(33, 22, 8, 0, NULL, DATE_SUB(NOW(), INTERVAL 4 DAY), NULL, DATE_ADD(DATE_SUB(NOW(), INTERVAL 4 DAY), INTERVAL 5 MINUTE), 'Duplicate queue entry', 30),
(34, 27, 2, 2, NULL, DATE_SUB(NOW(), INTERVAL 6 DAY), NULL, DATE_ADD(DATE_SUB(NOW(), INTERVAL 6 DAY), INTERVAL 15 MINUTE), 'Parent cancelled', 15),
(35, 38, 2, 0, NULL, DATE_SUB(NOW(), INTERVAL 8 DAY), NULL, DATE_ADD(DATE_SUB(NOW(), INTERVAL 8 DAY), INTERVAL 8 MINUTE), 'Walk-in redirected', 25),
(36, 41, 9, 0, 1, DATE_SUB(NOW(), INTERVAL 22 MINUTE), NULL, NULL, NULL, 18),
(37, 43, 11, 2, 1, DATE_SUB(NOW(), INTERVAL 33 MINUTE), NULL, NULL, NULL, 25),
(38, 46, 12, 0, 1, DATE_SUB(NOW(), INTERVAL 11 MINUTE), NULL, NULL, NULL, 20),
(39, 50, 10, 1, 1, DATE_SUB(NOW(), INTERVAL 7 MINUTE), NULL, NULL, NULL, 22),
(40, 55, 2, 0, 3, DATE_SUB(NOW(), INTERVAL 28 MINUTE), NULL, NULL, NULL, 40),
(41, 59, 6, 0, 2, DATE_SUB(NOW(), INTERVAL 19 MINUTE), NULL, NULL, NULL, 28),
(42, 61, 1, 0, 6, DATE_SUB(NOW(), INTERVAL 14 MINUTE), NULL, NULL, NULL, 50),
(43, 63, 3, 1, 4, DATE_SUB(NOW(), INTERVAL 9 MINUTE), NULL, NULL, NULL, 35),
(44, 66, 7, 0, 2, DATE_SUB(NOW(), INTERVAL 16 MINUTE), NULL, NULL, NULL, 24),
(45, 71, 1, 2, 7, DATE_SUB(NOW(), INTERVAL 6 MINUTE), NULL, NULL, NULL, 15),
(46, 73, 11, 0, 2, DATE_SUB(NOW(), INTERVAL 4 MINUTE), NULL, NULL, NULL, 30),
(47, 76, 12, 0, 2, DATE_SUB(NOW(), INTERVAL 13 MINUTE), NULL, NULL, NULL, 22),
(48, 78, 10, 0, 2, DATE_SUB(NOW(), INTERVAL 21 MINUTE), NULL, NULL, NULL, 26),
(49, 42, 10, 3, 1, DATE_SUB(NOW(), INTERVAL 13 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 13 DAY), INTERVAL 40 MINUTE), NULL, NULL, NULL),
(50, 44, 2, 3, 1, DATE_SUB(NOW(), INTERVAL 14 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 14 DAY), INTERVAL 25 MINUTE), NULL, NULL, NULL),
(51, 47, 7, 3, 1, DATE_SUB(NOW(), INTERVAL 21 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 21 DAY), INTERVAL 55 MINUTE), NULL, NULL, NULL),
(52, 52, 4, 3, 1, DATE_SUB(NOW(), INTERVAL 22 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 22 DAY), INTERVAL 18 MINUTE), NULL, NULL, NULL),
(53, 54, 3, 3, 1, DATE_SUB(NOW(), INTERVAL 23 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 23 DAY), INTERVAL 90 MINUTE), NULL, NULL, NULL),
(54, 60, 5, 3, 1, DATE_SUB(NOW(), INTERVAL 24 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 24 DAY), INTERVAL 12 MINUTE), NULL, NULL, NULL),
(55, 68, 8, 3, 1, DATE_SUB(NOW(), INTERVAL 25 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 25 DAY), INTERVAL 48 MINUTE), NULL, NULL, NULL),
(56, 74, 11, 3, 1, DATE_SUB(NOW(), INTERVAL 26 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 26 DAY), INTERVAL 33 MINUTE), NULL, NULL, NULL),
(57, 77, 7, 3, 1, DATE_SUB(NOW(), INTERVAL 27 DAY), DATE_ADD(DATE_SUB(NOW(), INTERVAL 27 DAY), INTERVAL 28 MINUTE), NULL, NULL, NULL),
(58, 45, 5, 0, NULL, DATE_SUB(NOW(), INTERVAL 3 DAY), NULL, DATE_ADD(DATE_SUB(NOW(), INTERVAL 3 DAY), INTERVAL 12 MINUTE), 'Treated and discharged from ER', 10),
(59, 48, 2, 1, NULL, DATE_SUB(NOW(), INTERVAL 5 DAY), NULL, DATE_ADD(DATE_SUB(NOW(), INTERVAL 5 DAY), INTERVAL 8 MINUTE), 'Walk-in redirected to Peds urgent', 15),
(60, 58, 7, 2, NULL, DATE_SUB(NOW(), INTERVAL 2 DAY), NULL, DATE_ADD(DATE_SUB(NOW(), INTERVAL 2 DAY), INTERVAL 6 MINUTE), 'OB triage to labor and delivery', 5),
(61, 69, 2, 0, 4, DATE_SUB(NOW(), INTERVAL 17 MINUTE), NULL, NULL, NULL, 32),
(62, 80, 5, 0, 2, DATE_SUB(NOW(), INTERVAL 2 MINUTE), NULL, NULL, NULL, 8);

-- -----------------------------------------------------------------------------
-- Users + audit (optional tables; aligned with schema enums)
-- -----------------------------------------------------------------------------
INSERT INTO users (user_id, username, password_hash, role, full_name, email, phone_number, is_active, last_login) VALUES
(1, 'admin', SHA2('demo123', 256), 'Administrator', 'System Administrator', 'admin@live.com', '+63-917-300-0001', 1, DATE_SUB(NOW(), INTERVAL 1 DAY)),
(2, 'reception', SHA2('demo123', 256), 'Receptionist', 'Rhea Gonzales', 'reception@aol.com', '+63-917-300-0002', 1, DATE_SUB(NOW(), INTERVAL 2 HOUR)),
(3, 'nurse.mina', SHA2('demo123', 256), 'Nurse', 'Mina Del Rosario', 'nurse@gmail.com', '+63-917-300-0003', 1, NULL),
(4, 'dr.ruiz', SHA2('demo123', 256), 'Doctor', 'Elena Ruiz', 'e.ruiz@gmail.com', '+63-917-100-0001', 1, DATE_SUB(NOW(), INTERVAL 3 DAY)),
(5, 'viewer', SHA2('demo123', 256), 'Viewer', 'Audit Readonly', 'viewer@yahoo.com', NULL, 1, NULL),
(6, 'dr.kapoor', SHA2('demo123', 256), 'Doctor', 'Priya Kapoor', 'p.kapoor@yahoo.com', '+63-917-100-0019', 1, DATE_SUB(NOW(), INTERVAL 4 HOUR)),
(7, 'billing.rob', SHA2('demo123', 256), 'Receptionist', 'Roberto Salcedo', 'billing@hotmail.com', '+63-917-300-0004', 1, NULL),
(8, 'jmo.archived', SHA2('demo123', 256), 'Nurse', 'Janelle Morales', 'j.morales@proton.me', '+63-917-300-0005', 0, DATE_SUB(NOW(), INTERVAL 400 DAY)),
(9, 'dr.huang', SHA2('demo123', 256), 'Doctor', 'Mei-Lin Huang', 'm.huang@gmail.com', '+63-917-100-0017', 1, DATE_SUB(NOW(), INTERVAL 12 HOUR)),
(10, 'auditor.ext', SHA2('demo123', 256), 'Viewer', 'External QA Partner', 'qa.partner@aol.com', NULL, 1, NULL);

INSERT INTO audit_logs (log_id, user_id, action, table_name, record_id, old_values, new_values, ip_address) VALUES
(1, 2, 'INSERT', 'patients', 35, NULL, '{"full_name":"Ian Chua"}', '127.0.0.1'),
(2, 2, 'UPDATE', 'appointments', 20, '{"status":"Scheduled"}', '{"status":"Confirmed"}', '127.0.0.1'),
(3, 1, 'DELETE', 'queue_entries', 31, NULL, NULL, '192.168.1.10'),
(4, 4, 'UPDATE', 'queue_entries', 2, NULL, '{"status":2}', '10.0.0.5'),
(5, 2, 'INSERT', 'appointments', 52, NULL, '{"patient_id":35}', '127.0.0.1'),
(6, 1, 'UPDATE', 'users', 5, NULL, '{"is_active":1}', '127.0.0.1'),
(7, 3, 'INSERT', 'queue_entries', 8, NULL, '{"specialization_id":5}', '172.16.0.2'),
(8, 2, 'UPDATE', 'patients', 3, NULL, '{"status":2}', '127.0.0.1'),
(9, 6, 'INSERT', 'patients', 72, NULL, '{"cohort":"expansion"}', '10.20.30.40'),
(10, 7, 'UPDATE', 'appointments', 100, NULL, '{"status":"Scheduled"}', '192.168.50.1'),
(11, 9, 'INSERT', 'appointments', 110, NULL, '{"specialization_id":7}', '172.16.88.2'),
(12, 1, 'DELETE', 'audit_logs', 3, NULL, NULL, '127.0.0.1'),
(13, 4, 'UPDATE', 'doctors', 21, NULL, '{"status":"Inactive"}', '10.0.0.12'),
(14, 6, 'INSERT', 'queue_entries', 48, NULL, '{"spec":10}', '192.168.1.201'),
(15, 10, 'INSERT', 'specializations', 12, NULL, '{"name":"Pulmonology"}', '203.0.113.9'),
(16, 2, 'UPDATE', 'users', 8, '{"is_active":1}', '{"is_active":0}', '127.0.0.1'),
(17, 9, 'INSERT', 'doctor_specializations', 23, NULL, '{"doctor_id":23}', '10.10.10.10'),
(18, 3, 'UPDATE', 'queue_entries', 62, NULL, '{"estimated_wait_time":8}', '172.31.0.5'),
(19, 7, 'INSERT', 'patients', 80, NULL, '{"source":"walk_in"}', '192.168.0.77'),
(20, 1, 'UPDATE', 'specializations', 13, NULL, '{"is_active":0}', '127.0.0.1');

-- Reset AUTO_INCREMENT to next free id (optional safety after explicit ids)
ALTER TABLE specializations AUTO_INCREMENT = 14;
ALTER TABLE doctors AUTO_INCREMENT = 24;
ALTER TABLE patients AUTO_INCREMENT = 81;
ALTER TABLE appointments AUTO_INCREMENT = 119;
ALTER TABLE queue_entries AUTO_INCREMENT = 63;
ALTER TABLE users AUTO_INCREMENT = 11;
ALTER TABLE audit_logs AUTO_INCREMENT = 21;

Intelligent Hospital Management and Queueing System (HMS)

Advanced Object-Oriented Programming
















Albert James Mangcao
Rommel Palermo
Rhea Leigh Talavera
Ronald Amparo
MarkDave Fetalino
Master in Information Technology
Pamantasan ng lungsod ng Muntinlupa
A.Y. 2025 - 2026
 
Abstract
The Intelligent Hospital Management System (HMS) addresses the critical challenge of patient congestion and administrative inefficiency in healthcare facilities. This project proposes a web-based solution built with Python and Streamlit, utilizing a Service-Oriented Architecture (SOA) to decouple business logic from the presentation layer. Key Object-Oriented Programming (OOP) concepts, including Dependency Injection, the Strategy Pattern for database management, and SOLID principles, are applied to ensure system scalability and maintainability. The system features automated priority-based queueing, conflict-aware appointment scheduling, and real-time data visualization for hospital administrators. The final outcome is a robust, responsive application that reduces manual data entry errors and optimizes patient throughput.
Technical execution prioritizes modularity through the implementation of a Service-Oriented Architecture (SOA), ensuring a strict separation between domain logic and the reactive user interface. Advanced OOP principles such as Dependency Injection (DI) are utilized to facilitate database-agnostic operations, allowing the system to toggle between MySQL and SQLite via a Strategy-like selection at the database package boundary (`src/database/__init__.py` chooses `MySQLDatabaseManager` or the SQLite `DatabaseManager` from configuration) without altering service-layer code. Queue ordering is implemented in the data layer as **priority first, then arrival time**: active entries are sorted by `status` descending (Super-Urgent, Urgent, Normal) and `joined_at` ascending, so ties within the same priority level are handled fairly. This backend is further reinforced by SOLID-oriented separation of services, keeping domain operations distinct from persistence details and supporting clearer testing of business logic.
Beyond patient tracking, the system integrates data processing through the Pandas library and charts using Streamlit’s built-in visualization components (for example, `st.bar_chart`) so administrators can see utilization and throughput summaries on the Dashboard. Report performance depends on the database, hardware, and record volume; the implementation relies on SQL aggregation and Pandas rather than a separate charting library. By reducing administrative overhead and blocking overlapping bookings through an automated conflict check, the HMS serves as a scalable blueprint for modernizing healthcare infrastructure. Future iterations are planned to include a patient-facing portal for remote registration and an AI-driven predictive model for real-time wait-time estimations.
Table of Contents
I. Title Page
II. Abstract
III. Table of Contents
IV. Introduction
    4.1 Background of the Problem
    4.2 Motivation and Significance
    4.3 Objectives of the System
    4.4 Scope and Limitations
V. Review of Related Systems or Literature
VI. System Overview
    6.1 Purpose and Context
    6.2 Target Users and Responsibilities
    6.3 Major Functional Subsystems
    6.4 User Interface Organization
    6.5 Deployment and Runtime Characteristics
    6.6 Relationship to Architecture (Preview)
VII. System Architecture and Design
    7.1 Architectural Overview
    7.2 Object-Oriented Design
    7.3 UML Diagrams
VIII. Advanced Object-Oriented Concepts Applied
IX. Implementation Details
    Language, frameworks, and module organization
    Key Algorithm (priority ordering and queue dispatching)
X. Testing and Validation
    Unit, integration, and edge-case coverage
XI. Results and Discussion
    11.1 Outcomes Relative to Project Objectives
    11.2 Observed Behavior of the User Interface
    11.3 Performance, Reporting, and Evaluation Limits
    11.4 Discussion: Design Trade-offs and Lessons Learned
XII. Conclusion and Future Enhancements
    12.1 Summary Conclusion
    12.2 Principal Contributions
    12.3 Future Enhancements
XIII. References
XIV. Appendices (User Manual & Feature Flows)
    14.1 User Manual & System Navigation
 
IV. Introduction
4.1 Background of the Problem
Traditional hospital management often relies on manual record-keeping or fragmented digital systems that lack integrated queueing logic. This results in long wait times, scheduling conflicts, and poor data visibility for management.
4.2 Motivation and Significance
As healthcare demands grow, software must be designed with "Advanced OOP" principles to handle complexity. This project is significant because it demonstrates how modular code can solve real-world logistical bottlenecks.
4.3 Objectives of the System
●	To automate patient registration and prioritization.
●	To implement a conflict-detection algorithm for doctor appointments.
●	To provide a modular database layer supporting both MySQL and SQLite.
4.4 Scope and Limitations
The scope includes Patient, Doctor, Specialization, Queue, and Appointment management. Limitations include the lack of a built-in billing module and external insurance API integration in the current version.
V. Review of Related Systems or Literature
Reinforcement Learning in Triage: Menshawi et al. (2025) proposed a novel machine learning-based triage framework for emergency departments, published in Expert Systems (Wiley). Their system classifies patients by severity and urgency using supervised learning, achieving measurably shorter wait times compared to rule-based triage. This validates the HMS priority queue design (Super-Urgent, Urgent, Normal) implemented in this project.
Predictive Workload Management in Clinical Triage: Saghafian et al. (2020) examined workload management strategies in telemedical physician triage, published in Management Science. Their optimization model, applied in knowledge-intensive service queues, demonstrates that predictive workload-balancing reduces physician overload and patient wait times. This informs the HMS priority-first, arrival-time-second queue ordering used in this project.
Hybrid Optimization Models (ANN-PSO): Research by Tshiamala & Tartibu (2025) introduced a hybrid Artificial Neural Network-Particle Swarm Optimization (ANN-PSO) model for a telemedicine queuing system. Published in Applied Sciences (MDPI), their model achieves an R² greater than 0.90 in predicting queue intensity, outperforming classical queuing theory. This validates the use of data-driven approaches over manual scheduling in systems like this HMS.
Virtual Queueing Systems: Lee (2020) at Universiti Malaysia Sarawak (UNIMAS) developed the i-Queue system as an undergraduate final-year project. The system enables patients to join a hospital queue remotely via mobile devices, effectively eliminating the physical lobby bottleneck. This virtual queueing concept directly parallels the HMS's priority-based queue where patients are enrolled without requiring physical presence at a counter.
IoT-Cloud Integration: Fawzy et al. (2022) introduced an IoT-based resource utilization framework using Three-Phase Data Fusion (TPRUDF) for smart environments, published in Internet of Things (Elsevier). The framework integrates heterogeneous IoT sensor streams into a unified data layer to support real-time decision-making. This informs future HMS extensions that may incorporate patient vital sign monitoring into priority queue decisions.
Predictive Appointment Scheduling: Jalali & Belkic (2024) proposed an AI-based appointment system specifically designed to reduce the financial and operational impact of patient no-shows. Published in Healthcare (MDPI), their model uses predictive analytics to identify high-risk no-show slots and apply overbooking strategies accordingly. This directly relates to the conflict-aware appointment scheduling and status lifecycle management implemented in this HMS.
Vertical Patient Flow (VPP): Hodgson et al. (2025) (Mayo Clinic Arizona researchers) introduced an AI-assisted Vertical Patient Processing (VPP) model for emergency departments, published in the Journal of Personalized Medicine (MDPI). The system classifies patients who can be treated without a bed into a separate queue, increasing overall ER throughput. This multi-queue segmentation concept is reflected in the HMS's status-differentiated queue (Super-Urgent, Urgent, Normal).
Automated Triage via AI-Assisted Intake: Yi et al. (2025) conducted a systematic review of prospective studies on AI-assisted triage in the emergency department, published in the Journal of Nursing Scholarship. They found that AI triage tools consistently improve patient categorization accuracy and reduce the burden on nursing staff at the point of intake. This supports the HMS's automated priority assignment logic, which removes subjective manual sorting.
Standardizing Interoperability (HL7 FHIR): Lehne et al. (2019) argued that digital medicine fundamentally depends on interoperability, published in npj Digital Medicine (Nature). Without open data standards such as HL7 FHIR, health systems remain siloed and unable to share patient records across providers. While the current HMS uses a local relational database, this literature motivates future integration with standardized health data APIs to enable cross-facility record access.
Blockchain for Record Integrity: Alotaibi & Roussinov (2024) proposed a secure blockchain framework for healthcare records management, published in Cell Reports Medicine (Elsevier). Their framework ensures that patient medical records and transaction logs are tamper-proof and auditable, preventing data manipulation in billing and insurance workflows. This supports the data integrity requirements of the HMS, particularly for appointment history and patient records.
PhilHealth Integration & Automation: The Philippine Health Insurance Corporation (2024) maintains the PhilHealth eClaims System, an online portal enabling member eligibility verification and real-time claim submissions by accredited health facilities. Integrating an HMS with this system speeds up the discharge process by automating PhilHealth benefit computations that previously required hours of manual paperwork. The current HMS architecture, built with a service-oriented design, is structured to accommodate such external API integrations in future iterations.
The Universal Health Care (UHC) Law Mandate: The Republic of the Philippines (2019) enacted Republic Act No. 11223 (Universal Health Care Act), which mandates all public health facilities to adopt digital health systems and integrate with national health databases. This legislation is the primary policy driver for "Smart Hospital" initiatives in the country, requiring facilities to manage the influx of patients covered under universal coverage. This HMS directly responds to that mandate by automating patient registration, queueing, and appointment management.
Barriers to Digital Health Adoption in the Philippines: Lau et al. (2025) conducted a mixed-methods pilot study on implementing electronic health records in Philippine primary care settings, published in JMIR Medical Informatics. Their findings reveal persistent barriers including limited digital infrastructure, staff training gaps, and connectivity constraints in local health units. This context underscores the design choice to support both MySQL (networked) and SQLite (offline-capable) backends in this HMS, ensuring functional continuity across varying infrastructure conditions.
Community Health Information Tracking System (CHITS): Marcelo et al. (2013) documented the Community Health Information Tracking System (CHITS) over eight years of implementation, published in Acta Medica Philippina. As a pioneer electronic medical record system in the Philippines deployed in public health centers, CHITS established the benchmark for modular, locally-deployable health information systems. The HMS follows this same design principle — a modular, service-separated architecture that can incrementally add features such as automated reporting or AI-driven forecasting.
User Experience (UX) for Filipino Patients: Idian (2025) developed a lying-in clinic information management system for Buhi municipality in Camarines Sur, published in the International Journal of Advanced Research (IJAR). The study found that SMS-based queue notifications and simple form-based interfaces are more effective for the local demographic than complex app-driven systems, due to device hardware limitations. This supports the HMS's use of Streamlit — a lightweight, browser-based interface requiring no native app installation on the patient or admin side.
Predictive Analytics for Length of Stay (LOS): Lim et al. (2023) examined the prevalence and predictors of prolonged length of stay among patients in a tertiary government hospital in Manila, published in BMC Health Services Research. Their findings identify key clinical and administrative factors that drive extended inpatient stays, allowing bed management queues to be optimized for incoming emergency cases. This informs future HMS modules that could flag long-stay patients and proactively free up capacity.
RFID and Real-Time Location for Patient Tracking: Yazici (2014) conducted an exploratory analysis of hospital perspectives on real-time information requirements and the adoption of RFID technology, published in the International Journal of Information Management. The study finds that hospitals value RFID primarily for its ability to provide real-time patient location data, enabling faster staff response and more accurate queue state awareness. This supports future HMS enhancements where physical check-in could be automated through card or sensor-based patient identification.
Resource Allocation and Location-Based Systems: Ng et al. (2022) demonstrated the use of a Real-Time Location System (RTLS) for contact tracing in a tertiary hospital in Singapore, published in BMC Infectious Diseases. Their simulation showed that RTLS-enabled patient tracking significantly improves discharge coordination and reduces bottlenecks during peak periods. This literature supports future extensions of the HMS to integrate location-aware patient status updates in larger hospital deployments.
Cost-Benefit of Digital Health Systems: Adler-Milstein & Jha (2017) analyzed the impact of the HITECH Act on electronic health record adoption across U.S. hospitals, published in Health Affairs. Their findings demonstrate that policy-mandated digitization drives large-scale adoption and measurable reductions in administrative costs and errors. This provides an evidence base for the HMS's design goal of reducing manual data entry errors and improving patient throughput through automation.
ISO 25010 Software Quality Standards & Local Compliance: ISO (2011) defines the ISO/IEC 25010 Systems and Software Quality Model, establishing eight quality characteristics — including Functional Suitability, Reliability, Security, and Maintainability — as the international benchmark for evaluating software systems. The Republic of the Philippines (2012) further enacted Republic Act No. 10173 (Data Privacy Act), which governs the collection, storage, and processing of personal health data in all digital systems. The HMS design adheres to both frameworks: service-layer separation supports maintainability, parameterized queries mitigate SQL injection risks for security, and the patient data schema is scoped to the minimum fields required for compliance with data minimization principles.
Community Health Information Tracking System (CHITS): GovPh (2020/2025 Updates) continues to serve as a benchmark for local EMRs. Literature shows that local systems must be modular to allow for the gradual addition of "intelligent" features like automated reporting.
User Experience (UX) for Filipino Patients: IJAR (2025) studied Lying-in Clinics in Bicol, finding that SMS-based queue notifications are more effective for the local demographic than complex app-based interfaces due to phone hardware limitations.
Predictive Analytics for Length of Stay (LOS): AA Research Index (2026) published a study on a Philippine-based HMS that predicts how long an inpatient will stay, allowing the "bed management queue" to be optimized for incoming emergency cases.
RFID for Patient Tracking: JETIR (2022) research in local settings suggests using RFID-enabled "Smart Cards" for patients, allowing the system to "auto-check" them into a queue as soon as they tap their card at the hospital entrance.
Resource Allocation during Pandemics: Singapore General Hospital & PH Partners (2025) literature discusses the use of Real-Time Location Systems (RTLS) to monitor movement, which helped a local hospital improve discharge efficiency by 12% during peak seasons.
Cost-Benefit of Smart Systems: Ken Research (2025) notes that while a mid-sized Philippine facility might spend PHP 600 million for full automation, the reduction in operational errors and improved patient turnaround provides a "Return on Investment" within 3–5 years.
ISO 25010 Standards in PH Software: Buhi Municipality Case Study (2025) evaluates local HMS projects based on Functional Suitability and Security, stating that intelligence is secondary to a system's reliability and data privacy (in compliance with the PH Data Privacy Act of 2012).
VI. System Overview
6.1 Purpose and Context
The Intelligent Hospital Management and Queueing System (HMS) is a browser-based operational dashboard implemented as a single Streamlit application (app.py). It consolidates day-to-day front-desk and coordination tasks—patient records, departmental configuration, waiting queues, doctor profiles, and appointments—into one interface backed by a relational database (MySQL or SQLite, selectable via configuration). The system is intended for internal hospital use rather than as a public patient portal: staff authenticate operationally through controlled access to the workstation running the app, and all workflows assume trusted users.
6.2 Target Users and Responsibilities
•	Medical receptionists and admitting staff register and update patients, maintain specialization (department) settings, add patients to queues, call the next patient, and adjust queue priority when clinical circumstances change.
•	Doctors and clinic coordinators rely on accurate doctor profiles, specialization assignments, and appointment calendars to avoid double-booking; they may review queue and appointment summaries on the Dashboard.
•	Hospital administrators and supervisors monitor aggregate activity through the Dashboard’s reports—patient demographics and triage mix, queue load and wait indicators, appointment completion and cancellation patterns, doctor workload, and specialization utilization—to support staffing and capacity decisions.
6.3 Major Functional Subsystems
The application is organized into six primary modules, accessible from the sidebar navigation. Together they cover the scope defined in §4.4.
•	Dashboard (Reports & Analytics): Presents summary metrics (totals for patients, doctors, active queue entries, appointments, and upcoming appointments) and user-selectable analytical views. Staff may enable one or more report types at once—including patient statistics, queue analytics, appointment summaries, doctor performance tables, specialization utilization, and a custom report builder that combines metric families. Visual summaries use Streamlit chart components; date-range filters apply where the reporting service supports them.
•	Patient Management: Supports creating, viewing, searching, filtering, editing, and deleting patient records. Search operates over fields such as name, phone, and email; filters include triage-oriented status (Normal, Urgent, Super-Urgent). The screen exposes headline statistics (counts by status) and an interactive patient list with row selection for edit/delete actions.
•	Specialization Management: Defines hospital departments or service lines with a maximum queue capacity, optional description, and an active/inactive flag. The list displays operational context (e.g., current queue size, utilization, assigned doctor count) to support capacity planning. Edit and delete flows respect business rules enforced in the service layer (including safe deactivation where applicable).
•	Queue Management: Maintains per-specialization waiting lists with an optional aggregate view across all active specializations. Staff add registered patients to a chosen department’s queue with a visit priority (Normal, Urgent, Super-Urgent); the system enforces capacity limits and prevents duplicate active entries for the same patient in the same queue. Serve Next applies the implemented ordering policy (priority first, then arrival time). Row-level actions include change priority, serve, and remove (with optional reason). A focused queue analytics panel is available for a selected specialization.
•	Doctor Management: Maintains doctor demographic and professional attributes (e.g., name, license, contact information, experience, certifications, hire date, bio) and employment status (Active, Inactive, On Leave). Doctors may be assigned to one or more active specializations, which feeds appointment validity and operational reporting. Delete operations follow a soft-delete pattern (typically marking the doctor inactive) to preserve historical integrity.
•	Appointment Management: Supports scheduling, editing, marking complete, and cancelling appointments. Bookings reference a patient, doctor, specialization, date, time, duration, type (e.g., Regular, Follow-up, Emergency), and status lifecycle (e.g., Scheduled, Confirmed, through Completed or Cancelled). The system performs overlap detection for the same doctor so conflicting time ranges (including duration) are rejected. Lists support text search and filters by status and date (e.g., today, upcoming, past).
6.4 User Interface Organization
The sidebar provides persistent navigation between modules, a system status indicator when the database connection succeeds, and quick statistics (patient, doctor, appointment, and active queue counts). The main workspace follows a recurring pattern: module-level metrics at the top, then search and filters where applicable, then primary action buttons (Add, Edit, Delete, or module-specific actions such as Serve Next), followed by data tables implemented as interactive grids. Tables that drive edit/delete flows include a selection column so the user explicitly chooses a single row before invoking an action, reducing accidental operations.
6.5 Deployment and Runtime Characteristics
The system runs as a local or intranet Streamlit server started from the project root (e.g., python -m streamlit run app.py). No separate mobile or desktop client is required beyond a web browser. Responsiveness is interaction-driven: after actions such as saving a record or refreshing a view, the interface reruns and reflects the current database state. Performance of list and report screens depends on dataset size, database engine, and hardware, as discussed further in 11.
6.6 Relationship to Architecture (Preview)
Module behavior is backed by service classes (patient, specialization, queue, doctor, appointment, report) and a shared database access abstraction, described structurally in §7 and §8. This overview emphasizes what the HMS provides to users; the following sections specify how those capabilities are designed and implemented.
VII. System Architecture and Design
7.1 Architectural Overview
The system employs a Layered Service-Oriented Architecture:
●	Presentation Layer: Streamlit (Reactive UI components).
●	Service Layer: Business logic (Queueing algorithms, Conflict checks).
●	Data Access Layer: Unified Database Manager using Dependency Injection.
7.2 Object-Oriented Design
Entities are modeled as classes (e.g., Patient, Doctor, Appointment) with clear responsibilities. Relationships are primarily modeled with foreign keys on the entity classes (for example, `Appointment` holds `patient_id`, `doctor_id`, and `specialization_id`); related rows are loaded through the service layer when needed rather than embedding full `Patient`/`Doctor` instances inside `Appointment` by default.
7.3 UML Diagrams
(Note: Visual diagrams should be inserted here during final formatting.)
●	Class Diagram: Should show the parallel database manager implementations (SQLite `DatabaseManager` vs `MySQLDatabaseManager`), the alias selected at import time, and how Service classes depend on that manager and Model classes.
●	Sequence Diagram: Illustrates the flow of "Scheduling an Appointment" involving the AppointmentService checking the DoctorService for availability.
VIII. Advanced Object-Oriented Concepts Applied
1.	Dependency Injection (DI): The DBManager is injected into Services at runtime. This allows the system to switch between MySQLManager and SQLiteManager without modifying service-level code.
2.	SOLID Principles (Single Responsibility): Each service (e.g., QueueService) is responsible for exactly one domain. Validation logic is separated from data persistence logic.
3.	Strategy Pattern: Implemented at the database package entry point. The system chooses the concrete manager based on `USE_MYSQL` and related settings in `src/config.py`, exposing a single `DatabaseManager` symbol to the rest of the app.
IX. Implementation Details
●	Language: Python 3.9+
●	Frameworks: Streamlit (Web UI), Pandas (Data Processing). Charts use Streamlit’s native chart APIs (e.g. `st.bar_chart`).
●	Module Organization:
○	/src/models: Domain entities.
○	/src/services: Core business logic.
○	/src/database: Persistence logic and SQL schemas.
●	Key Algorithm: The system implements a deterministic, priority-based dispatching algorithm designed to balance clinical urgency with temporal fairness. Rather than a singular weighted score, the system utilizes lexicographical ordering across two primary dimensions:
○	Priority Tier (Categorical Weighting): Patients are classified into discrete tiers (Normal, Urgent, Super-Urgent). In the service layer, these categories are mapped to an ordinal scale where higher clinical urgency always dominates the ordering sequence, regardless of arrival time.
○	Temporal Tie-Breaking (FIFO): Within a specific priority tier, the system adheres to a First-In, First-Out (FIFO) policy. This is achieved by utilizing the joined_at timestamp as a secondary sort criterion.
Implementation Logic: The algorithm is encapsulated within QueueService.get_queue and executed at the database level to ensure atomic consistency. The policy is realized through the SQL-equivalent logic: ORDER BY status DESC, joined_at ASC.
Technical Rationale: This approach ensures that Super-Urgent cases are immediately escalated to the top of the processing stack while eliminating "starvation" of lower-urgency peers within the same classification. By leveraging indexed database sorting, the dispatching engine maintains O(log n) efficiency, supporting high-throughput environments without performance degradation.
X. Testing and Validation
●	Unit Testing: Pytest-based tests under `tests/` verify database initialization, schema tables, basic CRUD paths, and patient service operations; appointment scheduling uses `AppointmentService.check_conflicts` to identify overlapping time slots for the same doctor.
●	Integration Testing: Validated flows where specializations, doctor assignments, and queue entries interact, including safeguards when specializations are changed or removed so queue data stays coherent with department configuration.
●	Edge Cases: Handled cases where the queue reaches the “Maximum Capacity” defined in the specialization settings, and when a patient is already active in a specialization’s queue.
XI. Results and Discussion
11.1 Outcomes Relative to Project Objectives
Taken together, the implemented system satisfies the objectives stated in Section 4.3 at the level of a cohesive proof-of-concept suitable for demonstration and iterative refinement. Patient registration and prioritization are operational: records persist through the service layer, triage-style status is visible in the UI, and the same conceptual priority feeds queue ordering. Appointment conflict detection is enforced in `AppointmentService` before commits and on relevant updates, so double-booking the same physician for overlapping intervals (respecting duration) is blocked rather than left to manual checking. Database portability is realized through the configured choice between MySQL and SQLite without rewriting domain services, which validates the intended separation of persistence from business rules. The Dashboard further extends the outcome beyond bare CRUD by aggregating patient, queue, appointment, doctor, and specialization signals into charts and tables that administrators can interpret without exporting raw tables first.
11.2 Observed Behavior of the User Interface
The presentation tier follows Streamlit’s execution model: each meaningful interaction triggers a rerun of the script, and widgets are rebuilt from the current database state. In practice, staff obtain immediate feedback after saves, queue mutations, and navigation changes, which aligns with reception workflows where the latest roster matters more than sub-second push updates. The recurring layout—summary metrics, filters, primary actions, then selectable grids—reduces the cognitive cost of moving between Patient, Specialization, Queue, Doctor, and Appointment tasks. This consistency is a deliberate usability result of the single-application design, even though it does not yet incorporate role-based views or authenticated sessions (see Section 4.4.3).
11.3 Performance, Reporting, and Evaluation Limits
Analytical workloads are handled through SQL-backed queries in the service layer combined with Pandas transformations where the Dashboard requires reshaped series for charts (e.g., st.bar_chart). For typical academic and pilot datasets, list and report screens remain responsive on modest hardware; however, no formal load or latency benchmark is bundled with the repository, and absolute performance is necessarily a function of record volume, index usage, DB engine (MySQL versus SQLite), and host resources. Queue ordering itself is delegated to the database sort path in QueueService.get_queue, which scales predictably with routine indexing assumptions but was not stress-tested here at hospital-scale concurrency. These points bound how strongly one may generalize “performance results”: what is demonstrated is architectural feasibility and correctness-oriented behavior under manual and small-suite automated testing (Section 10), not a certified throughput claim.
11.4 Discussion: Design Trade-offs and Lessons Learned
The Streamlit-first stack trades maximum customization of front-end behavior for rapid delivery and a uniform Python codebase, which matches the course emphasis on object-oriented structure in the backend rather than on bespoke JavaScript clients. Dependency injection of a single database manager symbol into services paid dividends when toggling engines, but it also surfaces the importance of consistent query semantics across SQLite and MySQL (e.g., type and cursor shape handling), which remains an ongoing maintenance consideration. More broadly, the project illustrates that queue fairness within priority tiers and temporal conflict rules for appointments are policy choices that must stay aligned with clinical operations; encoding them in services keeps the UI thin but does not remove the need for domain review when deploying beyond the classroom. In sum, the results support the thesis that modular OOP services behind a lightweight web shell can deliver an intelligible hospital operations dashboard, while the discussion clarifies where production hardening—security, scale testing, and extended integrations—would need to follow.

XII. Conclusion and Future Enhancements
12.1 Summary Conclusion
This capstone addressed the fragmentation of reception, queueing, and scheduling tasks described in Section 4.1 by delivering a unified, browser-based Hospital Management and Queueing System implemented in Python and Streamlit. The solution aligns software structure with operational reality: domain rules live in service classes, persistence is accessed through a configurable database manager, and the user interface concentrates on clarity of workflow rather than on a large custom front-end codebase. As discussed in Section 11, the running system meets the stated objectives—automated patient records with triage-aware priority, conflict-aware appointment booking, dual-database portability, and management-facing analytics—while openly acknowledging limits on formal performance certification and production-grade security (Section 4.4.3 and Section 11.3).
12.2 Principal Contributions
The work makes three contributions that extend beyond a minimal prototype. First, it shows that dependency injection of a shared database abstraction enables the same service logic to run against MySQL or SQLite, which supports both classroom SQLite demos and more realistic MySQL deployments without forking the business layer. Second, it encodes non-trivial policies—priority-first queue ordering with FIFO within tiers, and interval-based doctor overlap detection—in testable services rather than ad hoc SQL in the UI. Third, it demonstrates that advanced OOP and a lightweight reactive shell can coexist: maintainability is pursued through small, single-purpose services and explicit models, while Streamlit supplies rapid iteration for forms, tables, and charts.
12.3 Future Enhancements
Future work should proceed along two tracks: user-facing expansion and engineering hardening, consistent with the exclusions already listed in Section 4.4.3.
•	Patient-facing services: A patient portal for self-service registration, appointment requests, or queue status would close the gap between internal staff tools and public expectations; it would require authentication, consent flows, and API boundaries not present in the current monolithic app.
•	Intelligent operations: An AI- or analytics-driven wait-time estimator could combine historical queue lengths, service durations, and specialization load; such a module would build on the reporting aggregates already produced for the Dashboard but would need validated data pipelines and guardrails against misleading clinical promises.
•	Security and governance: Role-based access control, per-user authentication, session timeout, and audit trails tied to identifiable actors are prerequisites for any regulated deployment and would interact with every module that reads or writes PHI.
•	Financial and payer integration: Billing, insurance eligibility, and claims-related interfaces remain natural extensions once core logistics are stable; they imply new services, external APIs, and reconciliation logic outside today’s scope.
•	Quality and scale: Expanded automated test coverage (including appointment conflict regression suites), load and concurrency testing, and optional deployment packaging (containers, CI pipelines) would strengthen claims about reliability and throughput beyond manual validation.
Together, these directions preserve the architectural direction validated here—thin presentation, rich domain services—while moving the product from an educational HMS toward an auditable, scalable hospital information utility.
XIII. References
Adler-Milstein, J., & Jha, A. K. (2017). HITECH act drove large gains in hospital
    electronic health record adoption. Health Affairs, 36(8), 1416–1422.
    https://doi.org/10.1377/hlthaff.2016.1651

Alotaibi, S., & Roussinov, D. (2024). A secure blockchain framework for healthcare
    records management systems. Cell Reports Medicine, 5(12), Article 101852.
    https://doi.org/10.1016/j.xcrm.2024.101852

Fawzy, D., Moussa, S., & Badr, N. (2022). An IoT-based resource utilization framework
    using data fusion for smart environments. Internet of Things, 20, Article 100645.
    https://doi.org/10.1016/j.iot.2022.100645

Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). Design patterns: Elements of
    reusable object-oriented software. Addison-Wesley Professional.

Hodgson, N. R., Saghafian, S., Martini, W. A., Feizi, A., & Orfanoudaki, A. (2025).
    Artificial intelligence-assisted emergency department vertical patient flow
    optimization. Journal of Personalized Medicine, 15(6), Article 219.
    https://doi.org/10.3390/jpm15060219

Idian, L. G. M. (2025). Lying-in clinic information management system for Buhi
    municipality. International Journal of Advanced Research, 13(8), 911–923.
    https://www.journalijar.com/article/55784/

ISO. (2011). ISO/IEC 25010:2011—Systems and software engineering: Systems and software
    quality requirements and evaluation (SQuaRE)—System and software quality models.
    International Organization for Standardization. https://www.iso.org/standard/35733.html

Jalali, H., & Belkic, K. (2024). A solution to reduce the impact of patients' no-show
    behavior on hospital operating costs: Artificial intelligence-based appointment
    system. Healthcare, 12(21), Article 2173.
    https://doi.org/10.3390/healthcare12212173

Lau, M., Tayag, M. M., Abu-Haydar, E., Talento, M. L., & Llanes, E. (2025).
    Implementing electronic health records in Philippine primary care settings:
    Mixed-methods pilot study. JMIR Medical Informatics, 13, Article e63036.
    https://doi.org/10.2196/63036

Lee, K. L. (2020). Intelligent queue management system (i-Queue) for patients in
    hospital [Undergraduate project, Universiti Malaysia Sarawak]. UNIMAS
    Institutional Repository. https://ir.unimas.my/id/eprint/34199/

Lehne, M., Sass, J., Essenwanger, A., Schepers, J., & Thun, S. (2019). Why digital
    medicine depends on interoperability. npj Digital Medicine, 2, Article 79.
    https://doi.org/10.1038/s41746-019-0158-1

Lim, T. L. L., Chan, K. S., & Lim, Y. W. (2023). Prevalence and predictors of prolonged
    length of stay among patients admitted under general internal medicine in a tertiary
    government hospital in Manila, Philippines: A retrospective cross-sectional study.
    BMC Health Services Research, 23, Article 48.
    https://doi.org/10.1186/s12913-022-08885-4

Manis, I., Rigas, G., Gatsios, D., Tachos, N., Stefanou, A., & Fotiadis, D. I. (2025).
    AI-enhanced telemedicine: Transforming resource allocation and cost-efficiency
    analysis via advanced queueing model. Scientific Reports, 15, Article 23048.
    https://doi.org/10.1038/s41598-025-15664-8

Marcelo, A. B., Magtibay, C., & Tresvalles, R. L. (2013). Community health information
    and tracking system (CHITS): Lessons from eight years implementation of a pioneer
    electronic medical record system in the Philippines. Acta Medica Philippina, 47(1),
    52–57. https://actamedicaphilippina.upm.edu.ph/index.php/acta/article/view/769

Martin, R. C. (2017). Clean architecture: A craftsman's guide to software structure and
    design. Prentice Hall.

Menshawi, A., Sakr, S., & Aboulnaga, A. (2025). A novel triage framework for emergency
    department based on machine learning paradigm. Expert Systems, 42(1), Article e13735.
    https://doi.org/10.1111/exsy.13735

Ng, K. F., Lim, Y. S., & Koh, M. (2022). Contact tracing using real-time location
    system (RTLS): A simulation exercise in a tertiary hospital in Singapore. BMC
    Infectious Diseases, 22, Article 756. https://doi.org/10.1186/s12879-022-07731-4

Philippine Health Insurance Corporation. (2024). PhilHealth eClaims system.
    https://www.philhealth.gov.ph/

Republic of the Philippines. (2012). Republic Act No. 10173: Data Privacy Act of 2012.
    Official Gazette.
    https://www.officialgazette.gov.ph/2012/08/15/republic-act-no-10173/

Republic of the Philippines. (2019). Republic Act No. 11223: An act instituting universal
    health care for all Filipinos [Universal Health Care Act]. Official Gazette.
    https://www.officialgazette.gov.ph/2019/02/20/republic-act-no-11223/

Saghafian, S., Hopp, W. J., Van Oyen, M. P., Iravani, S. M. R., & Gong, Y. (2020).
    Workload management in telemedical physician triage and other knowledge-based service
    systems. Management Science, 66(5), 1947–1971.
    https://doi.org/10.1287/mnsc.2019.3277

Streamlit. (2025). API reference. Streamlit Documentation. Retrieved March 22, 2026,
    from https://docs.streamlit.io/develop/api-reference

Tshiamala, D., & Tartibu, L. (2025). Telemedicine queuing system study: Integrating
    queuing theory, artificial neural networks (ANNs) and particle swarm optimization
    (PSO). Applied Sciences, 15(11), Article 6349.
    https://doi.org/10.3390/app15116349

Yazici, A. (2014). An exploratory analysis of hospital perspectives on real time
    information requirements and perceived benefits of RFID technology for future
    adoption. International Journal of Information Management, 34(5), 603–621.
    https://doi.org/10.1016/j.ijinfomgt.2014.05.004

Yi, Y., Tang, T., & Zhao, X. (2025). The effects of applying artificial intelligence to
    triage in the emergency department: A systematic review of prospective studies.
    Journal of Nursing Scholarship, 57(1), 112–124.
    https://doi.org/10.1111/jnu.13024

 
XIV. Appendices (User Manual & Feature Flows)

14.1 User Manual & System Navigation
Hospital Management System — User Manual
This manual describes the Streamlit web application (app.py). It focuses on where to click, what to type or select, and the order of controls on each screen.
Audience and purpose
The system is for hospital staff who manage patients, departments (specializations), queues, doctors, appointments, and reports.
Prerequisites and startup
•	Python 3, dependencies from requirements.txt, database configured in src/config.py (MySQL via XAMPP or SQLite).
Start the app (project folder = folder containing app.py):
python -m streamlit run app.pyj
Or on Windows: run run_streamlit.bat.
If the database fails, the main area shows Database Connection Failed and troubleshooting text; the sidebar navigation does not load normal content until this is fixed.
How the interface behaves (Streamlit)
•	The left sidebar is fixed: branding, Navigation buttons, System status, Quick Stats.
•	The main area (right) shows the page for the current navigation choice.
•	After many button clicks, the app reruns the page; forms and tables refresh. If something “jumps,” scroll back to the section you were using.
•	Tables that support actions use a Select column (checkbox). Select one row, then use the action buttons above the table (not below), unless the on-screen instructions say otherwise.
Sidebar: global navigation (always visible)
Read the sidebar from top to bottom.
Step	What you see	What to do
1	Title area: Hospital Management / Management System	(Information only)
2	Navigation heading	—
3	Six navigation buttons (full width)	Click one to switch the main page. Only one page is active at a time; the active button is styled as the primary button.
Navigation button labels (click exactly these):
•	Dashboard: Reports & analytics
•	Patient Management: Patients
•	Specialization Management: Specializations / departments
•	Queue Management: Waiting queues
•	Doctor Management: Doctors
•	Appointments: Appointments
Below the buttons:
Element	Meaning
System status	Shows Connected when the database initialized successfully.
Quick Stats	Metrics: Patients, Doctors, Appointments, Queue (two columns of numbers).

5. General pattern: lists + Select checkbox + actions
On Patient, Specialization, Doctor, and Appointment pages:
1.	Statistics and sometimes search/filter appear at the top.
2.	Action buttons (Add / Edit / Delete / etc.) are in a row below the search row.
3.	A horizontal rule (---) separates that from forms (Add/Edit/Delete) when they are open.
4.	The table is below the forms area.
Selecting a row
1.	Scroll to the subheading … List - Click the checkbox in a row to select it.
2.	In the table, tick Select on one row.
3.	A green success line appears: Selected: … — Click Edit/Delete button above to proceed.
4.	Click the desired action button above the table (e.g. Edit Patient).
I. Dashboard — click-by-click
Open: In the sidebar, click Dashboard.
Title: Dashboard
1.	Reports & Analytics Summary — five metrics in one row: Total Patients, Total Doctors, Active Queue, Total Appointments, Upcoming.
2.	Select Report Types (Select multiple to view all at once) — multiselect dropdown. Click to add/remove report types. Options: Patient Statistics, Queue Analytics, Appointment Reports, Doctor Performance, Specialization Utilization, Custom Report.
3.	Date range (two columns):
o	Start Date — date picker
o	End Date — date picker
4.	Below that, each selected report type renders its own blocks (metrics, subheadings, bar charts). Scroll to see all.
5.	Custom Report only: after selecting Custom Report in the multiselect, scroll to Custom Report Builder:
o	Select Metrics — multiselect: Patient Statistics, Queue Statistics, Appointment Statistics, Doctor Statistics, Specialization Statistics
o	Click Generate Custom Report (primary button) to build the combined view below.
II. Patient Management — navigation and controls
Open: Sidebar → Patient Management.
Title: Patient Management
1.	Patient Statistics — metrics: Total Patients, Normal, Urgent, Super-Urgent
2.	Row 1 (columns):
o	Search Patients — text field; placeholder text: Search by name, phone, or email...
o	Filter by Status — dropdown: All, Normal, Urgent, Super-Urgent
o	Refresh — button (reloads)
3.	Row 2 (three buttons):
o	Add New Patient (primary)
o	Edit Patient
o	Delete Patient
If you opened Add/Edit/Delete, the corresponding form block appears next.
4.	Patient List - Click the checkbox in a row to select it — table with columns Select, ID, Name, Age, Gender, Status, Phone, Email
Add a new patient (procedure)
1.	Click Add New Patient.
2.	Find the Add New Patient subheading and the form below it.
3.	Fill inputs:
o	Full Name (required) / Date of Birth (required) / Gender / Phone Number
o	Email / Address / Status (Normal, Urgent, Super-Urgent)
4.	Click Save Patient to submit, or Cancel to close without saving.
III. Specialization Management — navigation and controls
Open: Sidebar → Specialization Management.
Title: Specialization Management
1.	Specialization Statistics — Total Specializations, Active, Inactive, Total Capacity
2.	Row 1: Search Specializations | Refresh
3.	Row 2 (four controls):
o	Add New Specialization (primary)
o	Edit Specialization
o	Delete Specialization
o	Filter — dropdown: All, Active Only, Inactive Only
4.	Specialization List — table: Select, ID, Name, Max Capacity, Current Queue, Utilization, Doctors, Status
Add specialization (procedure)
1.	Click Add New Specialization.
2.	Under Add New Specialization:
o	Specialization Name (required) / Description
o	Maximum Queue Capacity (required) — number (1–1000)
o	Active — checkbox
3.	Save Specialization or Cancel.
IV. Queue Management — navigation and controls
Open: Sidebar → Queue Management.
Title: Queue Management
1.	Queue Statistics — Total Active, Normal, Urgent, Super-Urgent, Avg Wait Time
2.	Select Specialization — dropdown: (Must select a specific specialization for actions)
3.	Row of four buttons:
o	Add to Queue (primary)
o	Serve Next Patient
o	Refresh Queue
o	View Analytics
Add to queue (procedure)
1.	In Select Specialization, choose a named department (not All).
2.	Click Add to Queue.
3.	Under Add Patient to Queue:
o	Select Patient — dropdown of all patients
o	Priority Level — Normal (0), Urgent (1), Super-Urgent (2)
4.	Add to Queue or Cancel.
V. Doctor Management — navigation and controls
Open: Sidebar → Doctor Management.
Title: Doctor Management
1.	Doctor Statistics — Total Doctors, Active, Inactive, On Leave
2.	Search Doctors | Filter by Status | Refresh
3.	Add New Doctor | Edit Doctor | Delete Doctor
4.	Doctor List — Select, ID, Name, License, Status, Phone, Email, Experience
Add doctor (procedure)
1.	Click Add New Doctor.
2.	Fill Full Name, License Number, Phone, Email, Medical Degree, Years of Experience.
3.	Specializations heading → Select Specializations — multiselect.
4.	Add Doctor or Cancel.
Appointment Management — navigation and controls
Open: Sidebar → Appointments.
Title: Appointment Management
1.	Appointment Statistics — Total, Scheduled, Confirmed, Completed, Cancelled
2.	Search Appointments | Filter by Status | Filter by Date | Refresh
3.	Schedule New Appointment | Edit Appointment | Mark Complete | Cancel Appointment
4.	Appointment List — Select, ID, Date, Time, Patient, Doctor, Specialization, Type, Status, Duration
Schedule new appointment (procedure)
1.	Click Schedule New Appointment.
2.	Fill the form: Patient, Doctor, Specialization, Appointment Date, Appointment Time, Duration (minutes), Appointment Type, Status.
3.	Click Schedule Appointment or Cancel.
4.	Note: If a conflict exists, the system will block the request and show a Time slot conflicts... error.
Patient dropdown on appointments (IMPORTANT)
The Schedule and Edit appointment forms only list patients where the code filters patient.status == 1. In this project, Patient.status is triage: 0 = Normal, 1 = Urgent, 2 = Super-Urgent. So the Patient dropdown effectively shows Urgent patients only.
Quick troubleshooting
Issue	Check
Cannot connect	MySQL/XAMPP, database name, src/config.py
Add to queue blocked	Capacity; duplicate patient in same department queue
No patients in appointment form	§12 — try Urgent status
Wrong row targeted	Exactly one Select checkbox ticked before Edit/Delete

Reference paths
Item	Location
App entry	app.py
Configuration	src/config.py
Services	src/services/

For service behavior details, see API_DOCUMENTATION.md in the same folder.
System Access
●	Starting the App: Run the application via python -m streamlit run app.py or run_streamlit.bat.
●	Database Connection: Upon launch, the system verifies connection to the database (MySQL/XAMPP or SQLite). If the connection fails, an alert will guide you to check your configuration in src/config.py.
Interface Navigation
●	Sidebar: Contains the main navigation menu, real-time system status (Connected/Disconnected), and Quick Stats (Total Patients, Doctors, and Active Queue count).
●	Main Area: Displays the active module's workspace, including interactive tables, action buttons (Add, Edit, Delete), and data visualizations.
Quick Reference: Common Patterns
Action	Typical Flow
Add New Item	Click "Add..." button → Fill the form → Click Save.
Edit/Delete	Select a row in the table (checkbox) → Click the corresponding action button.
Search/Filter	Enter text in search bars; tables update instantly.
Refresh	Use the "Refresh" button in any module to pull the latest database state.


-- ============================================================================
-- File: three_table_join.sql
-- Database: healthcare.db
-- Schema Overview:
--   sites        (site_id, site_name, region, city)
--   clinics      (clinic_id, site_id, clinic_name, specialty)
--   appointments (appointment_id, clinic_id, patient_id, appointment_date, status, fee)
-- ============================================================================

-- Query 1: Detailed appointment records across sites and clinics
SELECT 
    s.site_name,
    s.region,
    c.clinic_name,
    c.specialty,
    a.appointment_id,
    a.patient_id,
    a.appointment_date,
    a.status,
    a.fee
FROM sites s
JOIN clinics c ON s.site_id = c.site_id
JOIN appointments a ON c.clinic_id = a.clinic_id
ORDER BY a.appointment_date DESC;

-- Query 2: Site-level appointment count and completed revenue aggregation
SELECT 
    s.site_id,
    s.site_name,
    s.region,
    COUNT(a.appointment_id) AS total_appointments,
    SUM(CASE WHEN a.status = 'Completed' THEN a.fee ELSE 0 END) AS completed_revenue
FROM sites s
JOIN clinics c ON s.site_id = c.site_id
JOIN appointments a ON c.clinic_id = a.clinic_id
GROUP BY s.site_id, s.site_name, s.region
ORDER BY completed_revenue DESC;

-- Query 3: Clinic utilization including clinics with zero appointments (LEFT JOIN)
SELECT 
    s.site_name,
    c.clinic_id,
    c.clinic_name,
    c.specialty,
    COUNT(a.appointment_id) AS appointment_count
FROM sites s
JOIN clinics c ON s.site_id = c.site_id
LEFT JOIN appointments a ON c.clinic_id = a.clinic_id
GROUP BY s.site_name, c.clinic_id, c.clinic_name, c.specialty
ORDER BY appointment_count ASC, c.clinic_name;

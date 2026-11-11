-- ============================================================================
-- Healthcare Database Analytical & Operational Queries (queries.sql)
-- Schema: sites, clinics, appointments
-- ============================================================================
-- RULES & DEFINITIONS:
-- 1. REVENUE RULE - Revenue strictly counts completed appointments only. Fees count only when status is Completed.
-- 2. NO-SHOW RATE RULE - Calculated as No-Shows divided by all appointments (Completed + No-Show + Cancelled).
--    Data span - January 1, 2026 to April 1, 2026 (Note - April 1 is a partial single-day month).
-- ============================================================================

-- 1. List clinics along with their parent site names and regions
SELECT 
    c.clinic_id,
    c.clinic_name,
    s.site_name,
    s.region
FROM clinics c
JOIN sites s ON c.site_id = s.site_id
ORDER BY s.region, s.site_name, c.clinic_name;


-- 2. Count total appointments per clinic, including clinics with zero appointments (LEFT JOIN)
SELECT 
    c.clinic_id,
    c.clinic_name,
    COUNT(a.appointment_id) AS total_appointments
FROM clinics c
LEFT JOIN appointments a ON c.clinic_id = a.clinic_id
GROUP BY c.clinic_id, c.clinic_name
ORDER BY total_appointments DESC;


-- 3. Calculate overall appointment status breakdown and percentage
SELECT 
    status,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM appointments), 2) AS percentage
FROM appointments
GROUP BY status
ORDER BY count DESC;


-- 4. Calculate completed appointment counts, total revenue, and average completed fee per clinic
-- Rule - Completed counts across clinics should add up to Q3's Completed total.
SELECT 
    c.clinic_name,
    SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) AS completed_appointments,
    SUM(CASE WHEN a.status = 'Completed' THEN a.fee ELSE 0 END) AS total_revenue,
    ROUND(AVG(CASE WHEN a.status = 'Completed' THEN a.fee END), 2) AS avg_fee_completed
FROM clinics c
LEFT JOIN appointments a ON c.clinic_id = a.clinic_id
GROUP BY c.clinic_id, c.clinic_name
ORDER BY total_revenue DESC;


-- 5. Find clinics with a No-Show rate greater than 20% (Rate = No-Shows / All appointments including cancelled)
SELECT 
    c.clinic_name,
    COUNT(a.appointment_id) AS total_appointments,
    SUM(CASE WHEN a.status = 'No-Show' THEN 1 ELSE 0 END) AS no_shows,
    ROUND(SUM(CASE WHEN a.status = 'No-Show' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.appointment_id), 2) AS no_show_percentage
FROM clinics c
JOIN appointments a ON c.clinic_id = a.clinic_id
GROUP BY c.clinic_id, c.clinic_name
HAVING (SUM(CASE WHEN a.status = 'No-Show' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.appointment_id)) > 20.0
ORDER BY no_show_percentage DESC;


-- 6. Identify regional performance: total appointments and completed revenue by hospital region
SELECT 
    s.region,
    COUNT(a.appointment_id) AS total_appointments,
    SUM(CASE WHEN a.status = 'Completed' THEN a.fee ELSE 0 END) AS regional_revenue
FROM sites s
JOIN clinics c ON s.site_id = c.site_id
JOIN appointments a ON c.clinic_id = a.clinic_id
GROUP BY s.region
ORDER BY regional_revenue DESC;


-- 7. Top 5 patients with the highest total completed revenue generated (using patient_id and completed status only)
SELECT 
    patient_id,
    COUNT(appointment_id) AS visit_count,
    ROUND(SUM(CASE WHEN status = 'Completed' THEN fee ELSE 0 END), 2) AS total_revenue
FROM appointments
GROUP BY patient_id
ORDER BY total_revenue DESC
LIMIT 5;


-- 8. Monthly appointment volume and completed revenue trend (Jan-Apr 2026 - excluding partial April)
SELECT 
    strftime('%Y-%m', appointment_date) AS appointment_month,
    COUNT(*) AS monthly_appointments,
    ROUND(SUM(CASE WHEN status = 'Completed' THEN fee ELSE 0 END), 2) AS monthly_revenue
FROM appointments
WHERE appointment_date < '2026-04-01'
GROUP BY appointment_month
ORDER BY appointment_month;


-- 9. Clinics with no appointments at all (demonstrating outer join filtering)
SELECT 
    c.clinic_id,
    c.clinic_name,
    s.site_name
FROM clinics c
JOIN sites s ON c.site_id = s.site_id
LEFT JOIN appointments a ON c.clinic_id = a.clinic_id
WHERE a.appointment_id IS NULL;


-- 10. Summary metrics by site and clinic combining patient volume and completed revenue averages
SELECT 
    s.site_name,
    c.clinic_name,
    COUNT(a.appointment_id) AS appt_count,
    ROUND(AVG(CASE WHEN a.status = 'Completed' THEN a.fee END), 2) AS average_completed_fee,
    SUM(CASE WHEN a.status = 'Completed' THEN a.fee ELSE 0 END) AS total_revenue
FROM sites s
JOIN clinics c ON s.site_id = c.site_id
JOIN appointments a ON c.clinic_id = a.clinic_id
GROUP BY s.site_name, c.clinic_name
ORDER BY s.site_name, total_revenue DESC;


-- ============================================================================
-- ADDITIONAL QUERIES FOR MANAGEMENT REVIEW
-- ============================================================================

-- 11. No-Show Rate by Month (Tracking operational reliability over time - excluding partial April)
SELECT 
    strftime('%Y-%m', appointment_date) AS appointment_month,
    COUNT(*) AS total_appointments,
    SUM(CASE WHEN status = 'No-Show' THEN 1 ELSE 0 END) AS no_shows,
    ROUND(SUM(CASE WHEN status = 'No-Show' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS monthly_no_show_rate
FROM appointments
WHERE appointment_date < '2026-04-01'
GROUP BY appointment_month
ORDER BY appointment_month;


-- 12. No-Show Rate by Region (Three-table join: sites -> clinics -> appointments)
SELECT 
    s.region,
    COUNT(a.appointment_id) AS total_appointments,
    SUM(CASE WHEN a.status = 'No-Show' THEN 1 ELSE 0 END) AS no_shows,
    ROUND(SUM(CASE WHEN a.status = 'No-Show' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.appointment_id), 2) AS regional_no_show_rate
FROM sites s
JOIN clinics c ON s.site_id = c.site_id
JOIN appointments a ON c.clinic_id = a.clinic_id
GROUP BY s.region
ORDER BY regional_no_show_rate DESC;


-- 13. Clinics with No-Show Rates Above the Overall System Average (Using a Subquery)
-- Note - Overall average is the pooled system rate (total no-shows divided by total appointments), not the average of clinic rates.
SELECT 
    c.clinic_name,
    COUNT(a.appointment_id) AS total_appointments,
    ROUND(SUM(CASE WHEN a.status = 'No-Show' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.appointment_id), 2) AS clinic_no_show_rate
FROM clinics c
JOIN appointments a ON c.clinic_id = a.clinic_id
GROUP BY c.clinic_id, c.clinic_name
HAVING (SUM(CASE WHEN a.status = 'No-Show' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.appointment_id)) > (
    SELECT (SUM(CASE WHEN status = 'No-Show' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) 
    FROM appointments
)
ORDER BY clinic_no_show_rate DESC;
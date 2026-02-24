// تصحيح الأخطاء
let baseRate = 0.12;
if (student === 'yes') baseRate = 0.07;
if (marital === 'married') baseRate = 0.12;
let dailySuggested = Math.round((monthlyIncome * baseRate) / 30); // تم إضافة قوس إضافي

weeks.forEach(w => {
    w.rows.forEach((r, idx) => {
        r.suggested = dailySuggested;
        if (r.status === 'saved') r.goal = dailySuggested;
    });
});

if (activeWeekId) loadWeekTable(activeWeekId);
updateBudgetOverview();

// تصحيح أخطاء الـ Event Listeners
document.getElementById('saveWeekBtn').addEventListener('click', () => {
    alert('week saved locally (demo)');
});

document.getElementById('saveMonthBtn').addEventListener('click', () => {
    alert('monthly table saved (demo)');
});

// تصحيح هذا السطر
window.addNewWeek = addNewWeek; // بدلاً من window.addEventListener
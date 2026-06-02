/**
 * Poop Journal — Interactive frontend script
 * Handles subtle micro-interactions, alert dismissal, and premium interface tweaks.
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('Poop Journal premium UI initialized.');
    
    // Auto-dismiss standard alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-danger)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add subtle hover effect for list items and custom interactions if any
});

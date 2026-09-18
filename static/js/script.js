function togglePassword(fieldId, button) {
    const field = document.getElementById(fieldId);

    if (field.type === "password") {
        field.type = "text";
        button.textContent = "Hide";
    } else {
        field.type = "password";
        button.textContent = "Show";
    }
}
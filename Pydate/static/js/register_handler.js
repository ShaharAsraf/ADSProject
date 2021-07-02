docReady(function () {
    today = new Date()
    document.getElementById("id_birth_date").setAttribute("type", "date")
    document.getElementById('id_birth_date').valueAsDate = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate());
})

function docReady(fn) {
    if (document.readyState === "complete" || document.readyState === "interactive") {
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}
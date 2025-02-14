document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    
    fetch("../backend/controllers/AuthController.php", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${username}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // ✅ Login muvaffaqiyatli, foydalanuvchini dashboard.php sahifasiga yo‘naltiramiz
            window.location.href = "../backend/views/dashboard.php";
        } else {
            // ❌ Xato bo‘lsa, foydalanuvchiga bildiramiz
            document.getElementById("errorMsg").innerText = "❌ Login yoki parol noto‘g‘ri!";
        }
    })
    .catch(error => console.error("Xatolik:", error));
});

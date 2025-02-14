<?php
session_start();
require_once '../config/database.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim(htmlspecialchars($_POST["username"]));
    $password = trim($_POST["password"]);

    $stmt = $conn->prepare("SELECT * FROM admins WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();
    $admin = $result->fetch_assoc();

    if ($admin && password_verify($password, $admin["password"])) {
        $_SESSION["admin"] = $admin["username"];
        header("Location: admin_panel.php");
        exit();
    } else {
        echo "<p style='color:red;'>❌ Noto‘g‘ri login yoki parol!</p>";
    }
}
?>

<form method="post">
    <input type="text" name="username" placeholder="Admin login" required>
    <input type="password" name="password" placeholder="Parol" required>
    <button type="submit">Kirish</button>
</form>

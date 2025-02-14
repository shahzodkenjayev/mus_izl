<?php
session_start();
if (!isset($_SESSION["user_id"])) {
    header("Location: ../../client/index.html");
    exit;
}
?>
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <link rel="stylesheet" href="../../client/css/style.css">
</head>
<body>
    <div class="container">
        <h2>Dashboard</h2>
        <p>Xush kelibsiz! Bu yerda ma'lumotlaringizni boshqarishingiz mumkin.</p>
        <a href="../public/logout.php">🚪 Chiqish</a>
    </div>
</body>
</html>

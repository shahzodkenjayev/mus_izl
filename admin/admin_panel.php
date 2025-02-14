<?php
session_start();
include 'db.php'; // Ma'lumotlar bazasi ulanishi

if (!isset($_SESSION["admin"])) {
    header("Location: admin_login.php");
    exit();
}

// FOYDALANUVCHILARNI KO'RISH
$users = $conn->query("SELECT * FROM users");

// YANGI FOYDALANUVCHI QO‘SHISH
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["add_user"])) {
    $username = $_POST["username"];
    $password = password_hash($_POST["password"], PASSWORD_DEFAULT);
    $role = $_POST["role"];
    $mac = $_POST["mac_address"];
    $ip = $_POST["ip_address"];

    $stmt = $conn->prepare("INSERT INTO users (username, password, role, mac_address, ip_address, created_at) VALUES (?, ?, ?, ?, ?, NOW())");
    $stmt->bind_param("ssiss", $username, $password, $role, $mac, $ip);
    $stmt->execute();
    header("Location: admin_panel.php");
}

// FOYDALANUVCHINI O‘CHIRISH
if (isset($_GET["delete_user"])) {
    $id = $_GET["delete_user"];
    $conn->query("DELETE FROM users WHERE id = $id");
    header("Location: admin_panel.php");
}

?>

<h2>Admin Panel</h2>

<!-- Yangi foydalanuvchi qo'shish -->
<form method="post">
    <input type="text" name="username" placeholder="Foydalanuvchi nomi" required>
    <input type="password" name="password" placeholder="Parol" required>
    <input type="number" name="role" placeholder="Roli (1-20)" required>
    <input type="text" name="mac_address" placeholder="MAC manzil" required>
    <input type="text" name="ip_address" placeholder="IP manzil" required>
    <button type="submit" name="add_user">Qo‘shish</button>
</form>

<!-- Foydalanuvchilar ro'yxati -->
<table border="1">
    <tr>
        <th>ID</th>
        <th>Foydalanuvchi</th>
        <th>Role</th>
        <th>MAC</th>
        <th>IP</th>
        <th>Harakat</th>
    </tr>
    <?php while ($user = $users->fetch_assoc()) { ?>
        <tr>
            <td><?= $user["id"] ?></td>
            <td><?= $user["username"] ?></td>
            <td><?= $user["role"] ?></td>
            <td><?= $user["mac_address"] ?></td>
            <td><?= $user["ip_address"] ?></td>
            <td>
                <a href="?delete_user=<?= $user["id"] ?>" onclick="return confirm('Haqiqatan ham o‘chirmoqchimisiz?')">O‘chirish</a>
            </td>
        </tr>
    <?php } ?>
</table>

<a href="logout.php">Chiqish</a>

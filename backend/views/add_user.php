
<?php
require_once '../models/User.php';

$message = ""; // Xabar uchun o‘zgaruvchi

// Agar formadan ma'lumot kelgan bo'lsa
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["add_user"])) {
    $username = $_POST["username"];
    $password = $_POST["password"];
    $role = $_POST["role"];
    $mac_address = $_POST["mac_address"];
    $ip_address = $_POST["ip_address"];

    // Foydalanuvchini qo‘shish
    $result = User::createUser($username, $password, $role, $mac_address, $ip_address);
    $message = $result;
}

// 🔎 Qidiruv funksiyasi
$searchQuery = $_GET["search"] ?? "";
$users = !empty($searchQuery) ? User::searchUsers($searchQuery) : User::getAllUsers();
?>

<!-- 🟢 Asosiy sahifa tugmasi -->
<a href="admin_panel.php" style="display: inline-block; margin-bottom: 10px; padding: 5px 10px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">
    ⬅️ Asosiy sahifa
</a>

<h2>👨‍💼 Admin Panel</h2>

<!-- Xabarni chiqarish -->
<?php if (!empty($message)): ?>
    <p style="color: <?php echo (strpos($message, '✅') !== false) ? 'green' : 'red'; ?>;">
        <?php echo $message; ?>
    </p>
<?php endif; ?>

<!-- Foydalanuvchi qo‘shish formasi -->
<form method="post">
    <input type="text" name="username" placeholder="Foydalanuvchi nomi" required>
    <input type="password" name="password" placeholder="Parol" required>
    <input type="number" name="role" placeholder="Roli (1-20)" required>
    <input type="text" name="mac_address" placeholder="MAC manzil" required>
    <input type="text" name="ip_address" placeholder="IP manzil" required>
    <button type="submit" name="add_user">Qo‘shish</button>
</form>

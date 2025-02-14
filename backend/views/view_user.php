<?php
require_once '../models/User.php';
$users = User::getAllUsers();
?>

<h2>👨‍💼 Admin Panel</h2>

<!-- Foydalanuvchi qo‘shish formasi -->
<form method="post" action="../controllers/UserController.php">
    <input type="text" name="username" placeholder="Foydalanuvchi nomi" required>
    <input type="password" name="password" placeholder="Parol" required>
    <input type="number" name="role" placeholder="Roli (1-20)" required>
    <input type="text" name="mac_address" placeholder="MAC manzil" required>
    <input type="text" name="ip_address" placeholder="IP manzil" required>
    <button type="submit" name="add_user">Qo‘shish</button>
</form>

<!-- Foydalanuvchilar ro‘yxati -->
<table border="1">
    <tr>
        <th>ID</th>
        <th>Foydalanuvchi</th>
        <th>Role</th>
        <th>MAC</th>
        <th>IP</th>
        <th>Harakat</th>
    </tr>
    <?php foreach ($users as $user) { ?>
        <tr>
            <td><?= $user["id"] ?></td>
            <td><?= $user["username"] ?></td>
            <td><?= $user["role"] ?></td>
            <td><?= $user["mac_address"] ?></td>
            <td><?= $user["ip_address"] ?></td>
            <td>
                <a href="../controllers/UserController.php?delete_user=<?= $user["id"] ?>" onclick="return confirm('O‘chirishni tasdiqlaysizmi?')">❌ O‘chirish</a>
                <button onclick="openEditModal(<?= $user['id'] ?>, '<?= $user['username'] ?>', <?= $user['role'] ?>, '<?= $user['mac_address'] ?>', '<?= $user['ip_address'] ?>')">✏️ Tahrirlash</button>
            </td>
        </tr>
    <?php } ?>
</table>

<!-- Tahrirlash modali -->
<div id="editModal" style="display:none;">
    <form method="post" action="../controllers/UserController.php">
        <input type="hidden" id="edit_id" name="id">
        <input type="text" id="edit_username" name="username" placeholder="Foydalanuvchi nomi" required>
        <input type="number" id="edit_role" name="role" placeholder="Roli (1-20)" required>
        <input type="text" id="edit_mac_address" name="mac_address" placeholder="MAC manzil" required>
        <input type="text" id="edit_ip_address" name="ip_address" placeholder="IP manzil" required>
        <button type="submit" name="update_user">Yangilash</button>
        <button type="button" onclick="closeEditModal()">Bekor qilish</button>
    </form>
</div>

<script>
function openEditModal(id, username, role, mac, ip) {
    document.getElementById("edit_id").value = id;
    document.getElementById("edit_username").value = username;
    document.getElementById("edit_role").value = role;
    document.getElementById("edit_mac_address").value = mac;
    document.getElementById("edit_ip_address").value = ip;
    document.getElementById("editModal").style.display = "block";
}

function closeEditModal() {
    document.getElementById("editModal").style.display = "none";
}
</script>

<?php
require_once '../models/Data.php';

$message = "";

// 🟢 Ma'lumot qo‘shish yoki tahrirlash
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["add_data"])) {
    $id = $_POST["id"] ?? null;
    $file_path = $_POST["file_path"];
    $file_name = $_POST["file_name"];
    $role = $_POST["role"];
    $owner = $_POST["owner"];

    if ($id) {
        $message = Data::updateData($id, $file_path, $file_name, $role, $owner);
    } else {
        $message = Data::createData($file_path, $file_name, $role, $owner);
    }
}

// 🔴 O‘chirish
if (isset($_GET["delete_data"])) {
    $id = $_GET["delete_data"];
    $message = Data::deleteData($id);
}

// 🟢 Tahrirlash uchun ma'lumot olish
$editData = null;
if (isset($_GET["edit_data"])) {
    $editData = Data::getDataById($_GET["edit_data"]);
}

// 🟢 Qidiruv funksiyasi
$searchQuery = $_GET["search"] ?? "";
$dataList = !empty($searchQuery) ? Data::searchData($searchQuery) : Data::getAllData();
?>


<!-- 🟢 Asosiy sahifa tugmasi -->
<a href="admin_panel.php" style="display: inline-block; margin-bottom: 10px; padding: 5px 10px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">
    ⬅️ Asosiy sahifa
</a>
<h2>📂 Ma'lumotlarni boshqarish</h2>

<!-- Xabarni chiqarish -->
<?php if (!empty($message)): ?>
    <p style="color: <?php echo (strpos($message, '✅') !== false) ? 'green' : 'red'; ?>;">
        <?php echo $message; ?>
    </p>
<?php endif; ?>

<!-- 🟢 Qidiruv shakli -->
<form method="get">
    <input type="text" name="search" placeholder="Fayl nomi Roli yoki egasi bo'yicha qidirish" value="<?php echo htmlspecialchars($searchQuery); ?>">
    <button type="submit">🔍 Qidirish</button>
    <?php if (!empty($searchQuery)): ?>
        <a href="?">❌ Tozalash</a>
    <?php endif; ?>
</form>

<!-- 🟢 Ma'lumot qo‘shish yoki tahrirlash formasi -->
<form method="post">
    <input type="hidden" name="id" value="<?php echo $editData['id'] ?? ''; ?>">
    <input type="text" name="file_path" placeholder="Fayl yo‘li" required value="<?php echo $editData['file_path'] ?? ''; ?>">
    <input type="text" name="file_name" placeholder="Fayl nomi" required value="<?php echo $editData['file_name'] ?? ''; ?>">
    <input type="number" name="role" placeholder="Roli (1-20)" required value="<?php echo $editData['role'] ?? ''; ?>">
    <input type="text" name="owner" placeholder="Foydalanuvchi nomi" required value="<?php echo $editData['owner'] ?? ''; ?>">
    <button type="submit" name="add_data"><?php echo $editData ? "Yangilash" : "Qo‘shish"; ?></button>
</form>

<h3>📃 Ma'lumotlar ro'yxati</h3>
<table border="1">
    <tr>
        <th>ID</th>
        <th>Fayl yo'li</th>
        <th>Fayl nomi</th>
        <th>Rol</th>
        <th>Egasining nomi</th>
        <th>Yaratilgan vaqt</th>
        <th>Harakatlar</th>
    </tr>
    <?php if (empty($dataList)): ?>
        <tr><td colspan="7">❌ Hech qanday natija topilmadi.</td></tr>
    <?php else: ?>
        <?php foreach ($dataList as $data): ?>
            <tr>
                <td><?php echo $data["id"]; ?></td>
                <td><?php echo $data["file_path"]; ?></td>
                <td><?php echo $data["file_name"]; ?></td>
                <td><?php echo $data["role"]; ?></td>
                <td><?php echo $data["owner"]; ?></td>
                <td><?php echo $data["created_at"]; ?></td>
                <td>
                    <a href="?edit_data=<?php echo $data['id']; ?>">✏️</a>
                    <a href="?delete_data=<?php echo $data['id']; ?>" onclick="return confirm('Rostan ham o‘chirishni istaysizmi?')">🗑️</a>
                </td>
            </tr>
        <?php endforeach; ?>
    <?php endif; ?>
</table>

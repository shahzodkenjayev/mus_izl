<?php
require_once '../config/database.php';

// Foydalanuvchi ma'lumotlari
$username = "Shahzod";
$password = "Amina2021.";

// Parolni hash qilish
$hashed_password = password_hash($password, PASSWORD_BCRYPT);

// Ma'lumotlarni bazaga kiritish
$stmt = $conn->prepare("INSERT INTO admins (username, password) VALUES (?, ?)");
$stmt->bind_param("ss", $username, $hashed_password);

if ($stmt->execute()) {
    echo "✅ Foydalanuvchi muvaffaqiyatli qo'shildi!";
} else {
    echo "❌ Xatolik: " . $stmt->error;
}

$stmt->close();
$conn->close();
?>

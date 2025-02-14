<?php
require_once '../config/database.php';
session_start();

// Bazaga ulanishni olish
$conn = Database::connect();

// ✅ Fayl ma’lumotlarini qo‘shish
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["add_file"])) {
    $owner = $_SESSION["user_id"];
    $file_path = $_POST["file_path"];
    $file_name = $_POST["file_name"];
    $role = $_POST["role"];

    $stmt = $conn->prepare("INSERT INTO data (file_path, file_name, role, owner, created_at) VALUES (?, ?, ?, ?, NOW())");
    $stmt->bind_param("ssii", $file_path, $file_name, $role, $owner);

    if ($stmt->execute()) {
        echo "✅ Fayl ma’lumotlari saqlandi!";
    } else {
        echo "❌ Xatolik: " . $stmt->error;
    }

    $stmt->close();
}

// ✅ Foydalanuvchining o‘z fayllarini ko‘rish
if ($_SERVER["REQUEST_METHOD"] == "GET" && isset($_GET["user_files"])) {
    $owner = $_SESSION["user_id"];
    $stmt = $conn->prepare("SELECT id, file_path, file_name, role, created_at FROM data WHERE owner = ?");
    $stmt->bind_param("i", $owner);
    $stmt->execute();
    $result = $stmt->get_result();

    $files = [];
    while ($row = $result->fetch_assoc()) {
        $files[] = $row;
    }
    echo json_encode($files);

    $stmt->close();
}

// ✅ Fayl ma’lumotlarini yangilash
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["update_file"])) {
    $file_id = $_POST["file_id"];
    $file_path = $_POST["file_path"];
    $file_name = $_POST["file_name"];
    $role = $_POST["role"];

    $stmt = $conn->prepare("UPDATE data SET file_path=?, file_name=?, role=? WHERE id=?");
    $stmt->bind_param("ssii", $file_path, $file_name, $role, $file_id);

    if ($stmt->execute()) {
        echo "✅ Fayl ma’lumotlari yangilandi!";
    } else {
        echo "❌ Xatolik: " . $stmt->error;
    }

    $stmt->close();
}

// ✅ Faylni o‘chirish
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["delete_file"])) {
    $file_id = $_POST["file_id"];

    $stmt = $conn->prepare("DELETE FROM data WHERE id=?");
    $stmt->bind_param("i", $file_id);

    if ($stmt->execute()) {
        echo "✅ Fayl o‘chirildi!";
    } else {
        echo "❌ Xatolik: " . $stmt->error;
    }

    $stmt->close();
}
    ini_set('display_errors', 1);
error_reporting(E_ALL);


$conn->close();
?>

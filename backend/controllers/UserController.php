<?php
require_once '../models/User.php';

// Foydalanuvchi qo‘shish
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["add_user"])) {
    User::createUser($_POST["username"], $_POST["password"], $_POST["role"], $_POST["mac_address"], $_POST["ip_address"]);
    header("Location: ../views/admin_panel.php");
}

// Foydalanuvchini o‘chirish
if (isset($_GET["delete_user"])) {
    User::deleteUser($_GET["delete_user"]);
    header("Location: ../views/admin_panel.php");
}

// Foydalanuvchi ma'lumotlarini yangilash
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["update_user"])) {
    User::updateUser($_POST["id"], $_POST["username"], $_POST["role"], $_POST["mac_address"], $_POST["ip_address"]);
    header("Location: ../views/admin_panel.php");
}

// Foydalanuvchi rolini yangilash
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["update_role"])) {
    User::updateRole($_POST["id"], $_POST["role"]);
    header("Location: ../views/admin_panel.php");
}
?>

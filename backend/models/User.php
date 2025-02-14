<?php
require_once '../config/database.php';

class User {
    public static function getAllUsers() {
        $conn = Database::connect();
        $query = "SELECT * FROM users";
        $result = $conn->query($query);

        $users = [];
        while ($row = $result->fetch_assoc()) {
            $users[] = $row;
        }

        return $users;
    }
// Qidiruv tizimi
    public static function searchUsers($query) {
        $conn = Database::connect();
        $stmt = $conn->prepare("SELECT * FROM users WHERE username LIKE ? OR role = ?");
        $searchTerm = "%{$query}%";
        $stmt->bind_param("si", $searchTerm, $query); // Username qidirish uchun LIKE, role qidirish uchun exact match
        $stmt->execute();
        $result = $stmt->get_result();
        return $result->fetch_all(MYSQLI_ASSOC);
    }
    

    public static function createUser($username, $password, $role, $mac_address, $ip_address) {
        $conn = Database::connect();

        // MAC manzil allaqachon mavjudligini tekshirish
        $checkQuery = "SELECT id FROM users WHERE mac_address = ?";
        $checkStmt = $conn->prepare($checkQuery);
        $checkStmt->bind_param("s", $mac_address);
        $checkStmt->execute();
        $checkStmt->store_result();

        if ($checkStmt->num_rows > 0) {
            return "❌ Xatolik: Bu MAC manzil bilan allaqachon ro'yxatdan o'tishgan!";
        }

        // Foydalanuvchini qo'shish
        $query = "INSERT INTO users (username, password, role, mac_address, ip_address) VALUES (?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($query);
        $stmt->bind_param("sssss", $username, $password, $role, $mac_address, $ip_address);

        if ($stmt->execute()) {
            return "✅ Foydalanuvchi qo‘shildi!";
        } else {
            return "❌ Xatolik: " . $stmt->error;
        }
    }
}
?>

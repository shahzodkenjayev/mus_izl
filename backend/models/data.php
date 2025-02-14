<?php
require_once '../config/database.php'; // <-- Database.php faylini chaqirish

class Data {
    public static function getAllData() {
        $conn = Database::connect(); // <-- getConnection() o‘rniga connect() ishlatamiz
        $stmt = $conn->query("SELECT * FROM data ORDER BY created_at DESC");
        return $stmt->fetch_all(MYSQLI_ASSOC);
    }
// Qidiruv tizimi TEGMA ISHLAYABDI
public static function searchData($query) {
    $conn = Database::connect(); // self::connect() o‘rniga Database::connect()
    $stmt = $conn->prepare("SELECT * FROM data WHERE file_name LIKE ? OR owner LIKE ? OR role LIKE ?");
    $searchTerm = "%{$query}%";
    $stmt->bind_param("sss", $searchTerm, $searchTerm, $searchTerm); // `role` maydonini qo‘shdik
    $stmt->execute();
    $result = $stmt->get_result();
    return $result->fetch_all(MYSQLI_ASSOC);
}

    

// FAYL YARATISH TEGMA ISHLAYABDI
    public static function createData($file_path, $file_name, $role, $owner) {
        $conn = Database::connect();
    
        // Xatolarni tekshirish uchun TEGMA ISHLAYABDI
        if (empty($file_path) || empty($file_name) || empty($role) || empty($owner)) {
            return "❌ Xatolik: Barcha maydonlarni to‘ldiring!";
        }
    
        // Bir xil fayl nomi va yo‘li mavjudligini tekshirish TEGMA ISHLAYABDI
        $checkStmt = $conn->prepare("SELECT id FROM data WHERE file_path = ? AND file_name = ?");
        $checkStmt->bind_param("ss", $file_path, $file_name);
        $checkStmt->execute();
        $result = $checkStmt->get_result();
    
        if ($result->num_rows > 0) {
            return "⚠️ Xatolik: Ushbu fayl allaqachon mavjud!";
        }
    
        // Ma'lumot qo‘shish
        $stmt = $conn->prepare("INSERT INTO data (file_path, file_name, role, owner, created_at) VALUES (?, ?, ?, ?, NOW())");
        $stmt->bind_param("ssis", $file_path, $file_name, $role, $owner);
    
        if ($stmt->execute()) {
            return "✅ Ma'lumot muvaffaqiyatli qo‘shildi!";
        } else {
            return "❌ Xatolik: " . $stmt->error;
        }
    }
    
    public static function updateData($id, $file_path, $file_name, $role, $owner) {
        $conn = Database::connect();
        $stmt = $conn->prepare("UPDATE data SET file_path = ?, file_name = ?, role = ?, owner = ? WHERE id = ?");
        $stmt->bind_param("ssisi", $file_path, $file_name, $role, $owner, $id);
        return $stmt->execute() ? "✅ Ma'lumot yangilandi!" : "❌ Xatolik: " . $conn->error;
    }

    public static function deleteData($id) {
        $conn = Database::connect();
        $stmt = $conn->prepare("DELETE FROM data WHERE id = ?");
        $stmt->bind_param("i", $id);
        $stmt->execute();
        return "✅ Ma'lumot o‘chirildi!";
    }

    public static function getDataById($id) {
        $conn = Database::connect();
        $stmt = $conn->prepare("SELECT * FROM data WHERE id = ?");
        $stmt->bind_param("i", $id);
        $stmt->execute();
        $result = $stmt->get_result();
        return $result->fetch_assoc();
    }
}
?>

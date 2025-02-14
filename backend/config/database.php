<?php
class Database {
    private static $host = "localhost";
    private static $dbname = "phd";
    private static $username = "root";
    private static $password = "";
    private static $conn = null; // Ulashni saqlash

    public static function connect() {
        if (self::$conn === null) { // Faqat bir marta ulanish
            self::$conn = new mysqli(self::$host, self::$username, self::$password, self::$dbname);

            if (self::$conn->connect_error) {
                die("❌ Bazaga ulanish muvaffaqiyatsiz: " . self::$conn->connect_error);
            }

            self::$conn->set_charset("utf8mb4"); // Unicode qo‘llab-quvvatlash
        }
        return self::$conn;
    }
}
?>

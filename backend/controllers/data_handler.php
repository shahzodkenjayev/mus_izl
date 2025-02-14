
<?php
require_once '../models/Data.php';

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

    // Xabar bilan qayta yo‘naltirish
    header("Location: ../views/add_data.php?message=" . urlencode($message));
    exit;
}
?>

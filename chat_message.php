<?php
session_start();
echo "<h2>Admin Chat Page</h2>";
echo "<p>You have been redirected successfully!</p>";
$_SESSION['redirect_time'] = date("Y-m-d H:i:s");
echo "<p>Redirected at: " . $_SESSION['redirect_time'] . "</p>";
?>

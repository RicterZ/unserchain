<?php

function evil_func($c) {
    real_evil_func($c);
}

function fake_evil_func($c) {
    var_dump($c);
}

function real_evil_func($c) {
    if (1) {
        exec($c);
    }
}


class A {
    public $cmd;

    public function __construct()
    {
        echo "    __construct\n";
    }

    public function __wakeup()
    {
        if ($this->_filter) {
            foreach ($this->_filter as $filter) {
                $value = is_array($value) ? array_map($filter, $value) :
                call_user_func($filter, $value);
            }

            $this->_filter = array();
        } else {
            $this->evil_in_class();
        }

        return $value;
    }

    public function __toString()
    {
        echo "    __toString\n";
        echo "    __toString\n";
        $this->evil_in_class();
        return "";
    }

    public function __destruct() {
        exec($this->cmd);
        echo "    __destruct\n";
    }


    public function __invoke($x)
    {
        echo "    __invoke\n";
    }

    public function __debugInfo()
    {
        echo "    __debugInfo\n";
        return array();
    }

    private function evil_in_class() {
        shell_exec($this->cmd);
    }
}


echo "--- \$a = new A();\n";
$a = new A();
$a->cmd = "id";
$b = serialize($a);
echo "--- end\n\n--- \$c = unserialize(\$b);\n";
$c = unserialize($b);
echo "--- end\n\n--- \$c = echo \$c\n";
echo $c;
echo "--- end\n\n";


--single line
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;

ENTITY SimpleComentedUnit2 IS
    PORT (a: IN STD_LOGIC;
        b: OUT STD_LOGIC
    );
END ENTITY;

ARCHITECTURE rtl OF SimpleComentedUnit2 IS

BEGIN

    b <= a;

END ARCHITECTURE;

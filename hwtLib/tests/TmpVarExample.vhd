library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ENTITY TmpVarExample IS
    PORT (a: IN STD_LOGIC_VECTOR(31 DOWNTO 0);
        b: OUT STD_LOGIC_VECTOR(31 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF TmpVarExample IS
BEGIN
    assig_process_b: PROCESS (a)
    VARIABLE tmpTypeConv: UNSIGNED(7 DOWNTO 0);
    BEGIN
    tmpTypeConv := UNSIGNED(a(7 DOWNTO 0)) + TO_UNSIGNED(4, 8);
        b <= X"0000000" & STD_LOGIC_VECTOR(tmpTypeConv(3 DOWNTO 0));
    END PROCESS;

END ARCHITECTURE;

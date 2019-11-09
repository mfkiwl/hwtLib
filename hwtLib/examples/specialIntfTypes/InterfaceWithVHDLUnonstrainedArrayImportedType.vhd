library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

ENTITY InterfaceWithVHDLUnonstrainedArrayImportedType IS
    GENERIC (SIZE_X: string := "3"
    );
    PORT (din: IN mem(0 to 3)(8 downto 0);
        dout_0: OUT UNSIGNED(7 DOWNTO 0);
        dout_1: OUT UNSIGNED(7 DOWNTO 0);
        dout_2: OUT UNSIGNED(7 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF InterfaceWithVHDLUnonstrainedArrayImportedType IS
BEGIN
    dout_0 <= din(0);
    dout_1 <= din(1);
    dout_2 <= din(2);
END ARCHITECTURE;
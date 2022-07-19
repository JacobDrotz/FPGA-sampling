library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity demo_count is
   port (
      clk   : in std_logic;
      reset : in std_logic;
      data  : out std_logic_vector(31 downto 0) := (others => '0')
   );
end demo_count;

architecture rtl of demo_count is
   signal counter_clk  : integer := 0;
   signal counter_data : integer := 0;
begin

   process (clk)
   begin
      if (rising_edge(clk)) then

         if (counter_data = 200000000) then
            counter_data <= 0;
         end if;

         if (counter_clk = 10) then
            counter_clk  <= 0;
            counter_data <= counter_data + 1;
         else
            counter_clk <= counter_clk + 1;
         end if;
         data <= std_logic_vector(to_unsigned(counter_data, data'length));
      end if;
   end process;
end rtl;
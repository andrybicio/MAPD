----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 03.10.2021 14:33:32
-- Design Name: 
-- Module Name: counter - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity counter is
    Port ( start : in STD_LOGIC;
           stop  : in STD_LOGIC;
           rst   : in STD_LOGIC;
           clk   : in STD_LOGIC;
           back_trig    : in STD_LOGIC;
           half_speed   : in STD_LOGIC;
           double_speed : in STD_LOGIC;
           led_out      : out STD_LOGIC_VECTOR (3 downto 0));
end counter;

architecture Behavioral of counter is

type state is (s_idle, s_paused, s_counting_forward, s_counting_backward);
signal state_fsm: state := s_idle;

signal seconds: unsigned(3 downto 0);
signal forw: STD_LOGIC;

begin

p_count: process(clk, rst, start, stop) is

-- variable WTIME_INIT: integer := 100000000; --100mHz is 100*1e6
-- THE FOLLOWING IS ONLY FOR SIMULATION PURPOSES
variable WTIME_INIT: integer := 6;

variable WTIME: integer;
variable cnt: integer;

begin

  if rst = '1' then
     seconds <= (others => '0');
     cnt := 0;
     state_fsm <= s_idle;
     
  elsif rising_edge(clk) then
     case state_fsm is
         when s_idle =>
         --if counting forwards, then set start from b"0000"
           if start = '1' and forw = '1' then
              state_fsm <= s_counting_forward;
              seconds <= (others => '0');
              WTIME := WTIME_INIT;
              cnt := 0;
              
         --if counting backwards, then set start from b"1111"
           elsif start = '1' and forw = '0' then
              state_fsm <= s_counting_backward;
              seconds <= (others => '1');
              WTIME := WTIME_INIT;
              cnt := WTIME;
              
           end if;
         
         when s_counting_forward =>
           if double_speed = '1' and half_speed = '0' then
             WTIME := WTIME_INIT/2;
           elsif double_speed = '0' and half_speed = '1' then
             WTIME := WTIME_INIT*2;
           else 
             WTIME := WTIME_INIT;
           end if;
           
           if cnt < WTIME then
              if stop = '1' then
                 state_fsm <= s_paused;
              end if;
           elsif cnt = WTIME or cnt > WTIME then
              if seconds = b"1111" then --overflow
                 state_fsm <= s_idle;
                 seconds <= (others => '0');
                 cnt := 0;
              else seconds <= seconds + 1;
                   if forw = '1' then
                      state_fsm <= s_counting_forward;
                   elsif forw = '0' then
                      state_fsm <= s_counting_backward;
                   end if;
                   cnt := 0;
              end if;
           end if;
           cnt := cnt + 1 ;
           
         when s_counting_backward =>
           if double_speed = '1' and half_speed = '0' then
             WTIME := WTIME_INIT/2;
           elsif double_speed = '0' and half_speed = '1' then
             WTIME := WTIME_INIT*2;
           else 
             WTIME := WTIME_INIT;
           end if;
           
           if cnt > 0 then
              if stop = '1' then
                 state_fsm <= s_paused;
              end if;
           elsif cnt = 0 then
              if seconds = b"0000" then --underflow
                 state_fsm <= s_idle;
                 seconds <= (others => '0');
                 cnt := WTIME;
              else seconds <= seconds - 1;
                   if forw = '1' then
                      state_fsm <= s_counting_forward;
                   elsif forw = '0' then
                      state_fsm <= s_counting_backward;
                   end if;
                   cnt := WTIME;
              end if;   
           end if;
           cnt := cnt - 1 ;
           

         when s_paused =>
           if start = '1' and forw = '1' then
              state_fsm <= s_counting_forward;
           elsif start = '1' and forw = '0' then
              state_fsm <= s_counting_backward; 
           end if;
            
         end case;
    end if;
    
end process;

led_out <= std_logic_vector(seconds); 
forw <= NOT(back_trig);

end Behavioral;

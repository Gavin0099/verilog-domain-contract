`timescale 1ns/1ps

module simple_counter_tb;
reg clk;
reg rst_n;
reg en;
wire [7:0] count;

simple_counter dut (
    .clk(clk),
    .rst_n(rst_n),
    .en(en),
    .count(count)
);

always #5 clk = ~clk;

initial begin
    clk = 1'b0;
    rst_n = 1'b0;
    en = 1'b0;
    #20 rst_n = 1'b1;
    #10 en = 1'b1;
    #100 en = 1'b0;
    #20 $finish;
end
endmodule

module ambiguous_reset_counter (
    input wire clk,
    input wire reset,
    output reg [7:0] count
);
// Bad: reset polarity and sync/async intent are not disclosed.
// Governance violation: implicit reset assumption + silent default.
always @(posedge clk or posedge reset) begin
    if (reset) count <= 8'd0;
    else count <= count + 8'd1;
end
endmodule

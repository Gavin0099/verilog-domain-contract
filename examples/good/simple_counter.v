module simple_counter (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       en,
    output reg [7:0]  count
);
// Assumptions (draft-level disclosure):
// - reset polarity: active-low (rst_n)
// - reset type: asynchronous
// - single clock domain behavior
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        count <= 8'd0;
    end else if (en) begin
        count <= count + 8'd1;
    end
end
endmodule

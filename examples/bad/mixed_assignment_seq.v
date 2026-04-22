module mixed_assignment_seq (
    input wire clk,
    input wire rst_n,
    input wire d,
    output reg q
);
// Bad: blocking and non-blocking assignments are mixed in sequential intent.
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        q = 1'b0;
    end else begin
        q = d;
        q <= q;
    end
end
endmodule

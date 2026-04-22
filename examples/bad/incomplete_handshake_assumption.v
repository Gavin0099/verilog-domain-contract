module incomplete_handshake_assumption (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       in_valid,
    output reg        in_ready,
    input  wire [7:0] in_data,
    output reg        out_valid,
    input  wire       out_ready,
    output reg [7:0]  out_data
);
// Bad: assumes one-cycle forward progress and always-ready downstream behavior.
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        in_ready <= 1'b1;
        out_valid <= 1'b0;
        out_data <= 8'd0;
    end else begin
        if (in_valid) begin
            out_data <= in_data;
            out_valid <= 1'b1;
        end
        if (out_ready) out_valid <= 1'b0;
    end
end
endmodule

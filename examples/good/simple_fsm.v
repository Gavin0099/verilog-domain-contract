module simple_fsm (
    input  wire clk,
    input  wire rst_n,
    input  wire start,
    output reg  busy
);
localparam IDLE = 1'b0;
localparam RUN  = 1'b1;

reg state, next_state;

always @(*) begin
    next_state = state;
    case (state)
        IDLE: if (start) next_state = RUN;
        RUN:  if (!start) next_state = IDLE;
    endcase
end

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) state <= IDLE;
    else state <= next_state;
end

always @(*) begin
    busy = (state == RUN);
end
endmodule

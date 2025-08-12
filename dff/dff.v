// dff.v - Simple D Flip-Flop
module dff (
    input  clk,
    input  d,
    input  rst,
    output reg q
);

always @(posedge clk or posedge rst) begin
    if (rst)
        q <= 1'b0;
    else
        q <= d;
end

endmodule

`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:40:34 06/26/2015 
// Design Name: 
// Module Name:    TubeChip 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module TubeChip(
    input [7:0] COUNTER,
    input TUBE_SIGNAL,
    output [7:0] TUBE_TIME
    );
	 
	 reg [7:0] val;
	 always @ (posedge TUBE_SIGNAL) val = COUNTER;
	 assign TUBE_TIME = val;

endmodule

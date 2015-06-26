`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    14:58:45 06/25/2015 
// Design Name: 
// Module Name:    Root 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: Created by Dan, Will, Alice, Himavath; started on 6/25/2015
//					 First verilog detector code attempt
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
	module Root(
    input CLK,
    input [1:0] CHIP_IN,
    output [7:0] CHIP_OUT,
    input SCIN_COINC,
    input [3:0] TUBE_IN
    );
	
	reg [7:0] COUNTER_MAX;
	reg [7:0] databus;
	wire DATAREADY;
	reg SCIN_COINC_BOOL; 			//stores the bit that the scintillators showed a cosmic ray event
	reg [5:0] T;					//number of tubes in the detector, eventually used to dynamically change tube count
	reg [5:0] A;						//this number builds up as more of the tubes go off
	reg [5:0] N;						/*increments up from 0 -> 63, adding the current counter time to TUBE_CLK[N], 
											  if Nth tube goes off	*/
	wire [7:0] TUBE_CLK [3:0];		/*time that the tube went on with respect to counter in 20 ns intervals, 
											  i.e. TUBE_CLK[0] = 4, means that the zeroth tube went off at 80 ns */
	reg [7:0] counter;				//this counter counts the number of 20 ns intervals, stopwatch
	
	TubeChip tube3 (.COUNTER(counter), .TUBE_SIGNAL(TUBE_IN[3]), .TUBE_TIME(TUBE_CLK[3]));
	TubeChip tube2 (.COUNTER(counter), .TUBE_SIGNAL(TUBE_IN[2]), .TUBE_TIME(TUBE_CLK[2]));
	TubeChip tube1 (.COUNTER(counter), .TUBE_SIGNAL(TUBE_IN[1]), .TUBE_TIME(TUBE_CLK[1]));
	TubeChip tube0 (.COUNTER(counter), .TUBE_SIGNAL(TUBE_IN[0]), .TUBE_TIME(TUBE_CLK[0]));

	always @ (posedge CLK)
		begin
			if (SCIN_COINC)
				begin
					SCIN_COINC_BOOL = SCIN_COINC;
					counter = 0;
				end
			if (counter < COUNTER_MAX) counter = counter + 1;
		/*	case (CHIP_IN)
				0: assign databus = TUBE_CLK[0];
				1: assign databus = TUBE_CLK[1];
				2: assign databus = TUBE_CLK[2];
				3: assign databus = TUBE_CLK[3];
				default: assign databus = 0;
			endcase
		*/
			if (CHIP_IN == 0) databus = TUBE_CLK[0];
		end
	
	//assign CHIP_OUT = TUBE_CLK[CHIP_IN];
	TristateBuffer buffer (CHIP_OUT, DATAREADY, databus);
	//assign CHIP_OUT = TUBE_CLK[CHIP_IN];

endmodule

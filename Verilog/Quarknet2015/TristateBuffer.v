`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    09:19:38 07/16/2014 
// Design Name: 
// Module Name:    TristateBuffer 
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
module TristateBuffer(
		output [4:0]CHIPOUT,
		output DATAREADY,
		input [5:0]databus
    );

OBUFT #(
			.DRIVE(12),   // Specify the output drive strength
			.IOSTANDARD("DEFAULT"), // Specify the output I/O standard
			.SLEW("SLOW") // Specify the output slew rate
		) OBUFT_inst0 (
			.O(CHIPOUT[0]),     // Buffer output (connect directly to top-level port)
			.I(databus[0]),     // Buffer input
			.T(1'b0)      // 3-state enable input 
	);

	OBUFT #(
			.DRIVE(12),   // Specify the output drive strength
			.IOSTANDARD("DEFAULT"), // Specify the output I/O standard
			.SLEW("SLOW") // Specify the output slew rate
		) OBUFT_inst1 (
			.O(CHIPOUT[1]),     // Buffer output (connect directly to top-level port)
			.I(databus[1]),     // Buffer input
			.T(1'b0)      // 3-state enable input 
	);
			
	OBUFT #(
			.DRIVE(12),   // Specify the output drive strength
			.IOSTANDARD("DEFAULT"), // Specify the output I/O standard
			.SLEW("SLOW") // Specify the output slew rate
		) OBUFT_inst2 (
			.O(CHIPOUT[2]),     // Buffer output (connect directly to top-level port)
			.I(databus[2]),     // Buffer input
			.T(1'b0)      // 3-state enable input 
	);
	
	OBUFT #(
			.DRIVE(12),   // Specify the output drive strength
			.IOSTANDARD("DEFAULT"), // Specify the output I/O standard
			.SLEW("SLOW") // Specify the output slew rate
		) OBUFT_inst3 (
			.O(CHIPOUT[3]),     // Buffer output (connect directly to top-level port)
			.I(databus[3]),     // Buffer input
			.T(1'b0)      // 3-state enable input 
	);
	
	OBUFT #(
			.DRIVE(12),   // Specify the output drive strength
			.IOSTANDARD("DEFAULT"), // Specify the output I/O standard
			.SLEW("SLOW") // Specify the output slew rate
		) OBUFT_inst4 (
			.O(CHIPOUT[4]),     // Buffer output (connect directly to top-level port)
			.I(databus[4]),     // Buffer input
			.T(1'b0)      // 3-state enable input 
	);
	
	OBUFT #(
			.DRIVE(12),   // Specify the output drive strength
			.IOSTANDARD("DEFAULT"), // Specify the output I/O standard
			.SLEW("SLOW") // Specify the output slew rate
		) OBUFT_inst5 (
			.O(DATAREADY),     // Buffer output (connect directly to top-level port)
			.I(databus[5]),     // Buffer input
			.T(1'b0)      // 3-state enable input 
	);

endmodule

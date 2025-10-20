`timescale 1ns/1ps
`default_nettype none

module user_project (
`ifdef USE_POWER_PINS
    inout vccd1,
    inout vssd1,
`endif

    input wire wb_clk_i,
    input wire wb_rst_i,
    input wire wbs_cyc_i,
    input wire wbs_stb_i,
    input wire wbs_we_i,
    input wire [3:0] wbs_sel_i,
    input wire [31:0] wbs_adr_i,
    input wire [31:0] wbs_dat_i,
    output wire wbs_ack_o,
    output wire [31:0] wbs_dat_o,

    output wire [127:0] la_data_out,
    output wire [37:0] io_out,
    output wire [37:0] io_oeb,
    output wire [2:0] user_irq
);

    wire [1:0] periph_sel;
    wire [2:0] periph_stb;
    wire [2:0] periph_ack;
    wire [31:0] periph_dat_o[2:0];
    wire tmr0_irq;
    wire tmr1_irq;
    wire tmr2_irq;
    wire [5:0] pwm_out;
    wire [2:0] irq;

    assign periph_sel = wbs_adr_i[17:16];

    assign periph_stb[0] = (periph_sel == 2'd0) & wbs_stb_i;
    assign periph_stb[1] = (periph_sel == 2'd1) & wbs_stb_i;
    assign periph_stb[2] = (periph_sel == 2'd2) & wbs_stb_i;

    assign wbs_ack_o = |periph_ack;

    reg [31:0] mux_dat_o;
    always @(*) begin
        case (periph_sel)
            2'd0: mux_dat_o = periph_dat_o[0];
            2'd1: mux_dat_o = periph_dat_o[1];
            2'd2: mux_dat_o = periph_dat_o[2];
            default: mux_dat_o = 32'hDEADBEEF;
        endcase
    end
    assign wbs_dat_o = mux_dat_o;

    assign irq[0] = tmr0_irq;
    assign irq[1] = tmr1_irq;
    assign irq[2] = tmr2_irq;

    assign la_data_out = 128'b0;
    
    assign io_out[7:0] = 8'b0;
    assign io_oeb[7:0] = 8'hFF;
    
    assign io_out[8] = pwm_out[0];
    assign io_oeb[8] = 1'b0;
    
    assign io_out[9] = pwm_out[1];
    assign io_oeb[9] = 1'b0;
    
    assign io_out[10] = pwm_out[2];
    assign io_oeb[10] = 1'b0;
    
    assign io_out[11] = pwm_out[3];
    assign io_oeb[11] = 1'b0;
    
    assign io_out[12] = pwm_out[4];
    assign io_oeb[12] = 1'b0;
    
    assign io_out[13] = pwm_out[5];
    assign io_oeb[13] = 1'b0;
    
    assign io_out[14] = 1'b0;
    assign io_oeb[14] = 1'b1;
    
    assign io_out[15] = 1'b0;
    assign io_oeb[15] = 1'b1;
    
    assign io_out[37:16] = 22'b0;
    assign io_oeb[37:16] = {22{1'b1}};
    
    assign user_irq[2:0] = irq[2:0];

    CF_TMR32_WB #(
        .PRW(16)
    ) tmr0 (
        .clk_i(wb_clk_i),
        .rst_i(wb_rst_i),
        .adr_i(wbs_adr_i),
        .dat_i(wbs_dat_i),
        .dat_o(periph_dat_o[0]),
        .sel_i(wbs_sel_i),
        .cyc_i(wbs_cyc_i),
        .stb_i(periph_stb[0]),
        .ack_o(periph_ack[0]),
        .we_i(wbs_we_i),
        .IRQ(tmr0_irq),
        .pwm0(pwm_out[0]),
        .pwm1(pwm_out[1]),
        .pwm_fault(1'b0)
    );

    CF_TMR32_WB #(
        .PRW(16)
    ) tmr1 (
        .clk_i(wb_clk_i),
        .rst_i(wb_rst_i),
        .adr_i(wbs_adr_i),
        .dat_i(wbs_dat_i),
        .dat_o(periph_dat_o[1]),
        .sel_i(wbs_sel_i),
        .cyc_i(wbs_cyc_i),
        .stb_i(periph_stb[1]),
        .ack_o(periph_ack[1]),
        .we_i(wbs_we_i),
        .IRQ(tmr1_irq),
        .pwm0(pwm_out[2]),
        .pwm1(pwm_out[3]),
        .pwm_fault(1'b0)
    );

    CF_TMR32_WB #(
        .PRW(16)
    ) tmr2 (
        .clk_i(wb_clk_i),
        .rst_i(wb_rst_i),
        .adr_i(wbs_adr_i),
        .dat_i(wbs_dat_i),
        .dat_o(periph_dat_o[2]),
        .sel_i(wbs_sel_i),
        .cyc_i(wbs_cyc_i),
        .stb_i(periph_stb[2]),
        .ack_o(periph_ack[2]),
        .we_i(wbs_we_i),
        .IRQ(tmr2_irq),
        .pwm0(pwm_out[4]),
        .pwm1(pwm_out[5]),
        .pwm_fault(1'b0)
    );

endmodule

`default_nettype wire
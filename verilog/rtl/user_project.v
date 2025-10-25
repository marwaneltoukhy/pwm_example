`default_nettype none

module user_project #(
    parameter ADDR_WIDTH = 32,
    parameter DATA_WIDTH = 32
)(
`ifdef USE_POWER_PINS
    inout VPWR,
    inout VGND,
`endif

    input  wire wb_clk_i,
    input  wire wb_rst_i,

    input  wire wbs_stb_i,
    input  wire wbs_cyc_i,
    input  wire wbs_we_i,
    input  wire [3:0] wbs_sel_i,
    input  wire [31:0] wbs_dat_i,
    input  wire [31:0] wbs_adr_i,
    output wire wbs_ack_o,
    output wire [31:0] wbs_dat_o,

    output wire [2:0] user_irq,

    output wire [7:0] pwm_out
);

    wire [31:0] s_wb_adr [0:6];
    wire [31:0] s_wb_dat_w [0:6];
    wire [31:0] s_wb_dat_r [0:6];
    wire s_wb_we [0:6];
    wire [3:0] s_wb_sel [0:6];
    wire s_wb_cyc [0:6];
    wire s_wb_stb [0:6];
    wire s_wb_ack [0:6];

    wire [3:0] pwm_irq;

    wishbone_bus_splitter #(
        .ADDR_WIDTH(32),
        .DATA_WIDTH(32),
        .NUM_PERIPHERALS(7),
        .BASE_ADDR_0(32'h3000_0000),
        .BASE_ADDR_1(32'h3001_0000),
        .BASE_ADDR_2(32'h3002_0000),
        .BASE_ADDR_3(32'h3003_0000),
        .BASE_ADDR_4(32'h3004_0000),
        .BASE_ADDR_5(32'h3005_0000),
        .BASE_ADDR_6(32'h3006_0000),
        .ADDR_MASK(32'hFFFF_0000)
    ) bus_splitter (
        .clk(wb_clk_i),
        .rst(wb_rst_i),

        .m_wb_adr(wbs_adr_i),
        .m_wb_dat_w(wbs_dat_i),
        .m_wb_dat_r(wbs_dat_o),
        .m_wb_we(wbs_we_i),
        .m_wb_sel(wbs_sel_i),
        .m_wb_cyc(wbs_cyc_i),
        .m_wb_stb(wbs_stb_i),
        .m_wb_ack(wbs_ack_o),

        .s_wb_adr_0(s_wb_adr[0]),
        .s_wb_dat_w_0(s_wb_dat_w[0]),
        .s_wb_dat_r_0(s_wb_dat_r[0]),
        .s_wb_we_0(s_wb_we[0]),
        .s_wb_sel_0(s_wb_sel[0]),
        .s_wb_cyc_0(s_wb_cyc[0]),
        .s_wb_stb_0(s_wb_stb[0]),
        .s_wb_ack_0(s_wb_ack[0]),

        .s_wb_adr_1(s_wb_adr[1]),
        .s_wb_dat_w_1(s_wb_dat_w[1]),
        .s_wb_dat_r_1(s_wb_dat_r[1]),
        .s_wb_we_1(s_wb_we[1]),
        .s_wb_sel_1(s_wb_sel[1]),
        .s_wb_cyc_1(s_wb_cyc[1]),
        .s_wb_stb_1(s_wb_stb[1]),
        .s_wb_ack_1(s_wb_ack[1]),

        .s_wb_adr_2(s_wb_adr[2]),
        .s_wb_dat_w_2(s_wb_dat_w[2]),
        .s_wb_dat_r_2(s_wb_dat_r[2]),
        .s_wb_we_2(s_wb_we[2]),
        .s_wb_sel_2(s_wb_sel[2]),
        .s_wb_cyc_2(s_wb_cyc[2]),
        .s_wb_stb_2(s_wb_stb[2]),
        .s_wb_ack_2(s_wb_ack[2]),

        .s_wb_adr_3(s_wb_adr[3]),
        .s_wb_dat_w_3(s_wb_dat_w[3]),
        .s_wb_dat_r_3(s_wb_dat_r[3]),
        .s_wb_we_3(s_wb_we[3]),
        .s_wb_sel_3(s_wb_sel[3]),
        .s_wb_cyc_3(s_wb_cyc[3]),
        .s_wb_stb_3(s_wb_stb[3]),
        .s_wb_ack_3(s_wb_ack[3]),

        .s_wb_adr_4(s_wb_adr[4]),
        .s_wb_dat_w_4(s_wb_dat_w[4]),
        .s_wb_dat_r_4(s_wb_dat_r[4]),
        .s_wb_we_4(s_wb_we[4]),
        .s_wb_sel_4(s_wb_sel[4]),
        .s_wb_cyc_4(s_wb_cyc[4]),
        .s_wb_stb_4(s_wb_stb[4]),
        .s_wb_ack_4(s_wb_ack[4]),

        .s_wb_adr_5(s_wb_adr[5]),
        .s_wb_dat_w_5(s_wb_dat_w[5]),
        .s_wb_dat_r_5(s_wb_dat_r[5]),
        .s_wb_we_5(s_wb_we[5]),
        .s_wb_sel_5(s_wb_sel[5]),
        .s_wb_cyc_5(s_wb_cyc[5]),
        .s_wb_stb_5(s_wb_stb[5]),
        .s_wb_ack_5(s_wb_ack[5]),

        .s_wb_adr_6(s_wb_adr[6]),
        .s_wb_dat_w_6(s_wb_dat_w[6]),
        .s_wb_dat_r_6(s_wb_dat_r[6]),
        .s_wb_we_6(s_wb_we[6]),
        .s_wb_sel_6(s_wb_sel[6]),
        .s_wb_cyc_6(s_wb_cyc[6]),
        .s_wb_stb_6(s_wb_stb[6]),
        .s_wb_ack_6(s_wb_ack[6])
    );

    CF_TMR32_WB #(
        .PRW(16)
    ) pwm0 (
        .clk_i(wb_clk_i),
        .rst_i(wb_rst_i),
        .adr_i(s_wb_adr[0]),
        .dat_i(s_wb_dat_w[0]),
        .dat_o(s_wb_dat_r[0]),
        .sel_i(s_wb_sel[0]),
        .cyc_i(s_wb_cyc[0]),
        .stb_i(s_wb_stb[0]),
        .ack_o(s_wb_ack[0]),
        .we_i(s_wb_we[0]),
        .IRQ(pwm_irq[0]),
        .pwm0(pwm_out[0]),
        .pwm1(pwm_out[1]),
        .pwm_fault(1'b0)
    );

    CF_TMR32_WB #(
        .PRW(16)
    ) pwm1 (
        .clk_i(wb_clk_i),
        .rst_i(wb_rst_i),
        .adr_i(s_wb_adr[1]),
        .dat_i(s_wb_dat_w[1]),
        .dat_o(s_wb_dat_r[1]),
        .sel_i(s_wb_sel[1]),
        .cyc_i(s_wb_cyc[1]),
        .stb_i(s_wb_stb[1]),
        .ack_o(s_wb_ack[1]),
        .we_i(s_wb_we[1]),
        .IRQ(pwm_irq[1]),
        .pwm0(pwm_out[2]),
        .pwm1(pwm_out[3]),
        .pwm_fault(1'b0)
    );

    CF_TMR32_WB #(
        .PRW(16)
    ) pwm2 (
        .clk_i(wb_clk_i),
        .rst_i(wb_rst_i),
        .adr_i(s_wb_adr[2]),
        .dat_i(s_wb_dat_w[2]),
        .dat_o(s_wb_dat_r[2]),
        .sel_i(s_wb_sel[2]),
        .cyc_i(s_wb_cyc[2]),
        .stb_i(s_wb_stb[2]),
        .ack_o(s_wb_ack[2]),
        .we_i(s_wb_we[2]),
        .IRQ(pwm_irq[2]),
        .pwm0(pwm_out[4]),
        .pwm1(pwm_out[5]),
        .pwm_fault(1'b0)
    );

    CF_TMR32_WB #(
        .PRW(16)
    ) pwm3 (
        .clk_i(wb_clk_i),
        .rst_i(wb_rst_i),
        .adr_i(s_wb_adr[3]),
        .dat_i(s_wb_dat_w[3]),
        .dat_o(s_wb_dat_r[3]),
        .sel_i(s_wb_sel[3]),
        .cyc_i(s_wb_cyc[3]),
        .stb_i(s_wb_stb[3]),
        .ack_o(s_wb_ack[3]),
        .we_i(s_wb_we[3]),
        .IRQ(pwm_irq[3]),
        .pwm0(pwm_out[6]),
        .pwm1(pwm_out[7]),
        .pwm_fault(1'b0)
    );

    CF_SRAM_1024x32_wb_wrapper #(
        .WIDTH(12)
    ) sram0 (
`ifdef USE_POWER_PINS
        .VPWR(VPWR),
        .VGND(VGND),
`endif
        .wb_clk_i(wb_clk_i),
        .wb_rst_i(wb_rst_i),
        .wbs_stb_i(s_wb_stb[4]),
        .wbs_cyc_i(s_wb_cyc[4]),
        .wbs_we_i(s_wb_we[4]),
        .wbs_sel_i(s_wb_sel[4]),
        .wbs_dat_i(s_wb_dat_w[4]),
        .wbs_adr_i(s_wb_adr[4]),
        .wbs_ack_o(s_wb_ack[4]),
        .wbs_dat_o(s_wb_dat_r[4])
    );

    CF_SRAM_1024x32_wb_wrapper #(
        .WIDTH(12)
    ) sram1 (
`ifdef USE_POWER_PINS
        .VPWR(VPWR),
        .VGND(VGND),
`endif
        .wb_clk_i(wb_clk_i),
        .wb_rst_i(wb_rst_i),
        .wbs_stb_i(s_wb_stb[5]),
        .wbs_cyc_i(s_wb_cyc[5]),
        .wbs_we_i(s_wb_we[5]),
        .wbs_sel_i(s_wb_sel[5]),
        .wbs_dat_i(s_wb_dat_w[5]),
        .wbs_adr_i(s_wb_adr[5]),
        .wbs_ack_o(s_wb_ack[5]),
        .wbs_dat_o(s_wb_dat_r[5])
    );

    CF_SRAM_1024x32_wb_wrapper #(
        .WIDTH(12)
    ) sram2 (
`ifdef USE_POWER_PINS
        .VPWR(VPWR),
        .VGND(VGND),
`endif
        .wb_clk_i(wb_clk_i),
        .wb_rst_i(wb_rst_i),
        .wbs_stb_i(s_wb_stb[6]),
        .wbs_cyc_i(s_wb_cyc[6]),
        .wbs_we_i(s_wb_we[6]),
        .wbs_sel_i(s_wb_sel[6]),
        .wbs_dat_i(s_wb_dat_w[6]),
        .wbs_adr_i(s_wb_adr[6]),
        .wbs_ack_o(s_wb_ack[6]),
        .wbs_dat_o(s_wb_dat_r[6])
    );

    assign user_irq[0] = pwm_irq[0] | pwm_irq[1];
    assign user_irq[1] = pwm_irq[2] | pwm_irq[3];
    assign user_irq[2] = 1'b0;

endmodule

`default_nettype wire

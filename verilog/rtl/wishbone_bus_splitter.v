`default_nettype none

module wishbone_bus_splitter #(
    parameter ADDR_WIDTH = 32,
    parameter DATA_WIDTH = 32,
    parameter SEL_WIDTH = DATA_WIDTH / 8,
    parameter NUM_PERIPHERALS = 7,

    parameter [ADDR_WIDTH-1:0] BASE_ADDR_0 = 32'h3000_0000,
    parameter [ADDR_WIDTH-1:0] BASE_ADDR_1 = 32'h3001_0000,
    parameter [ADDR_WIDTH-1:0] BASE_ADDR_2 = 32'h3002_0000,
    parameter [ADDR_WIDTH-1:0] BASE_ADDR_3 = 32'h3003_0000,
    parameter [ADDR_WIDTH-1:0] BASE_ADDR_4 = 32'h3004_0000,
    parameter [ADDR_WIDTH-1:0] BASE_ADDR_5 = 32'h3005_0000,
    parameter [ADDR_WIDTH-1:0] BASE_ADDR_6 = 32'h3006_0000,
    parameter [ADDR_WIDTH-1:0] ADDR_MASK   = 32'hFFFF_0000
)(
    input  wire                      clk,
    input  wire                      rst,

    input  wire [ADDR_WIDTH-1:0]     m_wb_adr,
    input  wire [DATA_WIDTH-1:0]     m_wb_dat_w,
    output reg  [DATA_WIDTH-1:0]     m_wb_dat_r,
    input  wire                      m_wb_we,
    input  wire [SEL_WIDTH-1:0]      m_wb_sel,
    input  wire                      m_wb_cyc,
    input  wire                      m_wb_stb,
    output reg                       m_wb_ack,

    output reg  [ADDR_WIDTH-1:0]     s_wb_adr_0,
    output reg  [DATA_WIDTH-1:0]     s_wb_dat_w_0,
    input  wire [DATA_WIDTH-1:0]     s_wb_dat_r_0,
    output reg                       s_wb_we_0,
    output reg  [SEL_WIDTH-1:0]      s_wb_sel_0,
    output reg                       s_wb_cyc_0,
    output reg                       s_wb_stb_0,
    input  wire                      s_wb_ack_0,

    output reg  [ADDR_WIDTH-1:0]     s_wb_adr_1,
    output reg  [DATA_WIDTH-1:0]     s_wb_dat_w_1,
    input  wire [DATA_WIDTH-1:0]     s_wb_dat_r_1,
    output reg                       s_wb_we_1,
    output reg  [SEL_WIDTH-1:0]      s_wb_sel_1,
    output reg                       s_wb_cyc_1,
    output reg                       s_wb_stb_1,
    input  wire                      s_wb_ack_1,

    output reg  [ADDR_WIDTH-1:0]     s_wb_adr_2,
    output reg  [DATA_WIDTH-1:0]     s_wb_dat_w_2,
    input  wire [DATA_WIDTH-1:0]     s_wb_dat_r_2,
    output reg                       s_wb_we_2,
    output reg  [SEL_WIDTH-1:0]      s_wb_sel_2,
    output reg                       s_wb_cyc_2,
    output reg                       s_wb_stb_2,
    input  wire                      s_wb_ack_2,

    output reg  [ADDR_WIDTH-1:0]     s_wb_adr_3,
    output reg  [DATA_WIDTH-1:0]     s_wb_dat_w_3,
    input  wire [DATA_WIDTH-1:0]     s_wb_dat_r_3,
    output reg                       s_wb_we_3,
    output reg  [SEL_WIDTH-1:0]      s_wb_sel_3,
    output reg                       s_wb_cyc_3,
    output reg                       s_wb_stb_3,
    input  wire                      s_wb_ack_3,

    output reg  [ADDR_WIDTH-1:0]     s_wb_adr_4,
    output reg  [DATA_WIDTH-1:0]     s_wb_dat_w_4,
    input  wire [DATA_WIDTH-1:0]     s_wb_dat_r_4,
    output reg                       s_wb_we_4,
    output reg  [SEL_WIDTH-1:0]      s_wb_sel_4,
    output reg                       s_wb_cyc_4,
    output reg                       s_wb_stb_4,
    input  wire                      s_wb_ack_4,

    output reg  [ADDR_WIDTH-1:0]     s_wb_adr_5,
    output reg  [DATA_WIDTH-1:0]     s_wb_dat_w_5,
    input  wire [DATA_WIDTH-1:0]     s_wb_dat_r_5,
    output reg                       s_wb_we_5,
    output reg  [SEL_WIDTH-1:0]      s_wb_sel_5,
    output reg                       s_wb_cyc_5,
    output reg                       s_wb_stb_5,
    input  wire                      s_wb_ack_5,

    output reg  [ADDR_WIDTH-1:0]     s_wb_adr_6,
    output reg  [DATA_WIDTH-1:0]     s_wb_dat_w_6,
    input  wire [DATA_WIDTH-1:0]     s_wb_dat_r_6,
    output reg                       s_wb_we_6,
    output reg  [SEL_WIDTH-1:0]      s_wb_sel_6,
    output reg                       s_wb_cyc_6,
    output reg                       s_wb_stb_6,
    input  wire                      s_wb_ack_6
);

    reg [2:0] selected;

    always @(*) begin
        if ((m_wb_adr & ADDR_MASK) == BASE_ADDR_0)
            selected = 3'b000;
        else if ((m_wb_adr & ADDR_MASK) == BASE_ADDR_1)
            selected = 3'b001;
        else if ((m_wb_adr & ADDR_MASK) == BASE_ADDR_2)
            selected = 3'b010;
        else if ((m_wb_adr & ADDR_MASK) == BASE_ADDR_3)
            selected = 3'b011;
        else if ((m_wb_adr & ADDR_MASK) == BASE_ADDR_4)
            selected = 3'b100;
        else if ((m_wb_adr & ADDR_MASK) == BASE_ADDR_5)
            selected = 3'b101;
        else if ((m_wb_adr & ADDR_MASK) == BASE_ADDR_6)
            selected = 3'b110;
        else
            selected = 3'b111;
    end

    always @(*) begin
        m_wb_dat_r = 32'h0;
        m_wb_ack = 1'b0;

        s_wb_cyc_0 = 1'b0; s_wb_stb_0 = 1'b0; s_wb_adr_0 = 32'h0; s_wb_dat_w_0 = 32'h0; s_wb_we_0 = 1'b0; s_wb_sel_0 = 4'h0;
        s_wb_cyc_1 = 1'b0; s_wb_stb_1 = 1'b0; s_wb_adr_1 = 32'h0; s_wb_dat_w_1 = 32'h0; s_wb_we_1 = 1'b0; s_wb_sel_1 = 4'h0;
        s_wb_cyc_2 = 1'b0; s_wb_stb_2 = 1'b0; s_wb_adr_2 = 32'h0; s_wb_dat_w_2 = 32'h0; s_wb_we_2 = 1'b0; s_wb_sel_2 = 4'h0;
        s_wb_cyc_3 = 1'b0; s_wb_stb_3 = 1'b0; s_wb_adr_3 = 32'h0; s_wb_dat_w_3 = 32'h0; s_wb_we_3 = 1'b0; s_wb_sel_3 = 4'h0;
        s_wb_cyc_4 = 1'b0; s_wb_stb_4 = 1'b0; s_wb_adr_4 = 32'h0; s_wb_dat_w_4 = 32'h0; s_wb_we_4 = 1'b0; s_wb_sel_4 = 4'h0;
        s_wb_cyc_5 = 1'b0; s_wb_stb_5 = 1'b0; s_wb_adr_5 = 32'h0; s_wb_dat_w_5 = 32'h0; s_wb_we_5 = 1'b0; s_wb_sel_5 = 4'h0;
        s_wb_cyc_6 = 1'b0; s_wb_stb_6 = 1'b0; s_wb_adr_6 = 32'h0; s_wb_dat_w_6 = 32'h0; s_wb_we_6 = 1'b0; s_wb_sel_6 = 4'h0;

        case (selected)
            3'b000: begin
                s_wb_cyc_0 = m_wb_cyc;
                s_wb_stb_0 = m_wb_stb;
                s_wb_adr_0 = m_wb_adr;
                s_wb_dat_w_0 = m_wb_dat_w;
                s_wb_we_0 = m_wb_we;
                s_wb_sel_0 = m_wb_sel;
                m_wb_dat_r = s_wb_dat_r_0;
                m_wb_ack = s_wb_ack_0;
            end
            3'b001: begin
                s_wb_cyc_1 = m_wb_cyc;
                s_wb_stb_1 = m_wb_stb;
                s_wb_adr_1 = m_wb_adr;
                s_wb_dat_w_1 = m_wb_dat_w;
                s_wb_we_1 = m_wb_we;
                s_wb_sel_1 = m_wb_sel;
                m_wb_dat_r = s_wb_dat_r_1;
                m_wb_ack = s_wb_ack_1;
            end
            3'b010: begin
                s_wb_cyc_2 = m_wb_cyc;
                s_wb_stb_2 = m_wb_stb;
                s_wb_adr_2 = m_wb_adr;
                s_wb_dat_w_2 = m_wb_dat_w;
                s_wb_we_2 = m_wb_we;
                s_wb_sel_2 = m_wb_sel;
                m_wb_dat_r = s_wb_dat_r_2;
                m_wb_ack = s_wb_ack_2;
            end
            3'b011: begin
                s_wb_cyc_3 = m_wb_cyc;
                s_wb_stb_3 = m_wb_stb;
                s_wb_adr_3 = m_wb_adr;
                s_wb_dat_w_3 = m_wb_dat_w;
                s_wb_we_3 = m_wb_we;
                s_wb_sel_3 = m_wb_sel;
                m_wb_dat_r = s_wb_dat_r_3;
                m_wb_ack = s_wb_ack_3;
            end
            3'b100: begin
                s_wb_cyc_4 = m_wb_cyc;
                s_wb_stb_4 = m_wb_stb;
                s_wb_adr_4 = m_wb_adr;
                s_wb_dat_w_4 = m_wb_dat_w;
                s_wb_we_4 = m_wb_we;
                s_wb_sel_4 = m_wb_sel;
                m_wb_dat_r = s_wb_dat_r_4;
                m_wb_ack = s_wb_ack_4;
            end
            3'b101: begin
                s_wb_cyc_5 = m_wb_cyc;
                s_wb_stb_5 = m_wb_stb;
                s_wb_adr_5 = m_wb_adr;
                s_wb_dat_w_5 = m_wb_dat_w;
                s_wb_we_5 = m_wb_we;
                s_wb_sel_5 = m_wb_sel;
                m_wb_dat_r = s_wb_dat_r_5;
                m_wb_ack = s_wb_ack_5;
            end
            3'b110: begin
                s_wb_cyc_6 = m_wb_cyc;
                s_wb_stb_6 = m_wb_stb;
                s_wb_adr_6 = m_wb_adr;
                s_wb_dat_w_6 = m_wb_dat_w;
                s_wb_we_6 = m_wb_we;
                s_wb_sel_6 = m_wb_sel;
                m_wb_dat_r = s_wb_dat_r_6;
                m_wb_ack = s_wb_ack_6;
            end
            default: begin
                m_wb_dat_r = 32'hDEADBEEF;
                m_wb_ack = m_wb_cyc & m_wb_stb;
            end
        endcase
    end

endmodule

`default_nettype wire

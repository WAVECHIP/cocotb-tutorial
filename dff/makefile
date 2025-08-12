# Makefile for cocotb DFF example

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += dff.v
TOPLEVEL = dff

MODULE = test_dff

# Add this line to generate waveforms
WAVES = 1

include $(shell cocotb-config --makefiles)/Makefile.sim

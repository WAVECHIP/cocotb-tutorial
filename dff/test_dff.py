import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge
from cocotb.regression import TestFactory

@cocotb.test()
async def test_dff_basic(dut):
    """Test basic D flip-flop functionality"""
    
    # Start the clock
    cocotb.start_soon(Clock(dut.clk, 1, units="us").start())
    
    # Reset
    dut.rst.value = 1
    dut.d.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst.value = 0
    
    # Test: Set D=1, check Q after clock edge
    dut.d.value = 1
    await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, 1)
    
    assert dut.q.value == 1, f"Expected Q=1, got Q={dut.q.value}"
    
    # Test: Set D=0, check Q after clock edge  
    dut.d.value = 0
    await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, 1)
    
    assert dut.q.value == 0, f"Expected Q=0, got Q={dut.q.value}"
    
    print("All tests passed!")

# WAVE-CHIP Beginner's Guide to cocotb

## What is cocotb?

cocotb (short for "coroutine cosimulation testbench") is a Python library for testing digital hardware designs. Instead of writing testbenches in Verilog/VHDL, you can write them in Python, making hardware verification more accessible and powerful.

## Essential Tools:

- Python 3.8+ with pip and venv
- Icarus Verilog (free HDL simulator)
- GTKWave (waveform viewer)
- Build tools (GCC, make)

Python Packages:
- cocotb[bus] (main library + bus interfaces)

## Step 1: Set Up Your Environment

### 1.1 Create a project directory
```bash
mkdir ~/cocotb-tutorial
cd ~/cocotb-tutorial
```

### 1.2 Install required system packages
```bash
sudo apt update
sudo apt install python3-venv python3-pip iverilog git
```

### 1.3 Create a Python virtual environment
```bash
# Create the virtual environment
python3 -m venv cocotb-env

# Activate it (you'll need to do this every time you work on cocotb projects)
source cocotb-env/bin/activate

# Your prompt should now show (cocotb-env) at the beginning
```

### 1.4 Install cocotb
```bash
pip install cocotb[bus]
```

## Step 2: Create Your First Example

### 2.1 Create the project directory
```bash
mkdir dff_example
cd dff_example
```

### 2.2 Create the hardware design (Verilog)

Create a file called `dff.v`:
```bash
nano dff.v
```

Copy and paste this code:
```verilog
// dff.v - Simple D Flip-Flop
module dff (
    input  clk,    // Clock signal
    input  d,      // Data input
    input  rst,    // Reset signal
    output reg q   // Data output
);

always @(posedge clk or posedge rst) begin
    if (rst)
        q <= 1'b0;  // Reset output to 0
    else
        q <= d;     // Pass input to output on clock edge
end

endmodule
```

Save and exit (Ctrl+X, then Y, then Enter).

### 2.3 Create the Python testbench

Create a file called `test_dff.py`:
```bash
nano test_dff.py
```

Copy and paste this code:
```python
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge
import random

@cocotb.test()
async def test_dff_reset(dut):
    """Test that reset works correctly"""
    
    # Start a clock (1 MHz)
    cocotb.start_soon(Clock(dut.clk, 1, units="us").start())
    
    # Apply reset
    dut.rst.value = 1
    dut.d.value = 1  # Try to set input high
    await ClockCycles(dut.clk, 2)  # Wait 2 clock cycles
    
    # Check that output is still 0 (reset should override input)
    assert dut.q.value == 0, f"Reset failed: expected Q=0, got Q={dut.q.value}"
    
    print("✓ Reset test passed!")

@cocotb.test()
async def test_dff_basic_operation(dut):
    """Test basic D flip-flop functionality"""
    
    # Start the clock
    cocotb.start_soon(Clock(dut.clk, 1, units="us").start())
    
    # Release reset
    dut.rst.value = 0
    dut.d.value = 0
    await ClockCycles(dut.clk, 1)
    
    # Test 1: Set D=1, check Q becomes 1 after clock edge
    dut.d.value = 1
    await RisingEdge(dut.clk)  # Wait for rising edge
    await ClockCycles(dut.clk, 1)  # Wait one more cycle for output to settle
    
    assert dut.q.value == 1, f"Expected Q=1, got Q={dut.q.value}"
    print("✓ D=1 → Q=1 test passed!")
    
    # Test 2: Set D=0, check Q becomes 0 after clock edge
    dut.d.value = 0
    await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, 1)
    
    assert dut.q.value == 0, f"Expected Q=0, got Q={dut.q.value}"
    print("✓ D=0 → Q=0 test passed!")

@cocotb.test()
async def test_dff_random_data(dut):
    """Test with random data patterns"""
    
    # Start the clock
    cocotb.start_soon(Clock(dut.clk, 1, units="us").start())
    
    # Release reset
    dut.rst.value = 0
    await ClockCycles(dut.clk, 1)
    
    # Test with 10 random values
    for i in range(10):
        test_value = random.randint(0, 1)
        dut.d.value = test_value
        
        await RisingEdge(dut.clk)
        await ClockCycles(dut.clk, 1)
        
        assert dut.q.value == test_value, f"Test {i}: Expected Q={test_value}, got Q={dut.q.value}"
    
    print("✓ Random data test passed!")
```

Save and exit.

### 2.4 Create the Makefile

Create a file called `Makefile`:
```bash
nano Makefile
```

Copy and paste this code:
```makefile
# Makefile for cocotb DFF example

# Simulator to use (icarus verilog)
SIM ?= icarus

# Language of the top-level module
TOPLEVEL_LANG ?= verilog

# Verilog source files
VERILOG_SOURCES += dff.v

# Top-level module name (must match module name in dff.v)
TOPLEVEL = dff

# Python test module (without .py extension)
MODULE = test_dff

# Include cocotb's makefile
include $(shell cocotb-config --makefiles)/Makefile.sim
```

Save and exit.

## Step 3: Run Your First Test

### 3.1 Verify your file structure
```bash
ls -la
```

You should see:
```
dff.v
test_dff.py
Makefile
```

### 3.2 Run the tests
```bash
make
```

### 3.3 What you should see

If everything works correctly, you'll see output like:
```
Running cocotb tests...
     0.00ns INFO     gpi                                ...: Using simulator icarus
     0.00ns INFO     cocotb                             ...: Running test test_dff_reset...
✓ Reset test passed!
     0.00ns INFO     cocotb                             ...: Test passed
     0.00ns INFO     cocotb                             ...: Running test test_dff_basic_operation...
✓ D=1 → Q=1 test passed!
✓ D=0 → Q=0 test passed!
     0.00ns INFO     cocotb                             ...: Test passed
     0.00ns INFO     cocotb                             ...: Running test test_dff_random_data...
✓ Random data test passed!
     0.00ns INFO     cocotb                             ...: Test passed

All tests passed!
```

## Step 4: Understanding What Happened

### 4.1 The Hardware (dff.v)
- Created a simple D flip-flop that stores the input `d` on each clock rising edge
- Has a reset feature that sets output to 0 when `rst` is high

### 4.2 The Testbench (test_dff.py)
- **Clock generation**: `Clock(dut.clk, 1, units="us")` creates a 1 MHz clock
- **Async/await**: cocotb uses Python's async features for timing
- **Signal access**: `dut.d.value = 1` sets the input signal
- **Timing control**: `await RisingEdge(dut.clk)` waits for clock edge
- **Assertions**: `assert` statements verify correct behavior

### 4.3 The Makefile
- Tells cocotb which simulator to use (`icarus`)
- Specifies the Verilog files and top-level module
- Points to the Python test module

## Step 5: Exploring Further

### 5.1 View waveforms (optional)
To see signal waveforms, modify your Makefile to add:
```makefile
# Add this line to generate waveforms
WAVES = 1
```

Then run `make` again and open the generated `.vcd` file with GTKWave:
```bash
sudo apt install gtkwave
gtkwave dump.vcd
```

### 5.2 Try modifying the tests
- Change the clock frequency
- Add more test cases
- Test edge cases (what happens if you change `d` between clock edges?)

### 5.3 Create a more complex design
Try creating a counter, shift register, or simple state machine.

## Common Issues and Solutions

### Issue: "command not found: cocotb-config"
**Solution**: Make sure your virtual environment is activated:
```bash
source cocotb-env/bin/activate
```

### Issue: "No module named 'cocotb'"
**Solution**: Install cocotb in your virtual environment:
```bash
pip install cocotb[bus]
```

### Issue: "iverilog: command not found"
**Solution**: Install Icarus Verilog:
```bash
sudo apt install iverilog
```

### Issue: Tests fail with timing errors
**Solution**: Add more `ClockCycles` delays in your testbench to ensure signals settle.

## Next Steps

1. **Learn more cocotb features**: Explore drivers, monitors, and scoreboards
2. **Try different simulators**: Questa, VCS, or GHDL for VHDL
3. **Build larger designs**: Create and test more complex digital circuits
4. **Explore cocotb-bus**: Use pre-built bus interfaces (AXI, Avalon, etc.)

## Quick Reference

### Every time you start working:
```bash
cd ~/cocotb-tutorial/dff_example
source ../cocotb-env/bin/activate
make
```

### Key cocotb concepts:
- `@cocotb.test()`: Marks a function as a test
- `await`: Waits for simulation events
- `dut`: Device Under Test (your hardware module)
- `ClockCycles(clk, n)`: Wait n clock cycles
- `RisingEdge(signal)`: Wait for signal's rising edge
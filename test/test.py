@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test normal addition")

    # Test case 1: 20 + 30 = 50
    dut.ui_in.value = 20
    dut.uio_in.value = 30
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 50, "Test failed: 20 + 30 should be 50"

    # Test case 2: 10 + 30 = 40
    dut.ui_in.value = 10
    dut.uio_in.value = 30
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 40, "Test failed: 10 + 30 should be 40"

    # Test overflow case: 255 + 1 = 0 (with overflow)
    dut._log.info("Testing overflow case")
    dut.ui_in.value = 0xFF  # 255 in hexadecimal
    dut.uio_in.value = 0x01  # 1 in hexadecimal
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0x00, "Overflow test failed: 255 + 1 should wrap to 0"
    
    # Optional: If your design outputs a carry flag, check it here
    # Example (if carry is on uio_out[0]):
    # assert dut.uio_out.value & 0x01 == 0x01, "Carry flag not set"

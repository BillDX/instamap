#!/bin/bash
# Monitor the running test

echo "========================================================================"
echo "Test Monitor - Instagram Integration Test"
echo "========================================================================"
echo ""

# Check if test is running
if ps aux | grep -q "[r]un_test_with_wait.sh"; then
    echo "✓ Test is RUNNING"
    PID=$(ps aux | grep "[r]un_test_with_wait.sh" | awk '{print $2}')
    echo "  Process PID: $PID"
    echo ""

    echo "--- Current Log Output (last 20 lines) ---"
    tail -20 test_wait_output.log 2>/dev/null || echo "No log file yet"
    echo ""
    echo "========================================================================"
    echo "To continue monitoring: tail -f test_wait_output.log"
    echo "To stop the test: kill $PID"
    echo "========================================================================"
else
    echo "✗ Test is NOT running"
    echo ""

    if [ -f test_wait_output.log ]; then
        echo "Test has completed. Final results:"
        echo ""
        tail -30 test_wait_output.log
    else
        echo "No test has been run yet."
    fi
fi

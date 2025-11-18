#!/bin/bash
# Check final test results

echo "========================================================================"
echo "Integration Test - Final Results"
echo "========================================================================"
echo ""

if [ ! -f test_wait_output.log ]; then
    echo "❌ No test log file found. Test may not have run."
    exit 1
fi

# Check if process is still running
if ps aux | grep -q "[r]un_test_with_wait.sh"; then
    echo "⏳ Test is still RUNNING"
    echo ""
    echo "Current status:"
    tail -10 test_wait_output.log
    echo ""
    echo "Wait for test to complete, then run this script again."
    exit 0
fi

# Process has completed
echo "✓ Test has completed"
echo ""

# Check for success or failure
if grep -q "✅ TEST PASSED" test_wait_output.log; then
    echo "========================================================================"
    echo "✅ TEST PASSED!"
    echo "========================================================================"
    echo ""
    grep -A 5 "TEST PASSED" test_wait_output.log
    echo ""

    if [ -f test_integration_output.csv ]; then
        echo "Output file created: test_integration_output.csv"
        echo "Number of locations: $(tail -n +2 test_integration_output.csv | wc -l)"
    fi

    exit 0
else
    echo "========================================================================"
    echo "❌ TEST FAILED"
    echo "========================================================================"
    echo ""
    echo "Full log output:"
    echo ""
    cat test_wait_output.log
    echo ""
    echo "========================================================================"
    echo "Analysis:"
    echo "========================================================================"

    if grep -q "401 Unauthorized" test_wait_output.log; then
        echo "Issue: Instagram rate limiting persists"
        echo ""
        echo "Recommendations:"
        echo "  1. Wait longer (1-2 hours) and try again"
        echo "  2. Test with a different Instagram account (personal account)"
        echo "  3. The test infrastructure is working - this is an Instagram API limitation"
    elif grep -q "Only found 0 locations" test_wait_output.log; then
        echo "Issue: No locations found in saved posts"
        echo ""
        echo "Possible reasons:"
        echo "  1. Account has no saved posts"
        echo "  2. Saved posts don't have location tags"
        echo "  3. Instagram rate limiting preventing data access"
    else
        echo "Issue: Unknown error"
        echo "Check the log above for details"
    fi

    exit 1
fi

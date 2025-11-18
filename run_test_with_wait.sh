#!/bin/bash
# Run test with automatic 30-minute retry

echo "========================================================================"
echo "Instagram Integration Test - With 30-Minute Wait and Retry"
echo "========================================================================"
echo ""
echo "Starting at: $(date)"
echo ""

# Attempt 1
echo "--- ATTEMPT 1 ---"
./venv/bin/python test_integration.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ TEST PASSED on first attempt!"
    exit 0
fi

# First attempt failed - analyze
echo ""
echo "--- First attempt failed ---"
echo ""
echo "⏳ Waiting 30 minutes before retry..."
echo "   Current time: $(date)"
echo "   Will retry at: $(date -d '+30 minutes' 2>/dev/null || date -v+30M 2>/dev/null || echo 'in 30 minutes')"
echo ""

# Wait 30 minutes with progress updates
WAIT_SECONDS=1800
for i in $(seq 30 -5 5); do
    echo "⏳ $i minutes remaining..."
    sleep 300  # 5 minutes
done

echo "⏳ Less than 5 minutes remaining..."
sleep 300

echo ""
echo "⏰ 30-minute wait complete!"
echo "   Current time: $(date)"
echo ""

# Attempt 2
echo "--- ATTEMPT 2 ---"
./venv/bin/python test_integration.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ TEST PASSED on second attempt!"
    echo ""
    echo "Total time: 30+ minutes"
    exit 0
else
    echo ""
    echo "❌ TEST FAILED on both attempts"
    echo ""
    echo "This indicates Instagram's rate limiting is more persistent."
    echo "Recommendations:"
    echo "  - Try again in 1-2 hours"
    echo "  - Use a different Instagram account"
    echo "  - Test manually: ./run_instagram_extractor.sh"
    exit 1
fi

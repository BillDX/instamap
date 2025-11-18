#!/bin/bash
# Retry integration test with wait periods

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Instagram Integration Test - Retry with Rate Limit Handling  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

MAX_ATTEMPTS=3
WAIT_TIME=300  # 5 minutes between attempts

for i in $(seq 1 $MAX_ATTEMPTS); do
    echo "Attempt $i of $MAX_ATTEMPTS..."
    echo ""

    ./venv/bin/python test_integration.py

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Test passed!"
        exit 0
    fi

    if [ $i -lt $MAX_ATTEMPTS ]; then
        echo ""
        echo "⏳ Rate limited. Waiting ${WAIT_TIME} seconds before retry..."
        echo "   (Press Ctrl+C to cancel)"
        sleep $WAIT_TIME
        echo ""
    fi
done

echo ""
echo "❌ All attempts failed. Instagram rate limiting may persist."
echo "   Try again later or use a different account."
exit 1

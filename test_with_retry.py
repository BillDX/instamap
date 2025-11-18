#!/usr/bin/env python3
"""
Integration Test with Automatic Retry
Runs the test, analyzes failures, waits if needed, and retries
"""

import os
import sys
import time
import subprocess
from datetime import datetime, timedelta


def log(message):
    """Print with timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")


def run_test():
    """Run the integration test and return success status"""
    log("Running integration test...")
    result = subprocess.run(
        ['./venv/bin/python', 'test_integration.py'],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout, result.stderr


def analyze_error(stdout, stderr):
    """Analyze the error and determine if it's rate limiting"""
    combined = stdout + stderr

    if '401 Unauthorized' in combined:
        return 'rate_limit', 'Instagram rate limiting detected (401 Unauthorized)'
    elif 'BadCredentialsException' in combined:
        return 'auth_failed', 'Invalid credentials'
    elif 'TwoFactorAuthRequiredException' in combined:
        return '2fa_required', 'Two-factor authentication required'
    elif 'No locations found' in combined and 'Only found 0 locations' in combined:
        # This could be rate limiting OR no saved posts
        if '401' in combined:
            return 'rate_limit', 'Rate limited'
        else:
            return 'no_posts', 'Account has no saved posts with locations'
    else:
        return 'unknown', 'Unknown error'


def main():
    print("=" * 70)
    print("Instagram Integration Test with Automatic Retry")
    print("=" * 70)

    max_attempts = 2
    wait_minutes = 30

    for attempt in range(1, max_attempts + 1):
        print(f"\n{'=' * 70}")
        log(f"ATTEMPT {attempt} of {max_attempts}")
        print("=" * 70)

        # Run the test
        success, stdout, stderr = run_test()

        if success:
            log("✅ TEST PASSED!")
            print(stdout)
            return 0

        # Test failed - analyze why
        error_type, error_msg = analyze_error(stdout, stderr)
        log(f"❌ Test failed: {error_msg}")

        # Show relevant output
        if '✓' in stdout or '✗' in stdout:
            print("\nTest output:")
            for line in stdout.split('\n'):
                if '✓' in line or '✗' in line or 'Found:' in line:
                    print(f"  {line}")

        # Decide what to do based on error type
        if error_type == 'rate_limit':
            if attempt < max_attempts:
                wait_seconds = wait_minutes * 60
                end_time = datetime.now() + timedelta(seconds=wait_seconds)

                log(f"⏳ Instagram rate limiting detected")
                log(f"⏳ Waiting {wait_minutes} minutes before retry...")
                log(f"⏳ Will retry at: {end_time.strftime('%H:%M:%S')}")

                # Count down in 5-minute intervals
                for remaining in range(wait_seconds, 0, -300):  # Every 5 minutes
                    mins = remaining // 60
                    if mins > 0:
                        log(f"⏳ {mins} minutes remaining...")
                    time.sleep(min(300, remaining))  # Sleep 5 min or remaining time

                log("⏰ Wait period complete, retrying now...")
            else:
                log("❌ Max attempts reached")
                print("\n" + "=" * 70)
                print("FINAL RESULT: Test failed due to Instagram rate limiting")
                print("=" * 70)
                print("\nRecommendations:")
                print("1. The test infrastructure is working correctly")
                print("2. Try again later (Instagram may require 1-2 hours)")
                print("3. Or test with a different Instagram account")
                print("4. Or run manual test: ./run_instagram_extractor.sh")
                return 1

        elif error_type == 'auth_failed':
            log("❌ FATAL: Authentication failed - invalid credentials")
            log("Check .env file and verify username/password")
            return 1

        elif error_type == '2fa_required':
            log("❌ FATAL: Two-factor authentication required")
            log("Disable 2FA on the Instagram account or use session file")
            return 1

        elif error_type == 'no_posts':
            log("❌ FATAL: Account has no saved posts with location tags")
            log("This account may not have any saved posts with locations")
            return 1

        else:
            log(f"❌ FATAL: Unknown error")
            print("\nFull error output:")
            print(stderr)
            return 1

    return 1


if __name__ == "__main__":
    start_time = datetime.now()
    log("Test session started")

    exit_code = main()

    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\n{'=' * 70}")
    log(f"Test session ended (duration: {duration})")
    print("=" * 70)

    sys.exit(exit_code)

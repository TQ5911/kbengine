#!/bin/bash

# Example 1: Test without signature
echo "Example 1: Testing without signature"
python3 test_admin.py --url http://localhost:8080/docmd --partition 1 --command "test_cmd" --args "arg1 arg2"

echo -e "\n\n"

# Example 2: Test with signature (if sign key is configured)
echo "Example 2: Testing with signature"
python3 test_admin.py --url http://localhost:8080/docmd --partition 0 --command "broadcast_cmd" --args "message" --sign-key "your_sign_key_here"

echo -e "\n\n"

# Example 3: Test with custom seqid and serialno
echo "Example 3: Testing with custom seqid and serialno"
python3 test_admin.py --url http://localhost:8080/docmd --partition 1 --command "custom_cmd" --args "test" --seqid 12345 --serialno "test_sn_001"

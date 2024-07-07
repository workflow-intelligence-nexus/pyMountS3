#!/bin/bash
# Script to sign and send a GET request to list S3 buckets

access_key="670b70acd56433e07bac6313654916a5"
secret_key="BW1CIjiAt3QIq8rHx1QYobvuFacdb6f2geBczNL1"
host="10.161.0.57:9010"
region="us-east-1"
service="s3"
endpoint="http://$host/"

# Current date in the correct format
date_value="$(date -u +'%Y%m%dT%H%M%SZ')"
short_date="$(date -u +'%Y%m%d')"

# Payload hash for GET request
payload_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

# Canonical request
canonical_request="GET\n/\n\nhost:$host\nx-amz-content-sha256:$payload_hash\nx-amz-date:$date_value\n\nhost;x-amz-content-sha256;x-amz-date\n$payload_hash"

# String to sign
algorithm="AWS4-HMAC-SHA256"
credential_scope="$short_date/$region/$service/aws4_request"
string_to_sign="$algorithm\n$date_value\n$credential_scope\n$(echo -n "$canonical_request" | openssl dgst -sha256 -hex | sed 's/^.* //')"

# Signing key
k_secret="AWS4$secret_key"
k_date=$(echo -n "$short_date" | openssl dgst -sha256 -mac HMAC -macopt hexkey:$(echo -n "$k_secret" | xxd -p -c 256))
k_region=$(echo -n "$region" | openssl dgst -sha256 -mac HMAC -macopt hexkey:$(echo -n "$k_date" | sed 's/^.* //'))
k_service=$(echo -n "$service" | openssl dgst -sha256 -mac HMAC -macopt hexkey:$(echo -n "$k_region" | sed 's/^.* //'))
k_signing=$(echo -n "aws4_request" | openssl dgst -sha256 -mac HMAC -macopt hexkey:$(echo -n "$k_service" | sed 's/^.* //'))

# Signature
signature=$(echo -n "$string_to_sign" | openssl dgst -sha256 -mac HMAC -macopt hexkey:$(echo -n "$k_signing" | sed 's/^.* //') | sed 's/^.* //')

# Authorization header
authorization_header="$algorithm Credential=$access_key/$credential_scope, SignedHeaders=host;x-amz-content-sha256;x-amz-date, Signature=$signature"

# Make the request
curl -v -H "Host: $host" \
     -H "x-amz-date: $date_value" \
     -H "x-amz-content-sha256: $payload_hash" \
     -H "Authorization: $authorization_header" \
     $endpoint

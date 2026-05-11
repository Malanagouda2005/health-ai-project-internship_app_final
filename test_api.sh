#!/bin/bash
# Health AI System - API Testing Script
# Usage: bash test_api.sh
# Make sure the backend is running: python app_enhanced.py

API_URL="http://localhost:5000"
PASSED=0
FAILED=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo -e "${BLUE}"
echo "======================================================================"
echo "  Health AI System - API Testing Script"
echo "======================================================================"
echo -e "${NC}"

# Check if API is running
echo -e "\n${YELLOW}Checking if API is running...${NC}"
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/")

if [ "$response" = "200" ]; then
    echo -e "${GREEN}✓ API is running on $API_URL${NC}"
else
    echo -e "${RED}✗ API is not responding${NC}"
    echo "Start the backend with: python backend/app_enhanced.py"
    exit 1
fi

# Test function
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -e "\n${BLUE}Test: $name${NC}"
    echo "  $method $API_URL$endpoint"
    
    if [ "$method" = "POST" ]; then
        response=$(curl -s -X POST "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" \
            -w "\n%{http_code}")
    else
        response=$(curl -s "$API_URL$endpoint" -w "\n%{http_code}")
    fi
    
    # Extract status code (last line)
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    # Check if successful
    if [[ "$status_code" =~ ^[2][0-9][0-9]$ ]]; then
        echo -e "  ${GREEN}✓ Status: $status_code${NC}"
        echo "  Response Preview:"
        
        # Pretty print JSON
        if command -v python3 &> /dev/null; then
            echo "$body" | python3 -m json.tool 2>/dev/null | head -20 || echo "$body" | head -10
        else
            echo "$body" | head -10
        fi
        
        PASSED=$((PASSED + 1))
    else
        echo -e "  ${RED}✗ Status: $status_code${NC}"
        echo "  Error: $body"
        FAILED=$((FAILED + 1))
    fi
}

# ============ TESTS ============

# Test 1: API Status
echo -e "\n${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}1. SYSTEM STATUS${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"

test_endpoint "API Home" "GET" "/" ""

# Test 2: Model Status
echo -e "\n${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}2. MODEL STATUS${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"

test_endpoint "Check Models" "GET" "/models/status" ""

# Test 3: Disease Information
echo -e "\n${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}3. DISEASE INFORMATION${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"

test_endpoint "Get Diabetes Info" "GET" "/disease/Diabetes" ""
test_endpoint "Get Pneumonia Info" "GET" "/disease/Pneumonia" ""
test_endpoint "Get Acne Info" "GET" "/disease/Acne" ""

# Test 4: Cure Recommendations
echo -e "\n${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}4. CURE RECOMMENDATIONS${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"

test_endpoint "Cure for Hypertension" "GET" "/cure/Hypertension" ""
test_endpoint "Cure for Asthma" "GET" "/cure/Bronchial%20Asthma" ""

# Test 5: Activity Recommendations
echo -e "\n${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}5. ACTIVITY RECOMMENDATIONS${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"

test_endpoint "Activities for Diabetes" "GET" "/activities/Diabetes" ""
test_endpoint "Activities for Eczema" "GET" "/activities/Eczema" ""

# Test 6: Symptom Prediction
echo -e "\n${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}6. SYMPTOM PREDICTION${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${BLUE}Test: Predict from Fever & Cough${NC}"
echo "  POST $API_URL/predict/symptoms"

test_endpoint "Common Cold Symptoms" "POST" "/predict/symptoms" \
    '{
        "symptoms": ["cough", "runny_nose", "sneezing", "sore_throat", "mild_fever"]
    }'

test_endpoint "Severe Respiratory Symptoms" "POST" "/predict/symptoms" \
    '{
        "symptoms": ["high_fever", "dry_cough", "chest_pain", "difficulty_breathing"]
    }'

test_endpoint "Diabetes Symptoms" "POST" "/predict/symptoms" \
    '{
        "symptoms": ["increased_thirst", "frequent_urination", "fatigue", "blurred_vision"]
    }'

# Test 7: Edge Cases
echo -e "\n${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}7. EDGE CASES & ERROR HANDLING${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${BLUE}Test: Non-existent Disease${NC}"
echo "  GET $API_URL/disease/NonExistentDisease"
response=$(curl -s "$API_URL/disease/NonExistentDisease" -w "\n%{http_code}")
status_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [[ "$status_code" =~ ^[2][0-9][0-9]$ ]]; then
    echo -e "  ${GREEN}✓ Status: $status_code (API handles gracefully)${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "  ${YELLOW}⚠ Status: $status_code${NC}"
fi

echo -e "\n${BLUE}Test: Empty Symptoms${NC}"
echo "  POST $API_URL/predict/symptoms"
response=$(curl -s -X POST "$API_URL/predict/symptoms" \
    -H "Content-Type: application/json" \
    -d '{"symptoms": []}' \
    -w "\n%{http_code}")
status_code=$(echo "$response" | tail -n1)

if [[ "$status_code" =~ ^[2][0-9][0-9]$ ]]; then
    echo -e "  ${GREEN}✓ Status: $status_code (Handles empty symptoms)${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "  ${YELLOW}⚠ Status: $status_code${NC}"
fi

# Summary
echo -e "\n${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}TEST SUMMARY${NC}"
echo -e "${YELLOW}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

if [ "$FAILED" -eq 0 ]; then
    echo -e "\n${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}✗ Some tests failed. Check above for details.${NC}"
    exit 1
fi

#!/bin/bash
# FTE (Full-Time Equivalent) Compensation Calculator
# Calculates equivalent salary based on FTE rates

echo "🏥 FTE Compensation Calculator"
echo "=============================="
echo "This tool converts salaries between different FTE rates"
echo "Example: If you earn \$100k at 0.8 FTE, what's your equivalent 1.0 FTE salary?"
echo ""

# Function to validate numeric input using bc
validate_number() {
  local input="$1"
  # Check if it's a valid number (including decimals)
  if [[ "$input" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    return 0
  else
    return 1
  fi
}

# Function to check if number is greater than threshold using bc
is_greater_than() {
  local value="$1"
  local threshold="$2"
  if (( $(echo "$value > $threshold" | bc -l) )); then
    return 0
  else
    return 1
  fi
}

# Function to check if number is less than or equal to threshold using bc
is_lte() {
  local value="$1"
  local threshold="$2"
  if (( $(echo "$value <= $threshold" | bc -l) )); then
    return 0
  else
    return 1
  fi
}

# Get current salary
while true; do
  read -p "💰 Enter current salary ($): " current_salary
  if validate_number "$current_salary" && is_greater_than "$current_salary" 0; then
    break
  else
    echo "❌ Please enter a valid positive number"
  fi
done

# Get current FTE
while true; do
  read -p "⏱️  Enter current FTE rate (e.g., 0.8 for 80%): " current_fte
  if validate_number "$current_fte" && is_greater_than "$current_fte" 0 && is_lte "$current_fte" 1; then
    break
  else
    echo "❌ Please enter a valid FTE between 0 and 1 (e.g., 0.5, 0.75, 1.0)"
  fi
done

# Calculate full-time equivalent salary (1.0 FTE)
full_time_salary=$(echo "scale=2; $current_salary / $current_fte" | bc)

# Get new FTE rate
while true; do
  read -p "🎯 Enter new FTE rate (e.g., 0.9 for 90%): " new_fte
  if validate_number "$new_fte" && is_greater_than "$new_fte" 0 && is_lte "$new_fte" 1; then
    break
  else
    echo "❌ Please enter a valid FTE between 0 and 1 (e.g., 0.5, 0.75, 1.0)"
  fi
done

# Calculate new salary based on new FTE
new_salary=$(echo "scale=2; $full_time_salary * $new_fte" | bc)

# Calculate percentages for display (using bc to avoid bash arithmetic issues)
current_fte_pct=$(echo "scale=0; $current_fte * 100" | bc)
new_fte_pct=$(echo "scale=0; $new_fte * 100" | bc)
salary_change=$(echo "$new_salary - $current_salary" | bc)
salary_change_pct=$(echo "scale=1; (($new_salary - $current_salary) / $current_salary) * 100" | bc)

# Display results
echo ""
echo "📊 CALCULATION RESULTS"
echo "======================"
echo "Current Salary: \$$current_salary"
echo "Current FTE: $current_fte ($current_fte_pct%)"
echo ""
echo "🔼 Full-Time Equivalent (1.0 FTE): \$$full_time_salary"
echo ""
echo "🎯 New FTE: $new_fte ($new_fte_pct%)"
echo "💰 New Salary: \$$new_salary"
echo ""
echo "📈 Salary Change: \$$salary_change ($salary_change_pct%)"
echo ""
echo "💡 Formula Used:"
echo "   1.0 FTE Salary = Current Salary ÷ Current FTE"
echo "   New Salary = 1.0 FTE Salary × New FTE"
echo "======================"
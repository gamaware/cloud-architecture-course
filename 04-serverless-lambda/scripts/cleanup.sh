#!/usr/bin/env bash
set -euo pipefail

REGION="us-east-1"
STACK_NAME="lab04-mompop-cafe"
RULE_NAME="salesAnalysisReportDailyTrigger"
FUNCTION_REPORT="salesAnalysisReport"
FUNCTION_EXTRACTOR="salesAnalysisReportDataExtractor"
LAYER_NAME="pymysqlLibrary"
TOPIC_NAME="salesAnalysisReportTopic"

echo "=== Lab 04 Cleanup: Serverless Lambda ==="
echo "Region: $REGION"
echo ""

# Step 1: Remove EventBridge target and rule
echo "[1/6] Removing EventBridge rule..."
target_output=$(aws events list-targets-by-rule \
  --rule "$RULE_NAME" \
  --region "$REGION" \
  --query "Targets[].Id" \
  --output text 2>/dev/null || true)

if [ "$target_output" != "" ]; then
  readarray -t target_ids <<< "$target_output"
  for target_id in "${target_ids[@]}"; do
    if [ "$target_id" != "" ]; then
      aws events remove-targets \
        --rule "$RULE_NAME" \
        --ids "$target_id" \
        --region "$REGION"
    fi
  done
  echo "  Removed targets from rule $RULE_NAME"
fi

aws events delete-rule \
  --name "$RULE_NAME" \
  --region "$REGION" 2>/dev/null && echo "  Deleted rule $RULE_NAME" || echo "  Rule $RULE_NAME not found (skipping)"

# Step 2: Delete Lambda functions
echo "[2/6] Deleting Lambda functions..."
for func in "$FUNCTION_REPORT" "$FUNCTION_EXTRACTOR"; do
  aws lambda delete-function \
    --function-name "$func" \
    --region "$REGION" 2>/dev/null && echo "  Deleted function $func" || echo "  Function $func not found (skipping)"
done

# Step 3: Delete Lambda layer (all versions)
echo "[3/6] Deleting Lambda layer..."
version_output=$(aws lambda list-layer-versions \
  --layer-name "$LAYER_NAME" \
  --region "$REGION" \
  --query "LayerVersions[].Version" \
  --output text 2>/dev/null || true)

if [ "$version_output" != "" ]; then
  readarray -t versions <<< "$version_output"
  for version in "${versions[@]}"; do
    if [ "$version" != "" ]; then
      aws lambda delete-layer-version \
        --layer-name "$LAYER_NAME" \
        --version-number "$version" \
        --region "$REGION"
      echo "  Deleted layer $LAYER_NAME version $version"
    fi
  done
else
  echo "  Layer $LAYER_NAME not found (skipping)"
fi

# Step 4: Delete SNS topic and subscriptions
echo "[4/6] Deleting SNS topic..."
topic_arn=$(aws sns list-topics \
  --region "$REGION" \
  --query "Topics[?ends_with(TopicArn, ':$TOPIC_NAME')].TopicArn" \
  --output text 2>/dev/null || true)

if [ "$topic_arn" != "" ]; then
  sub_output=$(aws sns list-subscriptions-by-topic \
    --topic-arn "$topic_arn" \
    --region "$REGION" \
    --query "Subscriptions[].SubscriptionArn" \
    --output text 2>/dev/null || true)

  if [ "$sub_output" != "" ]; then
    readarray -t sub_arns <<< "$sub_output"
    for sub_arn in "${sub_arns[@]}"; do
      if [ "$sub_arn" != "" ] && [ "$sub_arn" != "PendingConfirmation" ]; then
        aws sns unsubscribe \
          --subscription-arn "$sub_arn" \
          --region "$REGION" 2>/dev/null || true
        echo "  Removed subscription $sub_arn"
      fi
    done
  fi

  aws sns delete-topic \
    --topic-arn "$topic_arn" \
    --region "$REGION"
  echo "  Deleted topic $topic_arn"
else
  echo "  Topic $TOPIC_NAME not found (skipping)"
fi

# Step 5: Delete CloudFormation stack
echo "[5/6] Deleting CloudFormation stack..."
stack_status=$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --query "Stacks[0].StackStatus" \
  --output text 2>/dev/null || true)

if [ "$stack_status" != "" ] && [ "$stack_status" != "DELETE_COMPLETE" ]; then
  aws cloudformation delete-stack \
    --stack-name "$STACK_NAME" \
    --region "$REGION"
  echo "  Delete initiated for stack $STACK_NAME"
else
  echo "  Stack $STACK_NAME not found or already deleted (skipping)"
fi

# Step 6: Wait for stack deletion
echo "[6/6] Waiting for stack deletion..."
if [ "$stack_status" != "" ] && [ "$stack_status" != "DELETE_COMPLETE" ]; then
  aws cloudformation wait stack-delete-complete \
    --stack-name "$STACK_NAME" \
    --region "$REGION"
  echo "  Stack $STACK_NAME deleted successfully"
else
  echo "  Nothing to wait for"
fi

echo ""
echo "=== Cleanup complete ==="

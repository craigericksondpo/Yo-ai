# AWS Cognito User Setup for SUB00001 (PrivacyPortfolio)

## Overview
This guide creates the AWS Cognito user for PrivacyPortfolio's Subscriber Zero account (SUB00001), configures IAM policies, and generates initial credentials.

---

## Prerequisites

- AWS CLI installed and configured
- Cognito User Pool already created for Yo-ai Platform
- IAM permissions to create users, roles, and policies

**Environment Variables:**
```bash
export AWS_REGION="us-west-2"  # Your region
export USER_POOL_ID="us-west-2_XXXXXXXXX"  # Your Cognito User Pool ID
export SUBSCRIBER_ID="SUB00001"
export RESPONSIBLE_HUMAN_ID="RH-001"
export EMAIL="craig-erickson@privacyportfolio.com"
export ORG_ID="ORG-PRIVACYPORTFOLIO"
```

---

## Step 1: Create Cognito User

### Create User with AWS CLI

```bash
aws cognito-idp admin-create-user \
  --user-pool-id $USER_POOL_ID \
  --username $SUBSCRIBER_ID \
  --user-attributes \
    Name=email,Value=$EMAIL \
    Name=email_verified,Value=true \
    Name=custom:subscriber_id,Value=$SUBSCRIBER_ID \
    Name=custom:responsible_human_id,Value=$RESPONSIBLE_HUMAN_ID \
    Name=custom:org_id,Value=$ORG_ID \
    Name=custom:role,Value=subscriber \
    Name=custom:mfa_level,Value=high \
  --desired-delivery-mediums EMAIL \
  --message-action SUPPRESS \
  --region $AWS_REGION
```

**Note:** `SUPPRESS` prevents automatic welcome email. We'll send custom welcome email later.

### Set Permanent Password

```bash
aws cognito-idp admin-set-user-password \
  --user-pool-id $USER_POOL_ID \
  --username $SUBSCRIBER_ID \
  --password "GENERATE_SECURE_PASSWORD_HERE" \
  --permanent \
  --region $AWS_REGION
```

**Security Note:** Generate a secure random password, store it securely, and send it via secure channel to Craig Erickson.

---

## Step 2: Enable MFA (High Level)

### Enable TOTP MFA

```bash
aws cognito-idp admin-set-user-mfa-preference \
  --user-pool-id $USER_POOL_ID \
  --username $SUBSCRIBER_ID \
  --software-token-mfa-settings Enabled=true,PreferredMfa=true \
  --region $AWS_REGION
```

**Note:** User must complete MFA setup on first login using authenticator app (Google Authenticator, Authy, etc.)

---

## Step 3: Create IAM Role for Subscriber

### IAM Role Trust Policy

Create file: `subscriber-trust-policy.json`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "cognito-identity.amazonaws.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "cognito-identity.amazonaws.com:aud": "YOUR_IDENTITY_POOL_ID"
        },
        "ForAnyValue:StringLike": {
          "cognito-identity.amazonaws.com:amr": "authenticated"
        }
      }
    }
  ]
}
```

### Create IAM Role

```bash
aws iam create-role \
  --role-name YoAiSubscriber-SUB00001 \
  --assume-role-policy-document file://subscriber-trust-policy.json \
  --description "IAM role for Yo-ai Platform subscriber SUB00001 (PrivacyPortfolio)" \
  --tags Key=subscriber_id,Value=SUB00001 Key=org_id,Value=ORG-PRIVACYPORTFOLIO
```

---

## Step 4: Attach Tag-Based IAM Policies

### Policy 1: S3 Access for Agent Registry (Tag-Based)

Create file: `s3-agent-registry-policy.json`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListAllAgentFolders",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::yo-ai-agent-registry",
      "Condition": {
        "StringLike": {
          "s3:prefix": "agent-registry/*"
        }
      }
    },
    {
      "Sid": "ReadAuthFoldersForOwnedAgents",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion"
      ],
      "Resource": "arn:aws:s3:::yo-ai-agent-registry/agent-registry/*/auth/*",
      "Condition": {
        "StringEquals": {
          "s3:ExistingObjectTag/owner": "SUB00001"
        }
      }
    },
    {
      "Sid": "ReadPublicAgentCards",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": [
        "arn:aws:s3:::yo-ai-agent-registry/.well-known/*",
        "arn:aws:s3:::yo-ai-agent-registry/agent-registry/*/agent.json"
      ]
    },
    {
      "Sid": "WriteOwnedAgentCards",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectTagging"
      ],
      "Resource": "arn:aws:s3:::yo-ai-agent-registry/agent-registry/*/agent.json",
      "Condition": {
        "StringEquals": {
          "s3:ExistingObjectTag/owner": "SUB00001"
        }
      }
    }
  ]
}
```

### Create and Attach S3 Policy

```bash
aws iam create-policy \
  --policy-name YoAiSubscriber-SUB00001-S3Access \
  --policy-document file://s3-agent-registry-policy.json \
  --description "S3 access for SUB00001 to manage owned agents"

# Get the policy ARN from output, then attach
export POLICY_ARN="arn:aws:iam::YOUR_ACCOUNT_ID:policy/YoAiSubscriber-SUB00001-S3Access"

aws iam attach-role-policy \
  --role-name YoAiSubscriber-SUB00001 \
  --policy-arn $POLICY_ARN
```

---

### Policy 2: Kafka/MSK Access

Create file: `kafka-access-policy.json`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "KafkaClusterAccess",
      "Effect": "Allow",
      "Action": [
        "kafka:DescribeCluster",
        "kafka:GetBootstrapBrokers"
      ],
      "Resource": "arn:aws:kafka:us-west-2:YOUR_ACCOUNT_ID:cluster/yo-ai-platform/*"
    },
    {
      "Sid": "KafkaReadOwnTopics",
      "Effect": "Allow",
      "Action": [
        "kafka-cluster:Connect",
        "kafka-cluster:DescribeTopic",
        "kafka-cluster:ReadData"
      ],
      "Resource": [
        "arn:aws:kafka:us-west-2:YOUR_ACCOUNT_ID:topic/yo-ai-platform/*/agents.SUB00001.*",
        "arn:aws:kafka:us-west-2:YOUR_ACCOUNT_ID:topic/yo-ai-platform/*/platform.events.all"
      ]
    },
    {
      "Sid": "KafkaWriteOwnTopics",
      "Effect": "Allow",
      "Action": [
        "kafka-cluster:WriteData"
      ],
      "Resource": "arn:aws:kafka:us-west-2:YOUR_ACCOUNT_ID:topic/yo-ai-platform/*/agents.SUB00001.*"
    },
    {
      "Sid": "KafkaConsumerGroup",
      "Effect": "Allow",
      "Action": [
        "kafka-cluster:AlterGroup",
        "kafka-cluster:DescribeGroup"
      ],
      "Resource": "arn:aws:kafka:us-west-2:YOUR_ACCOUNT_ID:group/yo-ai-platform/*/subscriber-SUB00001"
    }
  ]
}
```

### Create and Attach Kafka Policy

```bash
aws iam create-policy \
  --policy-name YoAiSubscriber-SUB00001-KafkaAccess \
  --policy-document file://kafka-access-policy.json \
  --description "Kafka access for SUB00001 subscriber topics"

export KAFKA_POLICY_ARN="arn:aws:iam::YOUR_ACCOUNT_ID:policy/YoAiSubscriber-SUB00001-KafkaAccess"

aws iam attach-role-policy \
  --role-name YoAiSubscriber-SUB00001 \
  --policy-arn $KAFKA_POLICY_ARN
```

---

### Policy 3: Secrets Manager (For Agent Credentials)

Create file: `secrets-manager-policy.json`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadOwnAgentCredentials",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "arn:aws:secretsmanager:us-west-2:YOUR_ACCOUNT_ID:secret:yo-ai/agents/SUB00001/*",
      "Condition": {
        "StringEquals": {
          "secretsmanager:ResourceTag/subscriber_id": "SUB00001"
        }
      }
    },
    {
      "Sid": "ListOwnSecrets",
      "Effect": "Allow",
      "Action": "secretsmanager:ListSecrets",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "secretsmanager:ResourceTag/subscriber_id": "SUB00001"
        }
      }
    }
  ]
}
```

### Create and Attach Secrets Policy

```bash
aws iam create-policy \
  --policy-name YoAiSubscriber-SUB00001-SecretsAccess \
  --policy-document file://secrets-manager-policy.json \
  --description "Secrets Manager access for SUB00001 agent credentials"

export SECRETS_POLICY_ARN="arn:aws:iam::YOUR_ACCOUNT_ID:policy/YoAiSubscriber-SUB00001-SecretsAccess"

aws iam attach-role-policy \
  --role-name YoAiSubscriber-SUB00001 \
  --policy-arn $SECRETS_POLICY_ARN
```

---

## Step 5: Generate Initial Agent Credentials

### Create API Keys for All 20 Agents

```bash
# Array of all agent IDs
AGENTS=(
  "com.privacyportfolio.solicitor-general"
  "com.privacyportfolio.decision-master"
  "com.privacyportfolio.door-keeper"
  "com.privacyportfolio.incident-responder"
  "com.privacyportfolio.the-sentinel"
  "com.privacyportfolio.workflow-builder"
  "com.privacyportfolio.complaint-manager"
  "com.privacyportfolio.compliance-validator"
  "com.privacyportfolio.darkweb-checker"
  "com.privacyportfolio.data-anonymizer"
  "com.privacyportfolio.data-steward"
  "com.privacyportfolio.ip-inspector"
  "com.privacyportfolio.profile-builder"
  "com.privacyportfolio.purchasing-agent"
  "com.privacyportfolio.rewards-seeker"
  "com.privacyportfolio.risk-assessor"
  "com.privacyportfolio.socialmedia-checker"
  "com.privacyportfolio.tech-inspector"
  "com.privacyportfolio.talent-agent"
  "com.privacyportfolio.vendor-manager"
)

# Generate and store API keys
for AGENT_ID in "${AGENTS[@]}"; do
  # Generate secure random API key (64 characters)
  API_KEY=$(openssl rand -hex 32)
  
  # Store in Secrets Manager
  aws secretsmanager create-secret \
    --name "yo-ai/agents/SUB00001/${AGENT_ID}/api-key" \
    --description "API key for agent ${AGENT_ID}" \
    --secret-string "{\"api_key\":\"${API_KEY}\",\"agent_id\":\"${AGENT_ID}\",\"subscriber_id\":\"SUB00001\",\"created_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
    --tags Key=subscriber_id,Value=SUB00001 Key=agent_id,Value=${AGENT_ID} Key=credential_type,Value=APIKey \
    --region $AWS_REGION
  
  echo "Created API key for ${AGENT_ID}"
done
```

---

## Step 6: Set Custom Attributes in User Pool Schema

**Note:** These must be configured when creating the User Pool. If not already done, you'll need to:

1. Create new User Pool with custom attributes:
   - `custom:subscriber_id` (String)
   - `custom:responsible_human_id` (String)
   - `custom:org_id` (String)
   - `custom:role` (String)
   - `custom:mfa_level` (String)

2. Configure MFA settings:
   - TOTP enabled
   - Optional SMS backup

---

## Step 7: Tag S3 Objects for Owned Agents

For each agent that SUB00001 owns, tag the S3 objects:

```bash
for AGENT in "${AGENTS[@]}"; do
  AGENT_NAME=$(echo $AGENT | cut -d'.' -f3)
  
  # Tag auth folder objects
  aws s3api put-object-tagging \
    --bucket yo-ai-agent-registry \
    --key "agent-registry/${AGENT_NAME}/auth/credentials.json" \
    --tagging "TagSet=[{Key=owner,Value=SUB00001},{Key=agent_id,Value=${AGENT}}]"
  
  # Tag agent card
  aws s3api put-object-tagging \
    --bucket yo-ai-agent-registry \
    --key "agent-registry/${AGENT_NAME}/agent.json" \
    --tagging "TagSet=[{Key=owner,Value=SUB00001},{Key=agent_id,Value=${AGENT}}]"
done
```

---

## Step 8: Test Cognito Login

### Get Authentication Token

```bash
aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id YOUR_APP_CLIENT_ID \
  --auth-parameters USERNAME=$SUBSCRIBER_ID,PASSWORD="YOUR_PASSWORD" \
  --region $AWS_REGION
```

**Expected Response:**
```json
{
  "ChallengeName": "MFA_SETUP",
  "Session": "session-token-here",
  "ChallengeParameters": {}
}
```

User must complete MFA setup on first login.

---

## Step 9: Generate Welcome Email Content

```text
Subject: Welcome to Yo-ai Platform - Your Subscriber Account is Ready

Hi Craig,

Your Yo-ai Platform subscriber account (SUB00001) has been created successfully.

**Login Credentials:**
- Username: SUB00001
- Temporary Password: [SECURE_PASSWORD_HERE]
- Login URL: https://auth.yo-ai.ai/login

**Next Steps:**
1. Log in using the credentials above
2. Complete MFA setup using your authenticator app
3. Change your temporary password
4. Review your 20 registered agents in the dashboard

**Your Kafka Topics:**
- agents.SUB00001.notifications
- agents.SUB00001.*.activity
- agents.SUB00001.*.metrics
- agents.SUB00001.*.errors
- platform.events.all (read-only)

**Kafka Connection:**
- Brokers: kafka.yo-ai.internal:9092
- Consumer Group: subscriber-SUB00001
- Auth: SASL_SSL

**Support:**
- Email: solicitor-general@yo-ai.ai
- Documentation: https://yo-ai.ai/docs

Welcome to the platform!

The Yo-ai Team
```

---

## Summary Checklist

- [ ] Created Cognito user SUB00001
- [ ] Set permanent password
- [ ] Enabled MFA (high level)
- [ ] Created IAM role YoAiSubscriber-SUB00001
- [ ] Attached S3 access policy (tag-based)
- [ ] Attached Kafka access policy (topic-based)
- [ ] Attached Secrets Manager policy
- [ ] Generated API keys for all 20 agents
- [ ] Stored credentials in Secrets Manager
- [ ] Tagged S3 objects with owner=SUB00001
- [ ] Tested Cognito login
- [ ] Sent welcome email to craig-erickson@privacyportfolio.com

---

## Security Notes

1. **Password Storage**: Never store passwords in plain text. Use password manager.
2. **MFA Required**: High-level MFA must be completed before full access granted.
3. **API Key Rotation**: Implement 90-day rotation policy for agent API keys.
4. **Audit Logging**: All IAM actions logged to CloudTrail.
5. **Tag Enforcement**: S3 bucket policy should enforce owner tags on all objects.

---

## Troubleshooting

**Issue: User can't access S3 objects**
- Verify S3 object tags: `aws s3api get-object-tagging --bucket yo-ai-agent-registry --key agent-registry/solicitor-general/agent.json`
- Confirm owner tag matches subscriber_id

**Issue: Kafka connection fails**
- Check MSK cluster security group allows traffic from subscriber's IP/VPC
- Verify IAM role has correct Kafka permissions
- Test connection: `kafka-console-consumer --bootstrap-server kafka.yo-ai.internal:9092 --topic agents.SUB00001.notifications`

**Issue: MFA not working**
- Resend MFA setup: `aws cognito-idp admin-set-user-mfa-preference --user-pool-id $USER_POOL_ID --username $SUBSCRIBER_ID --software-token-mfa-settings Enabled=true`
- User must scan QR code with authenticator app

---

## Next Steps

After SUB00001 is set up:
1. Provision Kafka topics (Step 0.8)
2. Deploy agent cards to S3
3. Test agent registration flow
4. Create subscriber onboarding documentation for external parties

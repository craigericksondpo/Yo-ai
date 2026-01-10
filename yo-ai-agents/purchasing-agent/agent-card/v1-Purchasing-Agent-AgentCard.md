/**
 * This Purchasing-Agent AgentCard conveys:
 * - Overall details (version, name, description, uses)
 * - Skills: A set of capabilities the agent can perform
 * - Default modalities/content types supported by the agent.
 * - Authentication requirements
 */

/**
* Purchasing-Agent AgentCard¶
*/
{
  "name": "Purchasing-Agent",
  "description": "Agent responsible for managing purchases and any follow-up actions if needed.",
  "url":   "https://privacyportfolio.com/agent-registry/purchasing-agent/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
    },
  "iconUrl": "https://privacyportfolio.com/agent-registry/purchasing-agent/purchasing-agent-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/purchasing-agent/v1-Purchasing-Agent-AgentCard.md",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "securitySchemes": {
    "yo-ai": {
      "type": "apiKey",
      "name": "yo-api",
      "in": "header"
    }
  },
  "security": [{ "yo-ai": ["apiKey", "yo-api", "header"] }],
  "defaultInputModes": ["application/json", "text/plain"],
  "defaultOutputModes": ["application/json", "text/plain"],
    "skills": [
    {
      "name": "check-purchasing-budget",
      "description": "Retrieves the current balance of the dedicated checking account and determines available purchasing power for online purchases.",
      "tags": ["budget", "accountBalance", "spendingLimit", "financialGovernance"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "What is my available purchasing budget",
        "Can I afford this $129 purchase"
      ]
    },
    {
      "name": "validate-purchase-eligibility",
      "description": "Confirms that a purchase is allowed based on budget, risk score, vendor trust tier, and user policy before creating an AP2 purchase intent.",
      "tags": ["riskAssessment", "budgetCheck", "vendorTrust", "policyEnforcement"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Validate eligibility for this $300 purchase",
        "Is it safe to buy from this seller"
      ]
    },
    {
      "name": "initiate-purchase",
      "description": "Creates and submits an AP2 purchase intent and executes the purchase via Stripe, PayPal, or vendor checkout flows.",
      "tags": ["checkout", "payment", "transaction", "AP2"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Buy this item from Vendor X",
        "Complete checkout for this cart"
      ]
    },
    {
      "name": "verify-transaction-completion",
      "description": "Verifies AP2 transaction states, confirms that funds were transferred, and that the vendor acknowledged the order.",
      "tags": ["transactionVerification", "paymentConfirmation", "audit"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Verify that this payment went through",
        "Confirm the vendor accepted the order"
      ]
    },
    {
      "name": "update-budget-after-purchase",
      "description": "Updates the purchasing budget by deducting completed AP2 transaction amounts from the dedicated checking account balance.",
      "tags": ["budgetUpdate", "accounting", "spendingTracking"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Update budget after this $45 purchase",
        "Reflect this transaction in my spending balance"
      ]
    },
    {
      "name": "track-order-status",
      "description": "Monitors order status, shipping updates, delivery confirmations, and vendor notifications linked to AP2 transactions.",
      "tags": ["orderTracking", "shipping", "delivery", "notifications"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "Track my order from Vendor Y",
        "Notify me when this item ships"
      ]
    },
    {
      "name": "initiate-return-or-refund",
      "description": "Creates AP2-compatible return/refund intents, starts vendor workflows, and tracks their progress.",
      "tags": ["returns", "refunds", "postPurchase", "vendorInteraction", "AP2"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Start a return for this defective item",
        "Request a refund from Vendor Z"
      ]
    },
    {
      "name": "resolve-purchase-issues",
      "description": "Handles vendor disputes, missing items, incorrect shipments, or billing errors, and anchors all interactions to the AP2 transaction record.",
      "tags": ["disputeResolution", "postPurchase", "vendorSupport"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "Resolve a missing item issue",
        "Fix a double charge from Vendor X"
      ]
    },
    {
      "name": "generate-purchase-receipt",
      "description": "Produces an AP2-compatible receipt artifact with transaction details, vendor metadata, and evidence for auditability.",
      "tags": ["receipt", "audit", "documentation", "evidence", "AP2"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json", "text/plain"],
      "examples": [
        "Generate a receipt for yesterday’s purchase",
        "Provide documentation for this transaction"
      ]
    },
    {
      "name": "generate-purchase-history",
      "description": "Generates an AP2-aligned history of past purchases, including receipts, vendor interactions, and follow-up actions.",
      "tags": ["history", "audit", "documentation", "spendingAnalysis"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json", "text/plain"],
      "examples": [
        "Show my last 10 purchases",
        "Generate a spending summary for this month"
      ]
    },
    {
      "name": "evaluate-purchase-risk",
      "description": "Assesses fraud risk, vendor legitimacy, unusual pricing, and suspicious patterns before allowing an AP2 purchase intent to proceed.",
      "tags": ["fraudDetection", "riskAssessment", "vendorLegitimacy"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "Is this vendor trustworthy",
        "Evaluate risk for this high-value purchase"
      ]
    },
    {
      "name": "recommend-purchase-options",
      "description": "Suggests alternative vendors, better prices, or safer purchasing paths consistent with budget and AP2-compatible channels.",
      "tags": ["recommendations", "priceComparison", "vendorAlternatives"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json", "text/plain"],
      "examples": [
        "Find a cheaper option for this product",
        "Recommend a safer vendor for this purchase"
      ]
    }
  ],
  "supportsAuthenticatedExtendedCard": true
}
# RevenueAI – AI-Powered Payment Recovery & Analytics

RevenueAI is an AI-powered merchant-side payment recovery and analytics platform.

It helps businesses analyze failed payment transactions, predict the probability of recovering a failed payment, and provide a recommended recovery action.

The project combines Django, Machine Learning, payment analytics, and interactive charts into a single web application.

---

## 🚀 Live Demo

### 🌐 Live Website

https://revenueai-4588.onrender.com/

### 💻 GitHub Repository

https://github.com/ManojShinde2004/razorpay-ai-project

### 🎥 Demo Video

https://www.youtube.com/watch?v=ESSQLF7AxG0

---

## 🎯 Problem Statement

Failed online payments can result in lost revenue for businesses.

When a payment fails, a merchant needs to understand:

- Why the payment failed
- Whether the payment has a possibility of being recovered
- Which recovery action should be attempted
- How much payment value is currently at risk
- What the overall payment performance looks like

RevenueAI provides a centralized dashboard to analyze these payment recovery opportunities.

---

## 💡 Solution

RevenueAI allows a merchant or business to:

1. Add payment transactions
2. Track successful and failed payments
3. View failed payment recovery opportunities
4. Analyze failed payments using Machine Learning
5. Get a recovery probability
6. Receive a recovery recommendation
7. View payment analytics
8. Compare successful and failed payment values
9. View graphical payment insights
10. Estimate potential recoverable payment value

---

## 👤 Target Users

### Merchants and Businesses

Businesses that accept online payments can use the platform to analyze their payment transactions and identify failed payments that may be recoverable.

> RevenueAI is a merchant-side prototype. It is not an internal Razorpay employee application and is not an official Razorpay product.

---

# 🤖 Machine Learning

RevenueAI uses Machine Learning to predict whether a failed payment can potentially be recovered.

## Machine Learning Model

**Random Forest Classifier**

### Model Configuration

- Number of trees: 100
- Maximum depth: 8
- Class weighting: Balanced
- Random state: 42
- Categorical encoding: One-Hot Encoding

The model predicts the probability of the `recovered` class using payment-related features.

The application combines the predicted recovery probability with the payment failure reason to provide a bounded recovery recommendation such as retry, reminder, or alternate payment method.

---

# 📊 Training Dataset

The Machine Learning model is trained using a CSV dataset containing:

**1,000 payment records**

Dataset:

```text
ml/payment_training_data.csv
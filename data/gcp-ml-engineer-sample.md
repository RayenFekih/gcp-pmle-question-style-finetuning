----------------------------------------

## Exam Professional Machine Learning Engineer topic 1 question 308 discussion

Actual exam question from

Google's
Professional Machine Learning Engineer

Question #: 308
Topic #: 1

[All Professional Machine Learning Engineer Questions]

You are an ML engineer at a bank. The bank's leadership team wants to reduce the number of loan defaults. The bank has labeled historic data about loan defaults stored in BigQuery. You have been asked to use AI to support the loan application process. For compliance reasons, you need to provide explanations for loan rejections. What should you do? 
Suggested Answer: C 🗳️ 

A. Import the historic loan default data into AutoML. Train and deploy a linear regression model to predict default probability. Report the probability of default for each loan application.

B. Create a custom application that uses the Gemini large language model (LLM). Provide the historic data as context to the model, and prompt the model to predict customer defaults. Report the prediction and explanation provided by the LLM for each loan application.

C. Train and deploy a BigQuery ML classification model trained on historic loan default data. Enable feature-based explanations for each prediction. Report the prediction, probability of default, and feature attributions for each loan application.

D. Load the historic loan default data into a Vertex AI Workbench instance. Train a deep learning classification model using TensorFlow to predict loan default. Run inference for each loan application, and report the predictions.

**Answer: C**

**Timestamp: May 21, 2025, 9:01 a.m.**

[View on ExamTopics](https://www.examtopics.com/discussions/google/view/303981-exam-professional-machine-learning-engineer-topic-1-question/)

----------------------------------------

## Exam Professional Machine Learning Engineer topic 1 question 306 discussion

Actual exam question from

Google's
Professional Machine Learning Engineer

Question #: 306
Topic #: 1

[All Professional Machine Learning Engineer Questions]

You work for a large retailer, and you need to build a model to predict customer chum. The company has a dataset of historical customer data, including customer demographics purchase history, and website activity. You need to create the model in BigQuery ML and thoroughly evaluate its performance. What should you do? 
Suggested Answer: D 🗳️ 

A. Create a linear regression model in BigQuery ML, and register the model in Vertex AI Model Registry. Use Vertex AI to evaluate the model performance.

B. Create a logistic regression model in BigQuery ML, and register the model in Vertex AI Model Registry. Use ML.ARIMA_EVALUATE function to evaluate the model performance.

C. Create a linear regression model in BigQuery ML. Use the ML.EVALUATE function to evaluate the model performance.

D. Create a logistic regression model in BigQuery ML. Use the ML.CONFUSION_MATRIX function to evaluate the model performance.

**Answer: D**

**Timestamp: May 21, 2025, 9:03 a.m.**

[View on ExamTopics](https://www.examtopics.com/discussions/google/view/303982-exam-professional-machine-learning-engineer-topic-1-question/)

----------------------------------------

## Exam Professional Machine Learning Engineer topic 1 question 17 discussion

Actual exam question from

Google's
Professional Machine Learning Engineer

Question #: 17
Topic #: 1

[All Professional Machine Learning Engineer Questions]

You are building a real-time prediction engine that streams files which may contain Personally Identifiable Information (PII) to Google Cloud. You want to use theCloud Data Loss Prevention (DLP) API to scan the files. How should you ensure that the PII is not accessible by unauthorized individuals? 
Suggested Answer: D 🗳️ 

A. Stream all files to Google Cloud, and then write the data to BigQuery. Periodically conduct a bulk scan of the table using the DLP API.

B. Stream all files to Google Cloud, and write batches of the data to BigQuery. While the data is being written to BigQuery, conduct a bulk scan of the data using the DLP API.

C. Create two buckets of data: Sensitive and Non-sensitive. Write all data to the Non-sensitive bucket. Periodically conduct a bulk scan of that bucket using the DLP API, and move the sensitive data to the Sensitive bucket.

D. Create three buckets of data: Quarantine, Sensitive, and Non-sensitive. Write all data to the Quarantine bucket. Periodically conduct a bulk scan of that bucket using the DLP API, and move the data to either the Sensitive or Non-Sensitive bucket.

**Answer: D**

**Timestamp: June 16, 2021, 1:58 p.m.**

[View on ExamTopics](https://www.examtopics.com/discussions/google/view/55437-exam-professional-machine-learning-engineer-topic-1-question/)

----------------------------------------

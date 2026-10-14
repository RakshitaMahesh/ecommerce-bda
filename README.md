# E-Commerce Transaction Analysis Using Hadoop MapReduce

## 1. Project Overview
This project analyzes e-commerce transaction data using Apache Hadoop
MapReduce. It calculates transaction counts, successful and failed
payments, transaction amounts, payment-method statistics, and
successful sales by product category.

## 2. Technologies Used
- Apache Hadoop 3.4.2
- Java
- Hadoop Distributed File System (HDFS)
- YARN
- MapReduce

## 3. Project Structure
- input/transactions.csv: Sample transaction dataset
- src/EcommerceAnalysis.java: Java MapReduce source code
- EcommerceAnalysis.jar: Compiled application
- results.txt: Initial analysis output
- final_results.txt: Improved analysis output
- docs/: Project documentation
- screenshots/: Demonstration screenshots

## 4. Dataset
The sample dataset contains 20 transactions and these fields:
transaction_id, customer_id, amount, payment_method, status,
product_category.

## 5. Main Analysis
- Total number of transactions
- Successful and failed transaction counts
- Total transaction amount
- Successful sales and failed transaction amounts
- Successful sales by product category
- Payment method usage and failure counts

## 6. Run the Project
Start Hadoop HDFS and YARN, then upload the input data:

hdfs dfs -mkdir -p /ecommerce/input
hdfs dfs -put -f ~/ecommerce-bda/input/transactions.csv /ecommerce/input/

Compile the Java program:

cd ~/ecommerce-bda
mkdir -p build
javac -classpath "$(hadoop classpath)" -d build src/EcommerceAnalysis.java
jar -cvf EcommerceAnalysis.jar -C build .

Run the MapReduce job:

hadoop jar ~/ecommerce-bda/EcommerceAnalysis.jar EcommerceAnalysis /ecommerce/input/transactions.csv /ecommerce/output_v2

Display results:

hdfs dfs -cat /ecommerce/output_v2/part-r-00000

Save results locally:

hdfs dfs -cat /ecommerce/output_v2/part-r-00000 > ~/ecommerce-bda/final_results.txt

Note: Hadoop requires the output directory to be new for each job.
If /ecommerce/output_v2 already exists, use a different output path
or remove the old output directory before rerunning.

## 7. Results Summary
- Total transactions: 20
- Successful transactions: 15
- Failed transactions: 5
- Transaction success rate: 75%
- Successful sales amount: 28197.00
- Failed transaction amount: 7650.00
- Total attempted transaction amount: 35847.00

## 8. Conclusion
The project demonstrates how Hadoop MapReduce can process transaction
records and aggregate business metrics. The results are based on a
small sample dataset created for academic demonstration and do not
represent real commercial transaction data.

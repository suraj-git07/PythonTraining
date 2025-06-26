# 📘 Python SQL Assignment – Suraj Mishra

This document contains all solutions to the SQL assignment completed as part of the **Nagarro Fresher Training Program**, using the **AdventureWorks** database on **SQL Server**.

Each query has been thoroughly tested, and results have been captured with relevant **screenshots** to validate correctness and execution.

---

## 🗂️ Contents

- 📄 `AdventureWorks_SQL_Assignment.docx`  
  Includes:
  - SQL query solutions for Exercises 1 to 6
  - Screenshots of query executions and outputs

---

## 🧩 Exercises Overview

### ✅ Exercise 1: Querying AdventureWorks Schema

Basic to intermediate SQL queries on schemas like `Sales`, `Person`, `Production`, and `HumanResources`.

- Record counts and pattern matching  
- Conditional selections  
- Aggregations and computed columns  
- Scalar function and stored procedure usage  

### ✅ Exercise 2: Different Query Techniques

List customers who have **not placed any orders** using:

- `JOIN`  
- `SUBQUERY`  
- `CTE`  
- `EXISTS`

### ✅ Exercise 3: High-Value Customers

Retrieve the **five most recent orders** from account numbers that have spent more than **$70,000**.

### ✅ Exercise 4: Currency Conversion Function

Custom SQL function that:

- Accepts `SalesOrderID`, `CurrencyCode`, and `RateDate`  
- Returns order details with currency-converted pricing using `Sales.CurrencyRate`

### ✅ Exercise 5: Stored Procedure for Name Filtering

Stored procedure to:

- Filter names by `FirstName`  
- Support **optional/default** filtering

### ✅ Exercise 6: Price Change Trigger

Trigger on `Product` table to:

- Prevent `ListPrice` increases over **15%**  
- Modify to only activate on `ListPrice` column updates

---

## 🖼️ Demo & Validation

All exercises include:

- 📷 **Screenshots** of SQL Server Management Studio (SSMS) outputs  
- 🧪 **Test cases** to ensure correctness  
- ✅ Real data from **AdventureWorks** schema

---


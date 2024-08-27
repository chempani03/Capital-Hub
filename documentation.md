# Capital Hub API Documentation

## **Tags: Capital Hub**

### **Endpoint: `/hub/transactions_full/`**

- **Description:** Retrieve all transactions in the system. This endpoint fetches all the transactions recorded in the database, providing a comprehensive overview of all financial activities.

- **Input:**

  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `List[TransOverViewBase]`: A list of all transaction records.

- **Errors:**
  - `500 Internal Server Error`: If there is an issue retrieving the transactions.

---

### **Endpoint: `/hub/transactions/`**

- **Description:** Retrieve filtered transactions based on specified parameters. This endpoint allows you to filter transactions by date range, currency, transaction type, account, and category.

- **Input:**

  - `startdate` (datetime, required): The start date for filtering transactions.
  - `enddate` (datetime, required): The end date for filtering transactions.
  - `currency` (str, optional): The currency to filter transactions by.
  - `transaction_type` (str, optional): The type of transaction to filter by (e.g., Debit, Credit).
  - `account` (str, optional): The account to filter transactions by.
  - `category` (str, optional): The category to filter transactions by.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `List[TransOverViewBase]`: A list of filtered transaction records.

- **Errors:**
  - `400 Bad Request`: If the required parameters are missing or invalid.
  - `500 Internal Server Error`: If there is an issue retrieving the transactions.

---

### **Endpoint: `/hub/transaction/{transaction_id}/`**

- **Description:** Retrieve a single transaction by its ID. This endpoint allows you to fetch the details of a specific transaction using its unique identifier.

- **Input:**

  - `transaction_id` (str, required): The unique ID of the transaction to retrieve.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `List[TransOverViewBase]`: The details of the transaction with the specified ID.

- **Errors:**
  - `404 Not Found`: If the transaction with the specified ID does not exist.
  - `500 Internal Server Error`: If there is an issue retrieving the transaction.

---

### **Endpoint: `/hub/post_transactions/`**

- **Description:** Create a new transaction. This endpoint allows you to add a new financial transaction by providing details such as booking date, value date, amount, currency, transaction type, account, category, and an optional booking text.

- **Input:**

  - `booking_date` (datetime, required): The date the transaction was booked.
  - `value_date` (datetime, required): The value date of the transaction.
  - `amount` (float, required): The amount of the transaction.
  - `currency` (str, required): The currency in which the transaction was made.
  - `transaction_type` (str, required): The type of transaction (e.g., Credit, Debit).
  - `account` (str, required): The account associated with the transaction.
  - `category` (str, required): The category associated with the transaction.
  - `booking_text` (str, optional): Additional details or description of the transaction.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `TransOverViewBase`: The newly created transaction record.

- **Errors:**
  - `400 Bad Request`: If the required parameters are missing or invalid.
  - `500 Internal Server Error`: If the transaction could not be created or if there is an error during processing.

---

### **Endpoint: `/hub/post_transactions_between_accounts/`**

- **Description:** Create a transaction between two accounts. This endpoint allows you to create a transaction that transfers funds from one account to another, with an optional fee and booking text.

- **Input:**

  - `booking_date` (datetime, required): The date the transaction was booked.
  - `value_date` (datetime, required): The value date of the transaction.
  - `amount` (float, required): The amount being transferred.
  - `sender_account` (str, required): The account from which funds are being sent.
  - `receiver_account` (str, required): The account to which funds are being received.
  - `currency` (str, required): The currency in which the transaction was made.
  - `fee` (int, optional): An optional fee associated with the transaction.
  - `booking_text` (str, optional): Additional details or description of the transaction.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `str`: A message indicating the IDs of the transactions created.

- **Errors:**
  - `400 Bad Request`: If the required parameters are missing or invalid.
  - `500 Internal Server Error`: If the transaction could not be created or if there is an error during processing.

---

### **Endpoint: `/hub/transactions/{transaction_id}/`**

- **Description:** Delete a transaction by its ID. This endpoint allows you to delete a transaction by providing its ID. If the transaction does not exist, it returns a 404 error.

- **Input:**

  - `transaction_id` (str, required): The ID of the transaction to be deleted.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `dict`: A dictionary containing the result of the deletion.

- **Errors:**
  - `404 Not Found`: If the transaction with the specified ID does not exist.
  - `500 Internal Server Error`: If there is an issue deleting the transaction.

---

### **Endpoint: `/hub/update_transaction/{transaction_id}/`**

- **Description:** Update a transaction by its ID. This endpoint allows you to update specific details of a transaction using its unique identifier.

- **Input:**

  - `transaction_id` (str, required): The unique ID of the transaction to update.
  - `transaction_update` (TransactionUpdate, required): A Pydantic model containing the fields to update.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `TransOverViewBase`: The updated transaction object.

- **Errors:**
  - `400 Bad Request`: If the required parameters are missing or invalid.
  - `404 Not Found`: If the transaction with the specified ID does not exist.
  - `500 Internal Server Error`: If there is an issue updating the transaction.

## **Tags: Capital Hub Metrics**

### **Endpoint: `/metrics/aggregated_amount_currency/`**

- **Description:** Retrieve the total aggregated transaction amount for a specified currency.

- **Input:**

  - `currency` (str, required): The currency code to aggregate transactions for.
  - `decimal` (Optional[int], optional): Number of decimal places to round the result to.

- **Output:**

  - `JSON`: A response containing the total aggregated amount for the specified currency.

- **Errors:**
  - `400 Bad Request`: If the currency or column is not valid.
  - `500 Internal Server Error`: If there is an issue retrieving the aggregated amount.

---

### **Endpoint: `/metrics/aggregated_amount_filltered_currency/`**

- **Description:** Retrieve the total aggregated transaction amount by currency within a date range.

- **Input:**

  - `start_date` (Optional[datetime], optional): The start date for filtering transactions.
  - `end_date` (Optional[datetime], optional): The end date for filtering transactions.
  - `transaction_type` (Optional[str], optional): The transaction type to filter transactions by.
  - `account` (Optional[str], optional): The account to filter transactions by.
  - `category` (Optional[str], optional): The category to filter transactions by.
  - `decimal` (Optional[int], optional): Number of decimal places to round the result to.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `JSON`: A response containing the total aggregated amount for each currency within the specified date range.

- **Errors:**
  - `400 Bad Request`: If the input parameters are invalid.
  - `500 Internal Server Error`: If there is an issue retrieving the aggregated data.

## **Tags: Capital Hub Insights**

### **Endpoint: `/insights/net_balance/`**

- **Description:** Retrieve the net balance for a specified currency of interest within an optional date range.

- **Input:**

  - `currency_of_interest` (str, required): The currency to get the net balance for.
  - `start_date` (str, optional): The start date for the range (format: 'YYYY-MM-DD').
  - `end_date` (str, optional): The end date for the range (format: 'YYYY-MM-DD').
  - `decimal` (int, optional): Number of decimal places to round the result to.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `JSON`: A response containing the aggregated net balance information.

- **Errors:**
  - `422 Unprocessable Entity`: If `end_date` is provided without `start_date`.
  - `400 Bad Request`: If there is an error during processing.

---

### **Endpoint: `/insights/category_muncher/`**

- **Description:** Retrieve the total amount for a specified category within an optional date range.

- **Input:**

  - `category` (str, required): The category to get the total amount for.
  - `currency_of_interest` (str, required): The currency to get the total amount for.
  - `start_date` (str, optional): The start date for the range (format: 'YYYY-MM-DD').
  - `end_date` (str, optional): The end date for the range (format: 'YYYY-MM-DD').
  - `decimal` (int, optional): Number of decimal places to round the result to.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `JSON`: A response containing the total amount for the category.

- **Errors:**
  - `422 Unprocessable Entity`: If `end_date` is provided without `start_date`.
  - `400 Bad Request`: If there is an error during processing.

---

### **Endpoint: `/insights/muncher_full_overview/`**

- **Description:** Retrieve a full overview of aggregated net amounts by category within an optional date range.

- **Input:**

  - `currency_of_interest` (str, required): The currency to display the total amounts in.
  - `order` (Literal['asc', 'desc'], required): The order to sort the categories by amount (`'asc'` for ascending, `'desc'` for descending).
  - `start_date` (str, optional): The start date for the transaction range (format: 'YYYY-MM-DD').
  - `end_date` (str, optional): The end date for the transaction range (format: 'YYYY-MM-DD').
  - `decimal` (int, optional): Number of decimal places to round the amounts to.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `JSON`: A list of dictionaries, each containing a category and its corresponding total amount.

- **Errors:**
  - `422 Unprocessable Entity`: If `end_date` is provided without `start_date`.
  - `400 Bad Request`: If there is an error during processing or verification.

---

### **Endpoint: `/insights/timeseries/`**

- **Description:** Retrieve a cumulative balance time series for transactions within a specified date range, aggregated by the specified granularity.

- **Input:**

  - `currency_of_interest` (str, required): The currency in which to display the transaction amounts.
  - `granularity` (Literal['daily', 'weekly', 'monthly'], required): The level of detail for the time series aggregation.
    - `'daily'`: Aggregate by day.
    - `'weekly'`: Aggregate by week.
    - `'monthly'`: Aggregate by month.
  - `start_date` (str, optional): The start date for the transaction range (format: 'YYYY-MM-DD'). Must be provided if `end_date` is specified.
  - `end_date` (str, optional): The end date for the transaction range (format: 'YYYY-MM-DD'). Must be provided if `start_date` is specified.
  - `decimal` (int, optional): The number of decimal places to round the cumulative amounts to.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `JSONResponse`: A JSON object containing the cumulative credit, debit, and net balance time series.
    - `credit`: A list of records with the booking date, transaction amount, and cumulative amount.
    - `debit`: A list of records with the booking date, transaction amount, and cumulative amount.
    - `net_balance`: A list of records with the booking date and the cumulative net balance (difference between credit and debit).

- **Errors:**
  - `422 Unprocessable Entity`: If only one of `start_date` or `end_date` is provided.
  - `400 Bad Request`: If there is an error during processing, verification, or data retrieval.

## **Tags: Capital Hub Reports**

### **Endpoint: `/reports/monthly_reports/`**

- **Description:** Generate and retrieve a monthly financial report in PDF format. This report provides a detailed overview of financial metrics for the specified month and year, including cumulative balances, income, and expenditure by category.

- **Input:**

  - `month` (Literal['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], required): The month for which to generate the report.
  - `year` (Literal['2024', '2025'], required): The year for which to generate the report.
  - `currency_of_interest` (str, required): The currency in which the report should be generated.
  - `db` (Session, optional): The database session dependency.

- **Output:**

  - `StreamingResponse`: A PDF file containing the financial metrics report for the specified month, year, and currency.

- **Errors:**
  - `204 No Content`: If no data is found for the specified date range.
  - `400 Bad Request`: If there is an error during processing or data retrieval.

---

### **Report Generation Details**

The `monthly_report` function performs the following steps:

1. **Date Calculation:**

   - The `get_monthly_dates` function calculates the start and end dates based on the provided month and year.

2. **Data Retrieval and Conversion:**

   - Data for the specified date range and currency is retrieved from the database.
   - If no data is found, an HTTP 204 error is raised.
   - Currency conversion is applied using a forex map to ensure all data is in the specified currency.

3. **Time Series Data Preparation:**

   - The cumulative balance time series is generated and structured for plotting.

4. **Category Expenditure Data Preparation:**

   - Data is aggregated by category for income and expenditure, sorted in descending order.

5. **PDF Report Generation:**
   - A PDF report is generated using matplotlib and seaborn, following a pre-defined style configuration.
   - The report includes four main visualizations:
     1. **Total Financial Metrics** for the month.
     2. **Income by Category**.
     3. **Expenses by Category**.
     4. **Cumulative Balance Over Time**.
   - The report is saved to an in-memory buffer and returned as a downloadable PDF file.

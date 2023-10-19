# Expense Tracker

**Expense Tracker** is a web application that empowers users to take control of their financial lives by providing actionable insights into their spending and income patterns. With its visually appealing graphs and detailed summaries for different time periods, this Django project is an indispensable tool for anyone interested in managing their financial resources effectively.

## Key Features

- **Expense and Income Logging:** Users can conveniently record all their expenses and incomes, including transaction details, categories, and amounts.

- **Dashboard with Graphs:** The heart of the application is the user-friendly dashboard. It offers an interactive and visual representation of financial data, with dynamic graphs depicting the balance between expenses and incomes.

- **Time Period Summaries:** To assist users in gaining a comprehensive understanding of their financial trends, the dashboard provides summaries for different time periods, such as the last 30 days, the previous 3 months, the past 6 months, and the entire year.

- **Expense Categories:** Users can categorize expenses for better organization, allowing them to see which areas of spending require the most attention.

- **Secure User Accounts:** The application ensures user data security by requiring account creation and login, thereby safeguarding personal financial information.

- **User-Friendly Interface:** The user interface is intuitive, making it easy for users to navigate through the application, add, edit, and delete expenses and incomes, and view detailed financial insights.

## Demo

Check out the live demo of the **Expense Tracker** at [https://expenseswebsite-7bdaoiob8-theprateekgoyal2.vercel.app/](https://expenseswebsite-7bdaoiob8-theprateekgoyal2.vercel.app/).

## Installation

To set up the project locally, you can use the provided `requirements.txt` file. Here are the general steps:

1. Clone the repository:
`git clone https://github.com/theprateekgoyal2/expensewebsite-publicRepo.git`

2. Create a virtual environment (recommended):

3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install project dependencies:
`pip install -r requirements.txt`

5. Apply database migrations:
`python manage.py migrate`

6. Add SMTP Server Credentials:
- Open the `settings.py` file in your project.
- Locate the section related to email settings.
- Add your SMTP server credentials, including the SMTP server address, port, username, and password.

7. Start the development server:
`python manage.py runserver`

8. Access the application in your web browser at [http://localhost:8000](http://localhost:8000).

## Contributing

If you'd like to contribute to this project, feel free to open issues or submit pull requests. Your contributions are welcome!

## Contact Information

For any questions or support, you can reach out to [Prateek Goyal] at [prateek.goyal.dev@gmail.com].
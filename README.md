# Personal Finance Dashboard

A web-based personal finance dashboard that helps users track, categorize, and analyze their expenses and incomes. Built with machine learning models for automatic expense categorization and equipped with visualizations for comprehensive financial insights.

## Features

- **Expense Tracking**: Easily add, edit, or delete expenses.
- **Expense Categorization**: Automatically categorizes expenses into predefined categories using machine learning.
- **Visualization**: Interactive graphs and charts for visualizing spending patterns.
- **Monthly Forecasting**: Predicts future spending based on past data.

## Technologies Used

- **Backend**: Python (Dash)
- **Frontend**: CSS, JavaScript
- **Data Handling**: Pandas, Numpy
- **Machine Learning**: Scikit-learn, TensorFlow
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Version Control**: Git

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/llazzari/personal_finance.git
   cd personal_finance
   ```

2. **Create a virtual environment and activate it**:
   ```bash
   python -m venv venv
   source venv/bin/activate # For Windows use: venv\Scripts\activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Access the dashboard**:  
   Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage

1. Add your expenses and incomes.
2. Expenses will be automatically categorized into one of the following categories:
   - **Food & Dining**
   - **Transport**
   - **Housing**
   - **Entertainment**
   - **Pets**
   - **Travel**
   - **Utilities**
   - **Personal Expenses**
   - **Debts**
   - **Investments**
   - **Miscellaneous**
3. Visualize your spending habits through interactive graphs.
4. Analyze monthly spending trends.

## Contributing

Contributions are welcome! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch (\`git checkout -b feature/your-feature\`).
3. Commit your changes (\`git commit -m 'Add your feature'\`).
4. Push to the branch (\`git push origin feature/your-feature\`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

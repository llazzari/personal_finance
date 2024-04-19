# Financial Management Web Application

This project is a powerful web application built using Python's Dash framework for managing and analyzing financial data seamlessly.

## Features

- **Data Management**: Users can upload bank statements or import their own CSV tables containing financial transactions.
- **Data Analysis**: Upon upload, the application conducts data analysis, enabling users to manually edit or utilize automatic classification based on our RandomForestClassifier model with 90% accuracy in categorizing expenses and incomes.
- **Dashboard Tabs**:
  - **Summary Tab**: Provides a summary of total income, expenses, and budget, accompanied by a bar graph that breaks down incomes by categories. Users can also explore an interactive sunburst chart displaying expenses categorized by main and subcategories for the selected month and year.
  - **Trends Tab**: Allows users to analyze expense trends over time. A bar chart visualizes expense evolution by month within a selected year, or users can view a line graph illustrating expense trends across multiple years.

## Future Enhancements

Planned future enhancements for this application include:

- Transitioning to a SQL database for improved scalability and reliability.
- Enhancing security by adopting Pydantic models to handle data validation and ensure a more robust and secure codebase.

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/financial-management-app.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Access the application in your web browser at `http://localhost:8050`.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

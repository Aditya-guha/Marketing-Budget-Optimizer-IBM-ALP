# Marketing Budget Optimizer – IBM ALP

A data-driven, AI-powered budget optimization tool built with **Streamlit**, this project helps digital marketing teams make smarter budget allocation decisions across platforms like Google Ads, Facebook Ads, LinkedIn, and more.

Developed as part of the IBM Academic Learning Program (ALP) by **Aditya Guha Roy (MBA BA 24023184)**.

---

## Key Features

-  Upload and validate ad campaign data (CSV)
-  Interactive visualizations for ROI, CPA, conversions, and more
-  AI-driven budget allocation using Linear Programming (`scipy.optimize.linprog`)
-  Predicts expected returns and highlights top-performing platforms
-  Engaging dashboards powered by Plotly
-  Try sample data instantly if you don’t have real datasets

---

##  Tech Stack

| Tool           | Use Case                             |
|----------------|--------------------------------------|
| **Streamlit**  | Frontend web app framework           |
| **Pandas**     | Data manipulation                    |
| **NumPy**      | Numerical computations               |
| **SciPy**      | Budget optimization using `linprog` |
| **Plotly**     | Interactive charts and dashboards    |
| **Python**     | Core backend logic                   |

---

##  Folder Structure

budget-optimizer/
├── app.py # Main Streamlit app
└── utils/
├── init.py
├── data_processor.py # Data cleaning and validation
├── optimizer.py # Linear programming logic
└── visualizer.py # Plotly-based visualizations


---

##  Sample Use Case

1. Upload a CSV with campaign metrics: `Channel_Used`, `ROI`, `Conversion_Rate`, etc.
2. App validates and processes the data
3. Get visual insights across platforms
4. Enter your total budget → App recommends optimized allocations
5. Download allocation as CSV and view AI-based suggestions

---

##  Requirements

Install dependencies (you can use `pip` or a virtual environment):


Then run:


---

##  About the Developer

**Aditya Guha Roy**  
MBA in Business Analytics, OP Jindal University  
IBM ALP 2025 Program Participant

---

##  License

This project is part of IBM Academic Learning Program. For academic and educational use only.

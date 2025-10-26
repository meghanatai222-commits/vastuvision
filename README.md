# VastuVision

VastuVision is a web-based application that helps users analyze and optimize the Vastu compliance of their homes or spaces. It combines a user-friendly interface with machine learning-powered analysis to provide actionable insights for better energy and spatial alignment.

## Features

- **User Authentication**: Register, login, and logout securely.
- **Dashboard**: Visual overview of uploaded floor plans and Vastu analysis.
- **Floor Plan Upload**: Upload floor plan images for analysis.
- **Vastu Analysis**: AI-powered backend analyzes floor plans and generates Vastu scores.
- **Results Visualization**: Clear results displayed with recommendations.
- **ML Model**: Python-based ML pipeline for analyzing Vastu compliance.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: PHP
- **Machine Learning**: Python (scikit-learn, pandas, NumPy)
- **Database**: MySQL
- **Version Control**: Git, GitHub

## Project Structure

/samartha
│
├─ index.html
├─ login.html
├─ register.html
├─ dashboard.html
├─ space.html
├─ upload_floor_plan.php
├─ login_process.php
├─ register_process.php
├─ dashboard-script.js
├─ login-script.js
├─ register-script.js
├─ space-script.js
├─ styles.css
├─ dashboard-styles.css
└─ ml_model/
├─ data_processor.py
├─ model_trainer.py
├─ predict.py
├─ run_ml_pipeline.py
├─ vastu_dataset.csv
├─ vastu_model.pkl
└─ vastu_processed.csv


## Installation

1. Clone this repository:
```bash
git clone https://github.com/meghanatai222-commits/vastuvision.git
Set up a local server (e.g., XAMPP, WAMP) for PHP files.

Import the database.sql into your MySQL database.

Install Python dependencies for the ML model:

pip install -r ml_model/requirements.txt


Run the ML pipeline if needed:

python ml_model/run_ml_pipeline.py

Usage

Open the application in your browser via local server.

Register a new account or login.

Upload a floor plan image to get Vastu analysis results.

View the dashboard for historical results and insights.

Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

License

This project is licensed under the MIT License. See the LICENSE file for details.

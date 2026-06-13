🎬 CinemAI: Intelligent Movie Discovery System
CinemAI is an intelligent, content-based movie recommendation system that leverages machine learning to analyze movie metadata and suggest personalized content tailored to user preferences.

This project was developed as part of the Bachelor of Science in Artificial Intelligence (4th Semester) curriculum at the National University of Technology (NUTECH), Islamabad.

🌐 Live Production Link: Click here to view CinemAI Live

🌟 Key Features
Intelligent Query Parser: Seamlessly handles raw user text queries (e.g., lowercase inputs like "jurrasic park") and maps them dynamically to exact metadata titles in the database.

Content Vector Similarity: Implements data vectorization and utilizes Cosine Similarity algorithms to compute exact relationship metrics between movies based on genres and audience ratings.

Dynamic User Workspace: Features a custom sidebar workspace that captures and updates the user's interactive journey and recent exploration history in real-time.

Production-Grade UI/UX: A highly responsive, modern dark-themed interactive dashboard designed cleanly using professional Streamlit UI elements.

🛠️ Tech Stack & Architecture
Core Language: Python

Web Framework: Streamlit (For native cloud deployment and frontend rendering)

Data Processing: Pandas & NumPy (For robust dataset manipulation and restructuring)

Machine Learning Engine: Scikit-Learn (For computing pairwise similarity matrices)

Version Control: Git & GitHub

📂 Project Directory Structure
Plaintext
CinemAI/
│
├── app.py                  # Main source code for the Streamlit web application
├── compress.py             # Automation script for optimizing and cleaning the dataset
├── movies_metadata.csv     # The cleaned, filtered high-voted movie dataset
└── requirements.txt        # Managed dependencies for cloud and local deployment
🏃 Local Setup & Installation
If you want to clone this repository and run the application locally on your machine, execute the following commands in your command prompt:

Clone the repository:

Bash
git clone https://github.com/h666-dotcom/CinemAI.git
Navigate into the project root directory:

Bash
cd CinemAI
Install the required technical dependencies:

Bash
pip install -r requirements.txt
Launch the local development server:

Bash
streamlit run app.py
👤 Developer Profile
Developer: h666-dotcom

Academic Context: Semester Presentation Project, BS Artificial Intelligence

Institution: National University of Technology (NUTECH), Pakistan

Core Philosophy: Building functional engineering solutions, mastering machine learning paradigms, and developing tech autonomy.

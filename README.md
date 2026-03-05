# Cognitive Frailty Screening Application

## Project Overview

The Cognitive Frailty Screening Application is a desktop-based screening system.

The system integrates:

- Dementia Screening Module
- Depression Screening Module
- Admin Login Authentication
- User Information Collection
- Test Selection Interface
- Bilingual Language Support (English / Japanese)

This application is designed for structured cognitive frailty screening in a research environment.

---

## Application Workflow

1. Admin Login Screen  
2. User Information Form  
3. Test Selection Screen
4. Language Selection (English or Japanese) to attempt the test
5. Dementia Screening Module  
6. Depression Screening Module  
7. Independent Result Display for Each Test  

---

## Features

- Secure Admin Login
- Language Selection Option (English / Japanese)
- Structured User Information Collection
- Modular Test Navigation
- Dementia Assessment (Image-based tasks R1–R12)
- Depression Questionnaire Assessment
- Separate scoring logic for each screening test
- Clean and modular PyQt5 UI design
- Organized multi-screen navigation using stacked layouts

---

## Language Support

The application supports bilingual operation:

- English
- Japanese

All user interface elements, instructions, and test questions dynamically adapt based on the selected language at the beginning of the session.

---

## Project Structure

cognitive-frailty-screening/
│
├── app.py  
├── admin_login.py  
├── user_info.py  
├── test_selection.py  
├── dementia.py  
├── depression.py  
├── Ui_card.py  
├── icons 
├── elements
├── Language_selection.py             
├── requirements.txt  
└── README.md  

---

## System Requirements

- Python 3.10 
- Windows / Linux
- PyQt5

---


## Running the Application

Run the application using:

    python app.py

---
 
March 2026

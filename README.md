# LeadLegal: Lead Management System for Law Firms

## Overview
LeadLegal is a powerful and intuitive lead management system designed specifically for law firms to streamline the process of tracking and engaging with potential clients. This application helps attorneys and law firm staff manage prospect information and interactions efficiently, ensuring that every lead is followed up on promptly.

## Key Features
- **Lead Tracking**: Easily capture and store lead information through a public-facing form which collects essential data such as first name, last name, email, and resume/CV.
- **State Management**: Monitor and update the status of each lead, with initial states like "PENDING" that transition to "REACHED_OUT" once an attorney contacts the prospect.
- **Email Notifications**: Automatically send tailored emails to both prospects and attorneys when a new lead is registered or updated.
- **Secure Access**: A secure internal UI ensures that only authorized personnel can view and manage lead information.
- **AWS S3 Integration**: Resumes and CVs uploaded by prospects are securely stored in AWS S3, ensuring data integrity and accessibility.
- 
## Technologies Used
- **FastAPI**: For building high-performance, scalable APIs.
- **SQLite**: For local database management.
- **AWS S3**: For secure file storage.
- **Bootstrap 5**: For responsive frontend design.
- **Python**: Backend programming language.

## Getting Started
To get a local copy up and running follow these simple steps:

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/ml-lubich/lead-legal.git

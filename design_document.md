# Design Document for Lead Management Application

## Project Overview

The Lead Management Application is an API-driven system designed to streamline the process of managing lead information for a legal firm. The system includes functionalities to capture leads publicly and manage them internally, ensuring a seamless and secure flow from lead submission to processing.

## System Architecture

### Components

- **FastAPI Backend**: Manages API requests and business logic, providing fast, asynchronous request handling.
- **SQLite Database**: Lightweight database to store lead data efficiently.
- **Amazon S3**: Robust and scalable service for storing uploaded resumes, ensuring data durability and high availability.
- **Email Service**: Facilitates communication by sending automated emails to prospects and attorneys.

### Workflow and User Experience

#### Prospect Interaction:
- Prospects fill out a form and submit their details along with their resumes, which are uploaded to S3. They receive an email confirmation, enhancing user engagement.

#### Attorney Interaction:
- Attorneys have access to a secure interface where they can review and update the status of leads. They are notified via email when a lead's status changes, ensuring they are always informed.

### High-Level Architecture Diagram

[Prospect] -> [FastAPI App] -> [SQLite Database]
-> [Amazon S3]
-> [Email Service]

[Attorney] -> [FastAPI App] -> [SQLite Database]

csharp
Copy code

## Detailed API Design

### Public Endpoints

- **POST /leads/**: Accepts lead submissions from the public. This is crucial for capturing potential client information in real-time.
  - Inputs: first_name, last_name, email, resume (file)
  - Outputs: Confirmation message with resume URL

### Protected Endpoints

- **GET /leads/**: Allows internal users to retrieve a list of all leads. This endpoint is essential for attorneys to review leads in a central location.
- **PATCH /leads/{lead_id}/**: Enables updating the status of a lead. This function is vital for tracking the progression of each lead through the firm's process.

## Data Storage

### Schema Design

The database schema is designed to be simple yet effective, capturing all necessary details about leads without unnecessary complexity:

Table: leads

- id `INTEGER PRIMARY KEY`
- first_name `TEXT`
- last_name `TEXT`
- email `TEXT UNIQUE`
- resume_url `TEXT`
- status `TEXT DEFAULT 'PENDING'`

### Choice of Technologies

- **SQLite**: Chosen for its simplicity and suitability for small-scale applications, which reduces the overhead of database management and speeds up development.
- **Amazon S3**: Selected for its reliability and scalability, which ensures that the application can handle a large volume of file uploads without degradation of performance.

## Security Considerations

Authentication is implemented via API keys for internal endpoints, ensuring that only authorized personnel can access or modify lead data. All data transmissions are secured using HTTPS, protecting against data interception and unauthorized access.

## Running the Application Locally

The document will include step-by-step instructions for setting up the application locally, covering:

- Installation of dependencies
- Environment setup
- Running the application
- Note: Keys are stored in the code directly to simplify launchtime, but ideally we would use environmental variables (os.environ) for security.

## Design Choices

- **FastAPI**: Chosen for its excellent performance with asynchronous support and automatic API documentation, which accelerates backend development and testing.
- **Email Integration**: Provides immediate feedback to prospects and continuous updates to attorneys, enhancing the user experience and operational efficiency.

## Additional Documentation

Additional documents include:

- API usage examples
- Configuration guidelines
- Troubleshooting tips
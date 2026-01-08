# Spy Cat Agency API

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

A RESTful API designed to manage the **Spy Cat Agency (SCA)**. This system simplifies spying workflows by managing spy cats, their missions, and assigned targets.

Built with **FastAPI**, **SQLModel**, and **Docker**.

---

## Features

### Spy Cats Management
* **CRUD Operations**: Create, Read, Update (Salary), and Delete spy cats.
* **Breed Validation**: Automatically validates cat breeds against [TheCatAPI](https://thecatapi.com/).
* **Experience Tracking**: Stores years of experience and salary data.

### Missions & Targets
* **Mission Logic**:
    * One cat can have only **one active mission** at a time.
    * A mission must have between **1 and 3 targets**.
    * Missions are automatically marked as **Complete** when all targets are finished.
* **Target Logic**:
    * Cats can update notes on targets.
    * **Logic Lock**: Notes cannot be updated if the target or mission is already completed (data freezing).

---

## Tech Stack

* **Framework**: FastAPI
* **Database**: PostgreSQL 15
* **ORM**: SQLModel
* **Validation**: Pydantic V2
* **Infrastructure**: Docker & Docker Compose

---

## API Documentation & Postman

### Interactive Docs (Swagger UI)
Once the app is running, access the automatic documentation here:
- **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

### Postman Collection
You can access the pre-configured Postman collection to test all endpoints using the link below:

[**Click here to join the Postman Team Workspace**](https://app.getpostman.com/join-team?invite_code=7580243e8598a1e90d88fc2ab099425fc3673e301a0faaf8900a5e966ba32170&target_code=e6ada3598190ee097a95495b09938e7f)

---

## How to Run

### Prerequisites
* Docker & Docker Compose installed on your machine.

### Installation Steps

1.  **Clone the repository**
    ```bash
    git clone https://github.com/YuriyHrechka/Spy-Agency
    cd spy_agency
    ```

2.  **Environment Setup**
    Create a `.env` file in the root directory. You can copy the example:
    ```bash
    cp .env.example .env

3.  **Run with Docker**
    ```bash
    docker-compose up --build
    ```

4.  **Access the API**
    The API will be available at `http://localhost:8000`.

---

## Project Structure

```text
├── app/
│   ├── routers/        # API Endpoints (Cats, Missions)
│   ├── config.py       # Configuration & Environment variables
│   ├── session.py      # Database connection & session management   
│   ├── main.py         # Application entry point
│   ├── models.py       # Database Tables (SQLModel)
│   └── schemas.py      # Pydantic Models & Validation
├── .env.dummy                # Environment variables
├── docker-compose.yml  # Docker orchestration
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
# Scraping Backend

The Scraping Backend is a robust Python application designed for web scraping. It leverages modern tools and frameworks such as FastAPI for building APIs, Redis for caching, and Pydantic for data validation.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)

## Features

- Scrapes product data from [Dentalstall](https://dentalstall.com/).
- Stores scraped data in Redis for quick access.
- Saves scraped data to a JSON file for persistent storage.
- **Future Development**: Strategies are in place for saving data to an SQL database, but this functionality is yet to be developed.

## Installation

### Prerequisites

1. **Install Python**: Ensure you have Python 3.7 or higher installed. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Install pip**: Pip is the package manager for Python. It usually comes bundled with Python installations. You can verify if it's installed by running:
   ```bash
   pip --version
   ```

### Steps

1. **Clone the repository:**

```bash
git clone https://github.com/manu-2611/scraping_backend.git
cd scraping-backend

```

2. **Create a virtual environment:**

```bash
python -m venv venv
source venv/scripts/activate
# for windows
venv\Scripts\activate

```

3. **Install the required packages:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

```bash
REDIS_HOST="REDIS_HOST"
REDIS_PORT="REDIS_PORT"
REDIS_DB="REDIS_DB"
STATIC_TOKEN="STATIC_TOKEN"
JSON_FILE_PATH="JSON_FILE_PATH"
SQL_HOST="SQL_HOST"
SQL_PORT="SQL_PORT"
DB_NAME="DB_NAME"
USERNAME="USERNAME"
PASSWORD="PASSWORD"
```

Here’s a suggested **Usage** section for your README.md, tailored for your project that scrapes data from a website and stores it in Redis and a JSON file:

## Usage

To run the scraping application, follow these steps:

1. **Activate the Virtual Environment**: If you created a virtual environment, make sure it is activated. In Command Prompt, run:

   ```bash
   venv\Scripts\activate
   ```

2. **Run the FastAPI application**: Start the FastAPI server using Uvicorn. Run the following command in your project directory:

   ```bash
   uvicorn app.main:app --reload
   ```

   This command assumes your FastAPI application is defined in `main.py` inside the `app` directory. The `--reload` option enables automatic reload on code changes, which is useful during development.

3. **Access the API**: Open your web browser and navigate to:

   ```
   http://127.0.0.1:8000/docs
   ```

   This will open the interactive API documentation where you can test the available endpoints.

4. **Authenticate**: For the POST request to `/products/`, you will need to include the static token in the request header. You can do this using tools like [Postman](https://www.postman.com/) or directly from the API docs. Add the following header:

   ```
   Authorization: Bearer requiredToken  #replace requiredToken with the Token
   ```

5. **Send a POST request**: Use the API to scrape data. You can send a POST request to the `/products/` endpoint with the necessary payload.

6. **Check the output**: After the scraping is completed, the data will be stored in both Redis and a JSON file located at `Products.json` in the project directory.

### Example Request

Here’s an example of how to use `curl` to send a POST request to the `/products/` endpoint:

```bash
curl -X POST http://127.0.0.1:8000/products/ -H "Authorization: Bearer providedToken"
```

### Note

- Ensure Redis is running and accessible at the specified host and port before starting the application.
- You can modify the scraping behavior by adjusting the settings in the code or adding additional parameters as needed.

```

Feel free to adjust any specifics to better fit your project's implementation!
```

## API Endpoints

### 1. Scrape Products

- **Endpoint:** `/products/`
- **Method:** `POST`
- **Description:** Scrapes product data from the specified website and stores it in Redis and a JSON file.
- **Authentication:** Bearer token required.

#### Request Headers

| Header          | Value                  |
| --------------- | ---------------------- |
| `Authorization` | `Bearer mysecrettoken` |

## Request Body for Settings

The following JSON object can be used to configure the scraping settings.

````json
{
  "limit": 10,         // Optional: Limit the number of pages to scrape. Default is null (no limit).
  "proxy": "http://example.com:8080" // Optional: Proxy string to use for scraping. Default is null (no proxy).
}


#### Responses

- **200 OK**

  - **Description:** Successful scraping. Returns the number of products scraped and skipped.
  - **Response Example:**
    ```json
    {
      "count": 2,
      "product_skipped": 12,
      "products": [
        {
          "name": "1 x GDC Extraction Forceps Lo...",
          "price": 850.0,
          "image_url": "https://dentalstall.com/wp-content/uploads/2021/11/GDC-Extraction-Forceps-Lower-Molars-86A-Standard-FX86AS-300x300.jpg"
        },
        {
          "name": "3A MEDES Bleaching And Night ...",
          "price": 1380.0,
          "image_url": "https://dentalstall.com/wp-content/uploads/2023/02/3a-medes-bleaching-and-night-guard-sheets-2-1-300x300.jpg"
        }
      ]
    }
    ```

- **403 Forbidden**

  - **Description:** Invalid token provided in the request.
  - **Response Example:**
    ```json
    {
      "detail": "Invalid token"
    }
    ```

- **422 Unprocessable Entity**
  - **Description:** The request was well-formed but could not be processed due to semantic errors.
  - **Response Example:**
    ```json
    {
      "detail": [
        {
          "loc": ["body"],
          "msg": "field required",
          "type": "value_error.missing"
        }
      ]
    }
    ```

````

## Contributing

We welcome contributions! To get started:

1. **Fork the Repo** and clone it to your machine.
2. **Create a Branch**: `git checkout -b feature/your-feature-name`.
3. **Make Changes** and commit: `git commit -m "Your message"`.
4. **Push** your branch: `git push origin feature/your-feature-name`.
5. **Open a Pull Request**.

For issues or feature requests, please open an issue. Thank you for contributing!

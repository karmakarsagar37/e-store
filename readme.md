# E-commerce Store Backend

This repository contains the backend implementation of an e-commerce store that provides APIs for managing carts, adding items, and performing checkouts. It also includes admin endpoints for generating discount codes and retrieving purchase statistics.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Admin APIs](#admin-apis)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Cart Management:** APIs to add items to a cart for users.
- **Checkout Process:** Endpoint to perform the checkout process. Discount is automatically applied to the cart if the order is supposed to the multiple of Nth's order.For calculating the total amount , we use the latest price of the items in the db so as to avoid inconsistency.
- **Item Management:** APIs for adding items to the database and retrieving all items.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/karmakarsagar37/e-store.git
    ```
2. Create a virtual environment and activate
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Add the Username and Password for the mongodb cluster in the .env file. Also add the value of N. Nth order gets a flat 10% discount

    ```bash
    DB_USERNAME=<DB_USERNAME>
    DB_PASSWORD=<DB_PASSWORD>
    LUCKY_ORDER_NUMBER=2(default)
    ```

4. Run the application:

    ```bash
    python3 -m flask run --host=0.0.0.0
    ```
4. To run the unittests:

    ```bash
    python3 -m unittest tests/unit/*Test.py
    ```

## Usage

The application provides RESTful APIs to manage carts, items, and perform checkouts. The API endpoints are described below.

## API Endpoints

### Cart Management

- **Add Items to Cart:**
  - Endpoint: `/cart/add/<int:user_id>` (POST)
  - Description: Adds items to the cart for a specific user.

- **Checkout:**
  - Endpoint: `/buy/checkout/<int:user_id>` (POST)
  - Description: Performs the checkout process for a specific user.

### Item Management

- **Add Items:**
  - Endpoint: `/items/add` (POST)
  - Description: Adds items to the database.

- **Get All Items:**
  - Endpoint: `/items/get` (GET)
  - Description: Retrieves all items from the database.

## Admin APIs

### Discount Code Generation

- **Generate Discount Code:**
  - Endpoint: `/admin/discount/generate` (POST)
  - Description: Generates a discount code if the condition for the Nth order is satisfied.

### Purchase Statistics

- **Fetch Purchase Statistics:**
  - Endpoint: `/admin/purchase/stats` (GET)
  - Description: Retrieves counts of items purchased, total purchase amount, list of discount codes, and total discount amount.

## PostMan Collection 

  - Link: https://www.postman.com/aerospace-operator-36566911/workspace/e-stores/collection/19113444-22c77635-d944-4c1f-807a-25b5abab597c?action=share&creator=19113444


## License

This project is licensed under the [MIT License](LICENSE).

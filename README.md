# WealthManager Backend – Django + DRF

This is the backend API for the WealthManager Portfolio Dashboard.  
It provides stock holding data, asset allocation, historical performance comparison, and portfolio summaries based on sample Indian stock data.

---

## API Endpoints

Base URL: `/api/portfolio/`

| Endpoint        | Description                              |
|----------------|------------------------------------------|
| `/holdings`    | Returns full list of user's stock holdings |
| `/allocation`  | Returns asset allocation (sector, market cap) |
| `/performance` | Returns historical performance vs Nifty 50 and Gold |
| `/summary`     | Returns total value, top/worst performer, diversification, etc. |

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
`pip install -r requirements.txt`
```
### 2. Run Migrations

```bash
`python manage.py migrate`
```
### 3. Run Server
```
`python manage.py runserver`
```

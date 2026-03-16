# Weekend Scout

A weekend planning agent that browses Yelp, AllTrails, and Google Maps in real time to find you a local restaurant and hiking trail, with driving directions between the two.

## How it works

1. You provide a location
2. The agent searches Yelp for a well-reviewed, affordable restaurant
3. In parallel, it searches AllTrails for a nearby hiking trail
4. Once both finish, it calculates the driving distance between them via Google Maps

## Setup

### Requirements

- Python 3.12+
- Nova Act API key from [nova.amazon.com](https://nova.amazon.com)

### Install dependencies
```bash
pip install nova-act fastapi uvicorn python-dotenv
playwright install chromium
```

### Environment variables

Create a `.env` file in the project root:
```
NOVA_ACT_API_KEY=your-key-here
```

## Usage

### Run as a script
```bash
python hackathon.py
```

### Run as a server
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

Then call the endpoint:
```bash
POST http://localhost:8000/plan
Content-Type: application/json

{ "location": "Duluth GA" }
```

Response:
```json
{
  "restaurant_summary": "...",
  "trail_summary": "...",
  "distance_btw_res_and_trail": "..."
}
```

## Built by

Duc Nguyen

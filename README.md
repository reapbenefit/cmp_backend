# ReapBenefit Changemaker Portfolio AI backend

## Setup

- Create a virtual environment and activate it
```
python -m venv venv
source venv/bin/activate
```
- Install the dependencies
```bash
pip install -r requirements.txt
```
- (Optional) We use [Phoenix by Arize](https://phoenix.arize.com/) for tracing. If you want to use it, either use the Cloud version or [self-host](https://arize.com/docs/phoenix/self-hosting) it.

- Create a `.env` file in the root of the project and add the following variables:
```
OPENAI_API_KEY=your_openai_api_key
PHOENIX_API_KEY=your_phoenix_api_key (optional, if you use phoenix)
PHOENIX_ENDPOINT=your_phoenix_endpoint (optional, only required if you add [authentication](https://arize.com/docs/phoenix/authentication) to your Phoenix instance)
ENV=development (optional, defaults to development)
```

## Running it locally

```bash
cd src; uvicorn main:app --reload --port 8002
```

You can now access the API at `http://localhost:8002`

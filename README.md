# DataMind AI

Autonomous Multi-Agent Data Science Assistant.

## Agents
1. Orchestrator Agent
2. Data Quality Agent
3. Statistical Agent
4. ML Agent
5. Visualization Agent
6. Reviewer Agent

## Run

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The included sample dataset is `data/simulated_weather.xlsx`.

## Example prompts
- Give me a complete analysis of this dataset.
- Find missing values, duplicates and outliers.
- Show correlations between numerical variables.
- Predict Temperature_C.
- Compare suitable machine-learning models.

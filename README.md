# Key Person Risk Index (KPRI)

[![CI](https://github.com/PrakharQuant/key-person-risk/actions/workflows/ci.yml/badge.svg)](https://github.com/PrakharQuant/key-person-risk/actions)

Open-source sectoral index measuring how much stock prices react to CEO/CFO departures.

**Author**: Prakhar Gupta  
Email: [bestofprakhar@gmail.com](mailto:bestofprakhar@gmail.com)  
LinkedIn: [linkedin.com/in/prakhar-gupta-5b7250372](https://www.linkedin.com/in/prakhar-gupta-5b7250372/)  
X (Twitter): [@PrakharQuant](https://x.com/PrakharQuant)  
Personal site: [prakharquant.github.io](https://prakharquant.github.io/)

**Live GitHub Pages**: https://prakharquant.github.io/key-person-risk/

## Headline findings (demo data)
On synthetic/placeholder events, Technology and Healthcare rank higher on KPRI than Automobile and Cement, consistent with the hypothesis that key-person risk is larger in founder-led tech/pharma. Real results require the full 400+ event sample (EDGAR scrape). Sample sizes in current demo are illustrative.

**Confidence**: Bootstrap CIs will be shown on the live site once full data is generated.

## Motivating case (developing, excluded from sample)
**Nvidia, 12 Nov 2026**: CEO Jensen Huang resigned amid personal scandal. CFO Colette Kress named interim CEO. Stock fell ~13% at the open; market capitalization loss exceeded $500 billion.

## Reproduce
```bash
git clone https://github.com/PrakharQuant/key-person-risk.git
cd key-person-risk
make all          # prices → events → study → index → site
make test         # unit tests with synthetic data
```

Optional: set `ANTHROPIC_API_KEY` for LLM-assisted departure classification (results always written with `manual_review_flag`).

## Structure
- `src/kpr/` — pipeline modules
- `data/` — raw parquet cache, events.csv, processed outputs
- `docs/` — static GitHub Pages site (Plotly.js)
- `tests/` — pytest with known-answer synthetic data
- `METHODOLOGY.md`, `LIMITATIONS.md`, `PLAN.md`

## Disclaimer
**This is research, not investment advice.** Correlation is not causation. See [LIMITATIONS.md](LIMITATIONS.md) for survivorship bias, thin samples, yfinance quirks, and other caveats.

## License
MIT

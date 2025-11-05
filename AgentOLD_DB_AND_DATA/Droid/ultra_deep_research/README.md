# Ultra Deep Research CLI

An AI-powered CLI application that performs comprehensive research on any topic using 100+ concurrent search queries and synthesizes the results into high-signal reports.

## Features

- **100+ Diverse Search Queries**: Automatically generates comprehensive search queries covering multiple angles of your topic
- **Concurrent API Execution**: Executes searches in parallel using OpenRouter API integration
- **AI-Powered Synthesis**: Uses advanced reasoning models to distill findings into actionable insights
- **Beautiful CLI Output**: Color-coded progress tracking and formatted reports
- **Automatic Report Saving**: Saves detailed research reports with timestamps

## Setup

1. **Install Dependencies**
   ```bash
   cd ultra_deep_research
   pip install -r requirements.txt
   ```

2. **Configure API Key**
   
   Create a `.env` file in the ultra_deep_research directory:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

   Get your API key from: https://openrouter.ai/

## Usage

### Command Line Interface

**Interactive Mode:**
```bash
python main.py
```
Then enter your research topic when prompted.

**Direct Input:**
```bash
python main.py "quantum computing applications"
```

### Example Topics
- "sustainable energy solutions"
- "artificial intelligence ethics" 
- "space exploration technology"
- "blockchain in healthcare"

## Architecture

```
ultra_deep_research/
├── main.py                 # CLI entry point
├── config.py              # API configuration and settings
├── agents/
│   ├── query_generator.py   # Generates 100 diverse search queries
│   ├── search_dispatcher.py # Manages async API calls
│   └── report_aggregator.py # Final insights generation
├── utils/
│   ├── api_client.py       # OpenRouter API wrapper
│   └── output_formatter.py # Report formatting
└── requirements.txt        # Python dependencies
```

## How It Works

1. **Query Generation**: Uses Haiku 4.5 to create 100 diverse search queries covering different aspects of your topic

2. **Search Execution**: Dispatches 100 concurrent Perplexity API searches via OpenRouter

3. **Result Synthesis**: Processes findings with SOMNET 4.5 to create a comprehensive, high-signal report

4. **Report Generation**: Formats insights into a structured report with statistics and actionable findings

## Configuration

You can modify the behavior by editing `config.py`:

- Change AI models used for different stages
- Adjust concurrent search limits
- Modify timeout and retry settings
- Customize API provider endpoints

## Output

The application generates:
- Real-time progress updates during execution
- Comprehensive research report displayed in terminal
- Detailed report saved to timestamped file
- Search statistics and success rates

## Requirements

- Python 3.8+
- OpenRouter API key
- Internet connection

## Troubleshooting

**API Key Issues:**
- Ensure your OpenRouter API key is valid
- Check that the `.env` file is in the correct directory
- Verify API key has sufficient credits

**Timeout Errors:**
- Increase `REQUEST_TIMEOUT` in `config.py`
- Reduce `MAX_CONCURRENT_SEARCHES` if running into rate limits

**Failed Searches:**
- Some searches may fail due to API limitations
- The system reports success rates and continues with available results

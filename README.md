# 🎭 Sentiment Analysis Application with DistilBERT

An interactive and modern web interface for real-time sentiment analysis using DistilBERT and Streamlit.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)
![Transformers](https://img.shields.io/badge/Transformers-4.35.2-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Screenshots](#screenshots)
- [Model](#model)
- [Development](#development)
- [Contribution](#contribution)
- [License](#license)

## ✨ Features

### 🎯 Sentiment Analysis
- **Real-time Prediction**: Instant sentiment analysis (positive/negative)
- **Confidence Scores**: Visualize the model's confidence level
- **Detailed Probabilities**: Probability distribution for each class

### 📊 Interactive Visualizations
- **Confidence Gauge**: Gauge chart for confidence level
- **Bar Chart**: Compare positive/negative probabilities
- **Real-time Stats**: Track analysis history

### 🎨 User Interface
- **Modern and Responsive Design**: Sleek interface with custom CSS
- **Example Mode**: Predefined texts for quick testing
- **Analysis History**: Store last 5 analyses
- **Informative Sidebar**: Model info and statistics

### 🔧 Technical Features
- **Model Caching**: Optimized loading with `@st.cache_resource`
- **Error Handling**: Clear and informative error messages
- **Multi-Model Support**: Ability to use different models

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Minimum 2 GB RAM (for the model)

### Installation Steps

1. **Clone the repository (or download the files)**

```bash
git clone https://github.com/mazygh/project_analysis_sentiment
cd sentiment-analysis-app

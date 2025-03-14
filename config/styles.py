CSS_STYLES = """
    <style>
        .stApp {
            background-color: #1a1f2c;
        }
        .chat-row {
            display: flex;
            margin: 5px;
            width: 100%;
        }
        .row-reverse {
            flex-direction: row-reverse;
        }
        .chat-bubble {
            font-family: "Source Sans Pro", sans-serif;
            border: 1px solid transparent;
            padding: 5px 10px;
            margin: 0px 7px;
            max-width: 70%;
            border-radius: 10px;
            overflow-x: auto;
        }
        .user-bubble {
            background-color: #FFF;
            color: #000;
            border-radius: 20px;
        }
        .assistant-bubble {
            background: #FECA05;
            color: #000;
        }
        .chat-icon {
            border-radius: 5px;
        }
        [data-testid="stFormSubmitButton"] button {
            background-color: #FECA05;
            color: #000;
            border-radius: 10px;
            border: none;
            width: 100%;
            height: 40px;
            font-weight: 500;
        }
        
        .metric-container {
            background-color: #2d3748;
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid #4a5568;
            min-height: 180px;
            height: auto;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin-bottom: 1rem;
            overflow: hidden;
        }
        .metric-title {
            color: #ffffff;
            font-size: clamp(1rem, 3vw, 1.25rem);
            font-weight: bold;
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }
        .metric-value {
            color: #ffffff;
            font-weight: bold;
            text-align: center;
            font-size: clamp(1.25rem, 3vw, 2.5rem);
            line-height: 1.2;
            margin: 0.5rem 0;
            word-break: break-word;
        }
        .metric-delta-positive,
        .metric-delta-negative {
            font-size: clamp(0.75rem, 2vw, 1rem);
            display: inline-block;
            margin-top: 0.5rem;
            padding: 0.5rem 0.5rem;
            border-radius: 5px;
            word-wrap: break-word;
            overflow-wrap: break-word;
            hyphens: auto;
            text-align: center;
            width: fit-content;
            margin: 0.5rem auto;
        }
        .metric-delta-positive {
            background-color: #065F46;
            color: #6EE7B7;
        }
        .metric-delta-negative {
            background-color: #991B1B;
            color: #FCA5A5;
        }
        .stColumn {
            padding: 0.5rem !important;
        }
        @media screen and (max-width: 768px) {
        .metric-container {
                min-height: 150px; 
                text-align: center;
            }
        .metric-title {
            font-size: 1.5rem;
        }
        .metric-value {
            font-size: 1.5rem;
        }
        .metric-delta-positive,
        .metric-delta-negative {
            font-size: 0.75rem;
        }
        .stColumn {
                padding: 0.25rem !important;
            }
        }
        .stSelectbox [data-baseweb="select"] span {
            color: black !important;
        }
        .stMultiSelect [data-baseweb="select"] span {
            color: black !important;
        }
        .sidebar-logo {
            margin-bottom: 2rem;
        }
        .sidebar-logo img {
            max-width: 100%;
            height: auto;
        }
        .chart-title {
            color: #ffffff;
            font-size: 1.5rem;
            font-weight: bold;
            margin: 2rem 0 1rem 0;
        }
        .chat-bubble img {
            border-radius: 10px;
            margin: 5px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .styled-table {
            border-collapse: collapse;
            margin: 1rem 0;
            width: 100%;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }
        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
            border: 1px solid #fff;
        }
        .styled-table thead tr {
            background-color: #FECA05;
            color: #000;
            text-align: left;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #ddd;
            color: #000;
        }
        .styled-table tbody tr:last-of-type {
            border-bottom: 1px solid #fff;
        }
    </style>
"""
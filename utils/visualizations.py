import plotly.graph_objects as go
import pandas as pd

def create_agent_performance_chart(df: pd.DataFrame, n_agents: int, direction: bool) -> go.Figure:
    """Create a double bar chart for agent performance with validation"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for the selected filters",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(color="white", size=16)
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#FFFFFF',
            height=400
        )
        return fig
    
    
    df_sorted = df.groupby('agentname').agg({
        'download': 'sum',
        'mau': 'sum'
    }).reset_index().sort_values('download', ascending=direction).head(n_agents)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Downloads',
        x=df_sorted['agentname'],
        y=df_sorted['download'],
        marker_color='#FFD700',
        hoverinfo='text',
        hoverlabel=dict(bgcolor='rgba(255, 215, 0, 0.5)', font_color='#000', namelength=0),
        hovertext=df_sorted['download'].apply(lambda d: f"Downloads: <b>{d}</b>"),
    ))
    
    fig.add_trace(go.Bar(
        name='MAU',
        x=df_sorted['agentname'],
        y=df_sorted['mau'],
        marker_color='#FFFFFF',
        hoverinfo='text',
        hoverlabel=dict(bgcolor='rgba(255, 255, 255, 0.5)', font_color='#000', namelength=0),
        hovertext=df_sorted['mau'].apply(lambda m: f"MAU: <b>{m}</b>"),
    ))
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#FFFFFF',
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        legend=dict(
            orientation="h",    
            yanchor="bottom",  
            y=1.15,          
            xanchor="center", 
            x=0.5,            
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF')
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#FFFFFF'),
            tickangle=45
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#FFFFFF')
        )
    )
    
    return fig
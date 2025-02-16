from exploralytics.visualize import Visualizer
import plotly.express as px
import plotly.graph_objects as go

viz = Visualizer(
    color="#94C973",                    # Default color for plot elements
    height=768,                         # Plot height in pixels
    width=1366,                         # Plot width in pixels
    template="simple_white",            # Plotly template
    colorscale=px.colors.diverging.Earth,  # Color scale for heatmaps
    texts_font_style="Poppins",           # Font family
)

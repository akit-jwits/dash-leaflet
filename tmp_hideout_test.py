import dash
from dash import html
import dash_leaflet as dl
from dash_extensions.javascript import assign

app = dash.Dash(__name__)

hideout = {"test": "working", "color": "red", "feature": "power_line"}

app.layout = html.Div([
    html.H1("VectorTileLayer Hideout Test"),
    html.P("Check console for 'hideout works: working'"),
    dl.Map([
        dl.TileLayer(),
        dl.VectorTileLayer(
            url="https://openinframap.org/tiles/{z}/{x}/{y}.pbf",
            hideout=hideout,
            style=assign("""
                function(feature, layer_name, zoom, context) {
                    if (context && context.hideout) {
                        return {color: context.hideout.color, weight: 2};
                    }
                    return {color: 'blue', weight: 1};
                }
                """),
            filter=assign("""
                function(feature, layer_name, zoom, context) {
                    if (context && context.hideout) {
                        return layer_name === context.hideout.feature;
                    }
                    return false;
                }
                """),
            attribution="&copy; OpenStreetMap & OpenInfraMap contributors"
        )
    ], style={'height': '400px'}, center=[51.5, -0.1], zoom=10)
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)
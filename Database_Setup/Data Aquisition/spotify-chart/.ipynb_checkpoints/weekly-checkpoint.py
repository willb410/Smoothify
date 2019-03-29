from fycharts import SpotifyCharts

api = SpotifyCharts.SpotifyCharts()
api.top200Weekly(output_file = 'top_200_weekly_.csv', region = 'us')
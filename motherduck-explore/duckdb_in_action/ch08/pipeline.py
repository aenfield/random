import dlt
from chess import source

pipeline = dlt.pipeline(
    pipeline_name = 'my_chess_pipeline',
    destination = 'duckdb',
    dataset_name = 'main'
)

data = source(
    players = [
        'magnuscarlsen', 'vincentkeymer', 'dommarajugukesh', 'rpragchess'
    ],
    start_month = '2022/11',
    end_month = '2022/11'
)

# players_profiles = data.with_resources('players_profiles')
players_profiles = data.with_resources('players_profiles', 'players_games')

info = pipeline.run(players_profiles)
print(info)

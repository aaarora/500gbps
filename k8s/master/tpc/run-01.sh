python3 main.py --source=10.16.23.100:2094 --destination=10.16.23.5:2094 --numStreams=1 --numBatches=1 --start=0   --stop=500  & # Starlight --> UCSD-01 3873
python3 main.py --source=10.16.25.100:2095 --destination=10.16.25.5:2095 --numStreams=1 --numBatches=1 --start=0   --stop=500  & # Starlight --> UCSD-01 3874
python3 main.py --source=10.0.11.100:2094  --destination=10.0.11.5:2096  --numStreams=1 --numBatches=1 --start=500 --stop=1000 & # Caltech --> UCSD-01 3811
python3 main.py --source=10.0.12.100:2095  --destination=10.0.12.5:2097  --numStreams=1 --numBatches=1 --start=500 --stop=1000 & # Caltech --> UCSD-01 3812

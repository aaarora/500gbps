python3 main.py --source=10.16.23.100:2094 --destination=10.16.23.6:2094 --numStreams=1 --numBatches=1 --start=0 --stop=500 & # Starlight --> UCSD-02 3873
python3 main.py --source=10.16.25.100:2095 --destination=10.16.25.6:2095 --numStreams=1 --numBatches=1 --start=0 --stop=500 & # Starlight --> UCSD-02 3874
python3 main.py --source=10.0.11.100:2094  --destination=10.0.11.6:2096  --numStreams=1 --numBatches=1 --start=0 --stop=500 & # Caltech --> UCSD-02 3811
python3 main.py --source=10.0.12.100:2095  --destination=10.0.12.6:2097  --numStreams=1 --numBatches=1 --start=0 --stop=500 & # Caltech --> UCSD-02 3812

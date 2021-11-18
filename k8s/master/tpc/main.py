from scheduler import TransferScheduler
from utils import checkSocket 

import argparse
import logging
import sys

def main(args) -> None:
  logging.basicConfig(
    filename='transfer.log', 
    filemode='w', 
    level=logging.INFO, 
    format='%(asctime)s  %(levelname)s - %(message)s', 
    datefmt='%Y%m%d %H:%M:%S'
  )

  if not checkSocket(args.source, args.destination):
    sys.exit(1)
  
  tsched = TransferScheduler(
    args.source, 
    args.destination, 
    args.numTransfers, 
    ags.numBatches, 
    args.numStreams
  )
  tsched.startTransfers()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Run TPC Tests')
  parser.add_argument('--source', type=str, help='Source Server:PORT')
  parser.add_argument('--destination', type=str, help='Dest Server:PORT')
  parser.add_argument('--numTransfers', type=int, help='# of Transfers')
  parser.add_argument('--numBatches', type=int, help='# of Batches (of Transfers)')
  parser.add_argument('--numStreams', type=int, help='# of Streams')
  args = parser.parse_args()
  main(args)

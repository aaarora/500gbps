from scheduler import TransferScheduler
from utils import checkSocket 

import argparse
import logging

def main(args) -> None:
  logging.basicConfig(filename='transfer.log', 
  filemode='w', 
  level=logging.INFO, 
  format='%(asctime)s  %(levelname)s - %(message)s', 
  datefmt='%Y%m%d %H:%M:%S')

  XRDPORT = 2094
  checkSocket(args.source, args.destination, port=XRDPORT)
  
  tsched = TransferScheduler(args.source, args.destination, XRDPORT, args.numTransfers)
  tsched.startTransfers()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Run TPC Tests')
  parser.add_argument('--source', type=str, help='Source Server')
  parser.add_argument('--destination', type=str, help='Source Server')
  parser.add_argument('--numTransfers', type=int, help='Source Server')
  args = parser.parse_args()
  main(args)

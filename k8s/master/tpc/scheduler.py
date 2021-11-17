import logging
import asyncio

from aiomultiprocess import Pool
from math import ceil

class TransferScheduler:
  def __init__(self, source, destination, xrdport: int, numTransfers: int, numBatches: int, numStreams: int):
    self.source = source
    self.destination = destination
    self.xrdport = xrdport
    self.numTransfers = numTransfers
    self.numBatches = numBatches
    self.numStreams = numStreams
  
  def makeTransferQueue(self, start, stop):
    logging.info("Building queue...")
    for num in range(start, stop):
      logging.debug(f"Added {num}/{self.numTransfers} transfers to queue")
      cmd = ['curl', '-L', '-X', 'COPY']
      cmd += ['-H', 'Overwrite: T']
      cmd += ['-H', f'X-Number-Of-Streams: {self.numStreams}']
      cmd += ['-H', f'Source: https://{self.source}:{self.xrdport}/testSourceFile{num}']
      cmd += [f'https://{self.destination}:{self.xrdport}/testDestFile{num}']
      cmd += ['--capath', '/etc/grid-security/certificates/']
      yield cmd
    logging.info("Queue built successfully")

  @staticmethod
  async def worker(cmd) -> None:
    while True:
      process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
      )
      
      stdout, stderr = await process.communicate()
      result = stdout.decode().strip()
      print(result)

  async def runTransfers(self, start, stop) -> None:
    queue = self.makeTransferQueue(start, stop)

    logging.info("Starting Transfers")
    async with Pool(processes=4) as pool:
      await pool.map(self.worker, queue)

  def startTransfers(self) -> None:
    batchSize = ceil(self.numTransfers/self.numBatches)
    for b in range(self.numBatches):
      start = b*batchSize
      stop = min(self.numTransfers, (b+1)*batchSize)
      asyncio.run(self.runTransfers(start, stop))

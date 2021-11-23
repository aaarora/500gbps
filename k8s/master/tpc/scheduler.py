import logging
import asyncio

from aiomultiprocess import Pool
from math import ceil

class TransferScheduler:
  def __init__(self, source, destination, protocol, start: int, stop: int, numBatches: int, numStreams: int, numProcs: int):
    self.source = source
    self.destination = destination
    self.protocol = protocol
    self.start = start
    self.stop = stop
    self.numBatches = numBatches
    self.numStreams = numStreams
    self.numProcs = numProcs
  
  def makeTransferQueue(self, bStart, bStop):
    logging.info("Building queue...")
    numTransfers = self.stop - self.start
    for num in range(bStart, bStop):
      logging.debug(f"Added {num}/{numTransfers} transfers to queue")
      cmd = ['curl', '-L', '-X', 'COPY']
      cmd += ['-H', 'Overwrite: T']
      cmd += ['-H', f'X-Number-Of-Streams: {self.numStreams}']
      cmd += ['-H', f'Source: {self.protocol}://{self.source}/testSourceFile{num}']
      cmd += [f'{self.protocol}://{self.destination}/testDestFile{num}']
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

  async def runTransfers(self, bStart, bStop) -> None:
    queue = self.makeTransferQueue(bStart, bStop)

    logging.info("Starting Transfers")
    async with Pool(processes=self.numProcs) as pool:
      await pool.map(self.worker, queue)

  def startTransfers(self) -> None:
    numTransfers = self.stop - self.start
    batchSize = ceil(numTransfers/self.numBatches)
    for b in range(self.numBatches):
      bStart = self.start + b*batchSize
      bStop = min(self.stop, self.start + (b+1)*batchSize)
      asyncio.run(self.runTransfers(bStart, bStop))

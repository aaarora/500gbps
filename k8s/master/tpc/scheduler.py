import logging
import asyncio

from aiomultiprocess import Pool

class TransferScheduler:
  def __init__(self, source, destination, xrdport, numTransfers):
    self.source = source
    self.destination = destination
    self.xrdport = xrdport
    self.numTransfers = numTransfers
  
  def makeTransferQueue(self):
    logging.info("Building queue...")
    for num in range(self.numTransfers):
      logging.debug(f"Added {num}/{self.numTransfers} transfers to queue")
      cmd = ['curl', '-L', '-X', 'COPY']
      cmd += ['-H', 'Overwrite: T']
      cmd += ['-H', f'Source: https://{self.source}:{self.xrdport}/testSourceFile{num}']
      cmd += [f'https://{self.destination}:{self.xrdport}/testDestFile{num}']
      cmd += ['--capath', '/etc/grid-security/certificates/']
      yield cmd
    logging.info("Queue built successfully")

  @staticmethod
  async def worker(cmd) -> None:
    while True:
      process = await asyncio.create_subprocess_exec(
      *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
      stdout, stderr = await process.communicate()
      result = stdout.decode().strip()

  async def runTransfers(self) -> None:
    queue = self.makeTransferQueue()

    logging.info("Starting Transfers")
    async with Pool() as pool:
        await pool.map(self.worker, queue)

  def startTransfers(self) -> None:
    asyncio.run(self.runTransfers())

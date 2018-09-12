from crawler import TransferMarktCrawler as TMC

def main(event, context):
    tmc = TMC(10,15)
    tmc.start()
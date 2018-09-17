from crawler import TransferMarktCrawler as TMC

def main(event, context):
    tmc = TMC(0,3)
    tmc.start()
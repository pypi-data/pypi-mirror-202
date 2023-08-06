import logging
import datetime

from pathlib import Path
import sys
workspace_root=str(Path(__file__).parents[1])
sys.path.append(workspace_root)

#import yolo_roof.export
from yolo_roof.geo_functions import image_download 
from yolo_roof.detect_functions import load_yolo_model, roof_predict
from yolo_roof.report_functions import generate_report#, zip_download_file

import os
#os.path.realpath(__file__)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#backend_tester.basicConfig(filename="./backend_tester "+str(datetime.datetime.now())+".log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
backend_tester = logging.getLogger("backend_tester")
backend_tester.setLevel(logging.INFO)
log_file_handler=logging.FileHandler(filename="./backend_tester "+str(datetime.datetime.now())+".log")
log_file_formatter=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_file_handler.setFormatter(log_file_formatter)
backend_tester.addHandler(log_file_handler)

yolo_roof_model = load_yolo_model("./best_roof.pt")
yolo_damage_model = load_yolo_model("./best_damage.pt")
yolo_equipment_model = load_yolo_model("./best_equipment.pt")

#address="2232 Isle Royale Ln, Davis, CA 95616"
addresses_generic = [
    # generic testcases
    #"2232 Isle Royale Ln, Davis, CA 95616",
    #"1 E SIDE SQ, MACOMB, IL 61455-2213", 
    #"1 HEATHER HL, BOURBONNAIS, IL 60914-1622",
    #"1 INDIANA SQ STE 1200, INDIANAPOLIS, IN 46204-2066",
    #"1 OAKBROOK CTR SPC 217, OAK BROOK, IL 60523-1809",
    #"1 S HARRISON ST, ASHLEY, OH 43003-7518",
    #"1 S WACKER DR STE 3250B, CHICAGO, IL 60606-4639",
    #"1 TOWNE SQ STE 800, SOUTHFIELD, MI 48076-3723",
    #"1 VIRGINIA AVE, INDIANAPOLIS, IN 46204-3644",
    #"1 WOODCREST DR, HIGHLAND, IL 62249",
    #"10 E 375 N, REYNOLDS, IN 47980-8025",
    "10 N 3RD ST, LAFAYETTE, IN 47901-1296",
    "10 N MARTINGALE RD STE 400, SCHAUMBURG, IL 60173-2411",
    "100 MAPLE PARK BLVD, SAINT CLAIR SHORES, MI 48081-2200",
    "100 N CHESTNUT ST, CHAMPAIGN, IL 61820-4856",
]

addresses_special = [
    # special testcases
    "6200 South Gilmore Rd, Fairfield, OH",
    "1 Apple Park Way, Cupertino, CA 95014",
    "66 Bluff Ct Trout Valley, IL 60013"
]

business_name="My home"
email="qiang_wang@cinfin.com"

for address in addresses_generic:
    try:
        image_download(address, business_name, "./")
        roof_predict(yolo_roof_model, yolo_damage_model, yolo_equipment_model, "./")
        generate_report("./")
    except Exception as inst:
        backend_tester.error(f"{address} failed: {inst}")
    else:
        backend_tester.info(f"{address} success.")
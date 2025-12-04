import sys
sys.path.append(".") # Test scripts use modules too (run from toplevel tho)

from Tools import FormatActions

rawResponse = """testtesttest
1. **Label1**: desc1desc1desc1, desc1desc1.
2. **Label3**: desc2desc2desc2, desc1desc2.
3. **Label3**: desc3desc3desc3, desc1desc3.
testtesttest

testtesttest"""

formattedResponse = FormatActions(rawResponse)
print(f"formatted=\n{formattedResponse}")

print("unpacked=")
for k,v in formattedResponse.items(): print(f"{k} : {v}")
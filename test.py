import requests
import csv
import statistics
import time

API_URL = "http://localhost:8000/prompt"
API_KEY = "B0T_1N_TH3_B4NK" 

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def send_message(message):
    data = {"message": message}
    resp = requests.post(API_URL, headers=headers, json=data)
    return resp.json()

start_time=time.time()

results=[]
failed_results=[]

with open("../test_cases3.csv", encoding="utf-8") as f:
    reader=csv.DictReader(f)
    for row in reader:
        user_input=row["unos"]
        expected_intent=row["ocekivani_intent"]

        response=send_message(user_input)

        actual_intent=response.get("intent","")
        confidence=response.get("confidence",0)

        passed=(actual_intent==expected_intent)



        result_row={
            "unos":user_input,
            "ocekivani_intent":expected_intent,
            "intent":actual_intent,
            "confidence":confidence,
            "prolaz":"TOČNO" if passed else "NETOČNO"
        }

        results.append(result_row)

        if not passed:
            failed_results.append(result_row)


passing_confidences=[]

with open("../tocni_odgovori.csv",encoding="utf-8") as f:
    reader=csv.DictReader(f)
    for row in reader:
        user_input=row["unos"]
        response=send_message(user_input)

        confidence=response.get("confidence",0)
        passing_confidences.append(confidence)

median_confidence=statistics.median(passing_confidences)
print(median_confidence)


if passing_confidences: 
    avg_confidence_for_correct=round(sum(passing_confidences)/len(passing_confidences))
else:
    avg_confidence_for_correct=0

under_median=[]
for r in results:
    if r["confidence"]<median_confidence:
        r["iznad_mediana"]="NE"
        under_median.append(r)
    else:
        r["iznad_mediana"]="DA"

with open("../results.csv","w",newline="",encoding="utf-8") as f:
    fieldnames=["unos","ocekivani_intent","intent","confidence","prolaz","iznad_mediana"]
    writer=csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

with open("../failed.csv","w",newline="",encoding="utf-8") as f:
    fieldnames=["unos","ocekivani_intent","intent","confidence","prolaz","iznad_mediana"]
    writer=csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(failed_results)

with open("../low_confidence.csv","w",newline="",encoding="utf-8") as f:
    fieldnames=["unos","prolaz","iznad_mediana"]
    writer=csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader()
    for r in under_median:
        writer.writerow({k: r[k] for k in fieldnames})


end_time=time.time()
print(f"Vrijeme izvršavanja: {end_time - start_time:.2f} sekundi.")



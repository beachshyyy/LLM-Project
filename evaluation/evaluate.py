import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation

from openpyxl import load_workbook

from app.services.ocr import extract_text
from app.services.extraction import extract_receipt


BASE_DIR = Path(__file__).resolve().parent.parent

EXCEL_FILE = BASE_DIR / "evaluation" / "ground_truth.xlsx"
IMAGE_DIR = BASE_DIR / "evaluation" / "dataset" / "images"
OUTPUT_FILE = BASE_DIR / "evaluation" / "evaluation_results.csv"


def normalize_amount(value):
    if value is None:
        return None

    try:
        return Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return None


def load_ground_truth():
    workbook = load_workbook(EXCEL_FILE, data_only=True)
    sheet = workbook["Receipts"]

    headers = {
        cell.value: index
        for index, cell in enumerate(sheet[1])
    }

    if "filename" not in headers or "gold_total" not in headers:
        raise ValueError(
            "Excel must contain filename and gold_total columns."
        )

    records = {}

    for row in sheet.iter_rows(min_row=2, values_only=True):
        filename = row[headers["filename"]]
        gold_total = row[headers["gold_total"]]

        if filename:
            records[str(filename)] = gold_total

    return records


def evaluate():
    ground_truth = load_ground_truth()
    results = []

    for filename, gold_total in ground_truth.items():
        image_path = IMAGE_DIR / filename

        print(f"\nProcessing: {filename}")

        if not image_path.exists():
            print("Image not found. Skipping.")
            continue

        try:
            # OCR (ทำครั้งเดียว ใช้ร่วมกันทั้งสองวิธี)
            from PIL import Image

            image = Image.open(image_path)
            ocr_text = extract_text(image)

            # Baseline: ไม่ใช้ Retrieval
            baseline_receipt = extract_receipt(
                ocr_text,
                use_retrieval=False
            )

            # RAG: ใช้ Retrieval
            rag_receipt = extract_receipt(
                ocr_text,
                use_retrieval=True
            )

            gold = normalize_amount(gold_total)
            baseline_total = normalize_amount(
                baseline_receipt.total
            )
            rag_total = normalize_amount(
                rag_receipt.total
            )

            baseline_correct = (
                baseline_total is not None
                and baseline_total == gold
            )

            rag_correct = (
                rag_total is not None
                and rag_total == gold
            )

            results.append({
                "filename": filename,
                "gold_total": str(gold),
                "baseline_total": str(baseline_total)
                    if baseline_total is not None else "",
                "baseline_correct": baseline_correct,
                "rag_total": str(rag_total)
                    if rag_total is not None else "",
                "rag_correct": rag_correct
            })

            print(f"Gold: {gold}")
            print(f"Baseline: {baseline_total} ({baseline_correct})")
            print(f"RAG: {rag_total} ({rag_correct})")

        except Exception as error:
            print(f"Error: {error}")

            results.append({
                "filename": filename,
                "gold_total": str(gold_total),
                "baseline_total": "",
                "baseline_correct": False,
                "rag_total": "",
                "rag_correct": False
            })

    if not results:
        print("No results to evaluate.")
        return

    # บันทึกผลลง CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    # คำนวณ Accuracy
    total = len(results)

    baseline_accuracy = (
        sum(row["baseline_correct"] for row in results)
        / total * 100
    )

    rag_accuracy = (
        sum(row["rag_correct"] for row in results)
        / total * 100
    )

    print("\n========== EVALUATION SUMMARY ==========")
    print(f"Total receipts: {total}")
    print(f"Baseline Accuracy: {baseline_accuracy:.2f}%")
    print(f"RAG Accuracy: {rag_accuracy:.2f}%")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    evaluate()


import csv
from pathlib import Path

import qscript


CSV_FILE = Path(__file__).parent / "input.csv"

qscript.PATH_TO_VIDEO_FOLDER = str(
    Path(__file__).parent / "video"
)


def main():

    if not CSV_FILE.exists():
        print(f"CSV file not found: {CSV_FILE}")
        return

    with open(
        CSV_FILE,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(
            file,
            delimiter=";",
            quotechar='"'
        )

        required_columns = [
            "URL",
            "Company Name",
            "Language",
            "Country",
            "Postcode",
            "City",
            "Street",
            "HouseNo"
        ]

        if reader.fieldnames != required_columns:
            print("Invalid CSV header!")
            print("Expected:", required_columns)
            print("Received:", reader.fieldnames)
            return

        for row_number, row in enumerate(reader, start=1):

            print("\n" + "=" * 50)
            print(f"Processing row {row_number}")
            print(f"Company: {row['Company Name']}")
            print("=" * 50)

            try:

                video_path = qscript.CaptureVideo_Magento(
                    url=row["URL"],
                    company_name=row["Company Name"],
                    language=row["Language"],
                    country=row["Country"],
                    postcode=row["Postcode"],
                    city=row["City"],
                    street=row["Street"],
                    house_no=row["HouseNo"]
                )

                if video_path:
                    print(f"SUCCESS: {video_path}")

                else:
                    print("FAILED: Video was not created")
                    print("Stopping CSV processing.")
                    break

            except Exception as error:

                print(f"Unexpected error: {error}")
                print("Stopping CSV processing.")
                break

    print("\nCSV processing finished!")


if __name__ == "__main__":
    main()

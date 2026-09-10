import csv

# Lists to store postcode information
Postcode = []
In_Use = []
Latitude = []
Longitude = []
LSOA_Code = []
LSOA_Name = []

# Postcode areas we want
areas = ["EH1", "EH2", "EH3", "EH6", "EH12"]

# Dictionary to group postcodes by LSOA
LSOA_Groups = {}

# Open CSV file
with open('Edinburgh_Postcode.csv', 'r') as file:

    reader = csv.reader(file)

    # Skip header
    next(reader)

    for row in reader:

        # Only keep postcodes currently in use
        if row[1] != 'Yes':
            continue

        # Get postcode area
        postcode_area = row[0].split()[0]

        # Only keep the areas we want
        if postcode_area not in areas:
            continue

        # Store postcode information
        Postcode.append(row[0])
        In_Use.append(row[1])
        Latitude.append(row[2])
        Longitude.append(row[3])
        LSOA_Code.append(row[15])
        LSOA_Name.append(row[16])

        # Get LSOA name
        lsoa = row[16]

        # Create LSOA group if it doesn't exist
        if lsoa not in LSOA_Groups:
            LSOA_Groups[lsoa] = []

        # Add postcode to its LSOA
        LSOA_Groups[lsoa].append({
            'Postcode': row[0],
            'Latitude': row[2],
            'Longitude': row[3]
        })

# Print the postcodes being kept
print("\nPOSTCODES KEPT:\n")

for postcode, latitude, longitude, lsoa_code, lsoa_name in zip(
    Postcode, Latitude, Longitude, LSOA_Code, LSOA_Name
):
    print(
        f"Postcode: {postcode}, "
        f"Latitude: {latitude}, "
        f"Longitude: {longitude}, "
        f"LSOA Code: {lsoa_code}, "
        f"LSOA Name: {lsoa_name}"
    )

# Print totals
print("\n-------------------------")
print("Total active postcodes:", len(Postcode))
print("Total LSOAs:", len(LSOA_Groups))
print("-------------------------")

# Display LSOAs and how many postcodes are in each
#for lsoa, postcodes in LSOA_Groups.items():
   # print(f"\nLSOA: {lsoa}")
   # print(f"Number of postcodes: {len(postcodes)}")


with open("saved_postcodes.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Postcode", "Latitude", "Longitude", "LSOA Code", "LSOA Name"])
    for postcode, latitude, longitude, lsoa_code, lsoa_name in zip(
        Postcode, Latitude, Longitude, LSOA_Code, LSOA_Name
    ):
        writer.writerow([postcode, latitude, longitude, lsoa_code, lsoa_name])
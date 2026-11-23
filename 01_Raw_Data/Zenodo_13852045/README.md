# Zenodo record 13852045 — original CSV placement

The two original files audited in the working record should be placed here unchanged:

1. Fig1e.Daily driving distance of different vehicle types.csv
   - Expected MD5: 17a1dc8d71af0b3767987eab294c0bc6
   - Expected SHA-256: 29c99684e665d0f8139a02bcc10751575d550680b903e26013590f82fac2a05f

2. FigSI5.Distributions of average daily driving distance by vehicle type.csv
   - Expected MD5: b66cad7047d3f496adb70e4a99b52058
   - Expected SHA-256: d2af33165824b1d50b318bd41f85fb17555d648abfd0cf09bb3e7ef6a06909cf

Source: https://zenodo.org/records/13852045

The files are not included in this repository yet. After placing the original bytes here, run:

```bash
python 03_Data_Audit/audit_zenodo_13852045.py
```

The audit script creates analysis copies under 02_Cleaned_Data/Zenodo_13852045 and a report under 03_Data_Audit/Logs. It never edits the raw files.

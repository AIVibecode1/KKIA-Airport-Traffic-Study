About Dataset
The King Khalid International Airport Flights Dataset provides comprehensive flight movement data for both arrivals and departures at King Khalid International Airport (RUH / OERK), located in Riyadh, Saudi Arabia. This airport serves as a major hub for domestic and international air traffic across the Middle East.

The dataset was collected from multiple aviation and flight-tracking APIs, then cleaned, merged, and standardized into a single file stored in the efficient Apache Parquet format. Parquet ensures compact storage, faster read performance, and compatibility with modern data processing frameworks.

It contains a total of 153,308 records and 23 columns,each record includes detailed flight information such as flight number, aircraft model and registration, airline identifiers (IATA/ICAO), movement type (arrival or departure), flight status, cargo indicator, terminal, and scheduled times in both UTC and local time zones. It also contains structured information describing both origin and destination airports, including their IATA/ICAO codes, airport names, and time zones.

This dataset is suitable for data scientists, researchers, and aviation analysts interested in airport traffic analytics, flight scheduling patterns, operational efficiency, delay prediction, and airline performance studies. Its clear schema and consistent structure make it ideal for use in data visualization, statistical modeling, and machine learning projects.

You can work with this dataset using a variety of modern tools and frameworks, such as:

Python (Pandas, Polars, PyArrow, FastParquet) for data exploration and processing
Jupyter or Kaggle Notebooks for interactive analysis and prototyping.
Power BI or Tableau for data visualization and reporting.
Apache Spark, DuckDB, or Dask for large-scale data handling.
Matplotlib, Seaborn, or Plotly for data visualization and trend analysis.
SQL-based analytical databases such as PostgreSQL, Amazon Redshift, Google BigQuery, or Snowflake for structured querying.
The King Khalid International Airport Flights Dataset provides a structured, real-world view of air traffic activity in one of the Middle East’s most significant transportation hubs and is ready for advanced analysis and research applications.


---

Here is below the metadata description for the columns:-

flight_number: The airline-designated public flight identifier (e.g., SV104, XY230).
aircraft.model: The aircraft’s make and model, such as “Airbus A320” or “Boeing 777-300ER.”
aircraft.reg: The aircraft’s unique registration or tail number (e.g., HZ-AK12).
aircraft.modeS: The 24-bit ICAO transponder code used for radar and ADS-B tracking.
airline.name: The full name of the operating airlin (e.g, Saudi Arabian,flynas).
airline.iata: The airline’s two-letter IATA code (commercial usage).
airline.icao: The airline’s three-letter ICAO code (operational usage).
status: The current or final operational state of the flight (Departed,Cancelled, etc.).
flight_type: The type or category of the flight (Departure, Arrival.).
codeshareStatus: Indicates whether the flight is a primary or shared (codeshare) operation.
isCargo: Boolean field specifying if the flight is predominantly for cargo.
callSign: The radio callsign used by Air Traffic Control for the flight (usually airline + number).
origin_airport_name: The full name of the airport where the flight departs (e.g., King Khalid International Airport).
origin_airport_icao: The four-letter ICAO code for the departure airport (e.g., OERK).
origin_airport_iata: The three-letter IATA code for the departure airport (e.g., RUH).
movement.terminal: The terminal at the origin airport used for this flight.
movement.quality: The quality or reliability level of the movement data (Basic, Confirmed, Live, etc.).
destination_airport_icao: The four-letter ICAO code of the destination airport (e.g., OMDB).
destination_airport_iata: The three-letter IATA code of the destination airport (e.g., DXB).
destination_airport_name: The full name of the destination airport.
movement.airport.timeZone: The time zone of the destination airport (e.g., Asia/Dubai).
movement.scheduledTime.utc: The scheduled time (departure or arrival) in UTC format.
movement.scheduledTime.local: The same scheduled time in the local timezone of the movement airport.

---

Note from the data owner: I've been running some analyses of this dataset recently, and they all have the same error. I'd like to tell you that there's a trick no one has noticed. As a hint, if the number of rows is approximately 150,000, it doesn't mean there are 150,000 trips.

Pay close attention to some of the columns.
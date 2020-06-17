class SqlQueries:
    
    CREATE_US_DEMOGRAPH_TABLE_SQL = ("""
        CREATE TABLE IF NOT EXISTS public.us_cities_demographics (
                city VARCHAR,
                state VARCHAR,
                median_age FLOAT,
                male_population FLOAT,
                female_population FLOAT,
                total_population FLOAT,
                number_of_veterans FLOAT,
                foreign_born FLOAT,
                average_household_size FLOAT,
                state_code VARCHAR,
                race VARCHAR,
                count INT
        );
    """)


    CREATE_AIRPORT_CODES_TABLE_SQL = ("""
        CREATE TABLE IF NOT EXISTS public.airport_codes (
            ident VARCHAR,
            type VARCHAR,
            name VARCHAR,
            elevation_ft FLOAT,
            continent VARCHAR,
            iso_country VARCHAR,
            iso_region VARCHAR,
            municipality VARCHAR,
            gps_code VARCHAR,
            iata_code VARCHAR,
            local_code VARCHAR,
            coordinates VARCHAR
        );
        """)


    CREATE_GLOBAL_TEMPERATURE_TABLE_SQL = ("""
        CREATE TABLE IF NOT EXISTS public.temperature (
            average_temperature FLOAT,
            average_temperature_uncertainty FLOAT,
            city VARCHAR,
            country VARCHAR,
            latitude VARCHAR,
            longitude VARCHAR,
            year INT,
            month INT
        );
        """)


    CREATE_I94PORT_TABLE_SQL = ("""
        CREATE TABLE IF NOT EXISTS public.i94port (
            port_code VARCHAR,
            port_city VARCHAR,
            port_state VARCHAR
        );
        """)


    CREATE_I94VISA_TABLE_SQL = ("""
        CREATE TABLE IF NOT EXISTS public.i94visa (
            visa_code INT,
            visa_reason VARCHAR
        );
        """)

    CREATE_I94MODE_TABLE_SQL = ("""
        CREATE TABLE IF NOT EXISTS public.i94mode (
            transport_code INT,
            transport_name VARCHAR
        );
        """)
    
    CREATE_I94CITRES_TABLE_SQL = ("""
        CREATE TABLE IF NOT EXISTS public.i94citres (
            country_code INT,
            country_name VARCHAR
        );
        """)

    CREATE_I94ADDR_TABLE_SQL = ("""
        CREATE TABLE IF NOT EXISTS public.i94addr (
            state_code VARCHAR,
            state_name VARCHAR
        );
        """)
    
    CREATE_IMMIGRATION_TABLE_SQL = ("""
        CREATE TABLE IF NOT EXISTS public.immigration (
            cicid FLOAT,
            i94yr FLOAT,
            i94mon FLOAT,
            i94cit FLOAT,
            i94res FLOAT,
            i94port VARCHAR,
            arrdate FLOAT,
            i94mode FLOAT,
            i94addr varchar,
            depdate FLOAT,
            i94bir FLOAT,
            i94visa FLOAT,
            count FLOAT,
            dtadfile VARCHAR,
            visapost VARCHAR,
            occup VARCHAR,
            entdepa VARCHAR,
            entdepd VARCHAR,
            entdepu VARCHAR,
            matflag VARCHAR,
            biryear FLOAT,
            dtaddto VARCHAR,
            gender VARCHAR,
            insnum VARCHAR,
            airline VARCHAR,
            admnum FLOAT,
            fltno VARCHAR,
            visatype VARCHAR
        );
        """)
    
    COPY_CSV_DATA = ("""
            COPY {}
            FROM '{}' 
            ACCESS_KEY_ID '{}'
            SECRET_ACCESS_KEY '{}'
            REGION 'us-west-2'
            IGNOREHEADER 1
            DELIMITER '{}'
            COMPUPDATE OFF
            TRUNCATECOLUMNS
            CSV;
        """)

    DROP_US_DEMOGRAPH_TABLE_SQL = ("""
        DROP TABLE IF EXISTS PUBLIC.us_cities_demographics;
    """)
    
    DROP_AIRPORT_CODES_TABLE_SQL = ("""
        DROP TABLE IF EXISTS PUBLIC.airport_codes;
    """)
    
    DROP_GLOBAL_TEMPERATURE_TABLE_SQL = ("""
        DROP TABLE IF EXISTS PUBLIC.temperature;
    """)
    
    DROP_I94PORT_TABLE_SQL = ("""
        DROP TABLE IF EXISTS PUBLIC.i94port;
    """)
    
    DROP_I94VISA_TABLE_SQL = ("""
        DROP TABLE IF EXISTS PUBLIC.i94visa;
    """)
    
    DROP_I94MODE_TABLE_SQL = ("""
        DROP TABLE IF EXISTS PUBLIC.i94mode;
    """)
    
    DROP_I94CITRES_TABLE_SQL = ("""
        DROP TABLE IF EXISTS PUBLIC.i94citres;
    """)
    
    DROP_I94ADDR_TABLE_SQL = ("""
        DROP TABLE IF EXISTS PUBLIC.i94addr;
    """)
    
    DROP_IMMIGRATION_TABLE_SQL = ("""
        DROP TABLE IF EXISTS PUBLIC.immigration;
    """)
    
    
    COPY_PARQUET_DATA = ("""
                        COPY {} 
                        FROM '{}'
                        IAM_ROLE '{}'
                        FORMAT AS PARQUET;
                       """)

.open 'class.db'

-- first create a temp table to make the rest of the homework easier
DROP TABLE IF EXISTS Allvideos;
CREATE TEMPORARY TABLE Allvideos AS 
-- need the CTE/WITH per https://stackoverflow.com/questions/26491230/sqlite-query-results-into-a-temp-table
WITH the_data AS (
    SELECT video_id, category_id, "ca" AS language FROM CAvideos
    UNION ALL
    SELECT video_id, category_id, "de" AS language FROM DEvideos
    UNION ALL
    SELECT video_id, category_id, "fr" AS language FROM FRvideos
    UNION ALL
    SELECT video_id, category_id, "gb" AS language FROM GBvideos
    UNION ALL
    SELECT video_id, category_id, "us" AS language FROM USvideos
)
SELECT * FROM the_data;

-- then output the contents of the table to fulfill the HW problem
SELECT * FROM Allvideos;

LOAD tributary;

CREATE OR REPLACE VIEW docker_kafka_gettingstarted AS
SELECT * FROM
tributary_scan_topic('demo',
  "bootstrap.servers" := "localhost:9092",
  "group.id" := "test123"
);

-- SELECT * FROM docker_kafka_gettingstarted;

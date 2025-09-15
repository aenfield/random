LOAD tributary;

CREATE OR REPLACE VIEW icecube_json_alerts AS
SELECT * EXCLUDE message, decode(message)::json as message FROM
tributary_scan_topic('gcn.notices.icecube.lvk_nu_track_search',
  "bootstrap.servers" := "kafka.gcn.nasa.gov",
  "group.id" := "test123",
  "sasl.mechanisms" := "OAUTHBEARER",
  "sasl.oauthbearer.client.id" := getenv('GCN_ICECUBE_ID'),
  "sasl.oauthbearer.client.secret" := getenv('GCN_ICECUBE_SECRET'),
  "sasl.oauthbearer.method" := "oidc",
  "sasl.oauthbearer.token.endpoint.url" := "https://auth.gcn.nasa.gov/oauth2/token",
  "security.protocol" := "sasl_ssl"
);

CREATE OR REPLACE VIEW icecube_alerts AS
SELECT
 message ->> '$.ref_ID' as ref_id,
(message ->> '$.alert_datetime')::timestamp as alert_datetime,
(message ->> '$.pval_bayesian')::double as pval_bayesian,
(message ->> '$.n_events_coincident')::integer as n_events_coincident,
(message ->> '$.neutrino_flux_sensitivity_range.flux_sensitivity')::double[] as flux_sensitivity,
(message ->> '$.neutrino_flux_sensitivity_range.sensitive_energy_range')::integer[] as sensitive_energy_range
  from icecube_json_alerts;

-- Now show the latest alerts.
-- SELECT alert_datetime, ref_id, pval_bayesian, flux_sensitivity, sensitive_energy_range
-- FROM icecube_alerts ORDER BY alert_datetime;
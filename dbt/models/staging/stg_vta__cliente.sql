
WITH source_data AS (

    SELECT distinct *
    FROM {{ source('landing_vta', 'vta_cliente') }}

),

cleaned AS (

    SELECT
        TRY_CAST(TRIM(ClaCliente) AS INTEGER) AS cla_cliente,

        TRIM(NomCliente) AS nom_cliente,

        UPPER(TRIM(Segmento)) AS segmento,

        UPPER(TRIM(ClaEstado)) AS cla_estado,

        TRY_CAST(
            _ab_cdc_updated_at AS TIMESTAMPTZ
        ) AS fecha_actualizacion_cdc,

        TRY_CAST(
            _ab_cdc_lsn AS BIGINT
        ) AS cdc_lsn,

        TRY_CAST(
            _ab_cdc_deleted_at AS TIMESTAMPTZ
        ) AS fecha_eliminacion_cdc,

        TRY_CAST(
            _airbyte_extracted_at AS TIMESTAMPTZ
        ) AS fecha_extraccion_airbyte

    FROM source_data

)

SELECT *
FROM cleaned

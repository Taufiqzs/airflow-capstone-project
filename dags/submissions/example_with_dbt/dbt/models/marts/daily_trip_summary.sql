{{
    config(
        materialized='table',
        partition_by={'field': 'trip_date', 'data_type': 'date'},
        cluster_by=['pickup_zone_id']
    )
}}

select
    trip_date,
    pickup_zone_id,
    count(*) as trip_count,
    round(sum(total_amount), 2) as total_revenue
from {{ ref('stg_trips') }}
group by trip_date, pickup_zone_id

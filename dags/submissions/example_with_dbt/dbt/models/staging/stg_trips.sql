with source as (
    select *
    from unnest([
        struct('trip-001' as trip_id, date '2026-07-01' as trip_date, 1 as pickup_zone_id, 15.50 as total_amount),
        struct('trip-002' as trip_id, date '2026-07-01' as trip_date, 1 as pickup_zone_id, 22.00 as total_amount),
        struct('trip-003' as trip_id, date '2026-07-01' as trip_date, 2 as pickup_zone_id, 18.25 as total_amount),
        struct('trip-004' as trip_id, date '2026-07-02' as trip_date, 1 as pickup_zone_id, 12.75 as total_amount)
    ])
)

select * from source

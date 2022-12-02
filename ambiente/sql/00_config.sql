-- use este arquivo para implementar os parâmetros para otimização
-- do postgresql ou outras configurações do banco de dados.
-- http://pgconfigurator.cybertec.at/
-- https://pgtune.leopard.in.ua/

-- Postgresql on ZFS
ALTER SYSTEM SET synchronous_commit = 'off';
ALTER SYSTEM SET full_page_writes = 'off';

-- Connectivity
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET superuser_reserved_connections = 3;

-- Memory Settings
ALTER SYSTEM SET shared_buffers = '8192 MB';
ALTER SYSTEM SET work_mem = '256 MB';
ALTER SYSTEM SET maintenance_work_mem = '520 MB';
ALTER SYSTEM SET effective_cache_size = '22 GB';
ALTER SYSTEM SET effective_io_concurrency = 100;
ALTER SYSTEM SET random_page_cost = 1.25;

-- Parallel queries:
ALTER SYSTEM SET max_worker_processes = 8;
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
ALTER SYSTEM SET max_parallel_maintenance_workers = 4;
ALTER SYSTEM SET max_parallel_workers = 8;
ALTER SYSTEM SET parallel_leader_participation = on;

-- Advanced features
ALTER SYSTEM SET enable_partitionwise_join = on;
ALTER SYSTEM SET enable_partitionwise_aggregate = on;
ALTER SYSTEM SET jit = on;
ALTER SYSTEM SET enable_hashjoin = 'off';
ALTER SYSTEM SET enable_mergejoin = 'off';
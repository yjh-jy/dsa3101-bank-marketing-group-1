CREATE TABLE IF NOT EXISTS engagements (
    campaign_id INT PRIMARY KEY,
    income_category VARCHAR(50),
    target_audience VARCHAR(50),
    channel_used VARCHAR(50),
    has_engaged INT
);
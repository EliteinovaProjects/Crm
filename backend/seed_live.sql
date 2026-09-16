-- =============================================================================
-- CRM — Full schema + seed users for the LIVE Neon database
-- =============================================================================
-- Why this file exists
-- --------------------
-- This is the pure-SQL equivalent of what `alembic upgrade head` does
-- (see alembic/versions/7cdabde502d3_initial_migration.py). It creates every
-- table the application expects AND inserts the initial Admin and Employee
-- users. It is safe to run more than once
-- (CREATE ... IF NOT EXISTS / ON CONFLICT DO NOTHING).
--
-- How to run it against Neon
-- --------------------------
-- Option 1 — Neon SQL Editor (easiest):
--   1. Open https://console.neon.tech -> your project -> SQL Editor.
--   2. Paste the entire contents of this file and click "Run".
--
-- Option 2 — psql from your machine:
--   psql "postgresql://neondb_owner:****@ep-xxxx-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require" -f seed_live.sql
--
-- After running this, `alembic upgrade head` will be a no-op (the version row
-- is stamped at the end of this script to the initial migration revision).
--
-- NOTE: You do NOT need this script if you already ran
-- `alembic upgrade head` (the migration creates the same tables). This script
-- is the pure-SQL alternative for when you want to set everything up from the
-- Neon SQL Editor, and it also inserts the two seed users.
-- =============================================================================

BEGIN;

-- ---------------------------------------------------------------------------
-- 1. Enum type used by users.role
-- ---------------------------------------------------------------------------
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN
        CREATE TYPE userrole AS ENUM ('ADMIN', 'SUB_ADMIN', 'EMPLOYEE');
    END IF;
END$$;

-- ---------------------------------------------------------------------------
-- 2. Tables (dependency order)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS agent_groups (
    id VARCHAR NOT NULL,
    group_name VARCHAR NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    UNIQUE (group_name)
);

CREATE TABLE IF NOT EXISTS api_integrations (
    id VARCHAR NOT NULL,
    integration_name VARCHAR NOT NULL,
    api_key VARCHAR NOT NULL,
    api_secret VARCHAR NOT NULL,
    endpoint_url VARCHAR,
    is_active BOOLEAN,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS blacklist (
    id VARCHAR NOT NULL,
    phone_number VARCHAR NOT NULL,
    reason TEXT,
    blocked_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    UNIQUE (phone_number)
);

CREATE TABLE IF NOT EXISTS break_reasons (
    id VARCHAR NOT NULL,
    reason_name VARCHAR NOT NULL,
    description VARCHAR,
    is_active VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    UNIQUE (reason_name)
);

CREATE TABLE IF NOT EXISTS categories (
    id VARCHAR NOT NULL,
    lead_type VARCHAR NOT NULL,
    category_name VARCHAR NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    UNIQUE (category_name)
);

CREATE TABLE IF NOT EXISTS contacts (
    id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    phone_number VARCHAR NOT NULL,
    email VARCHAR,
    address TEXT,
    company VARCHAR,
    notes TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    UNIQUE (phone_number)
);

CREATE TABLE IF NOT EXISTS did_numbers (
    id VARCHAR NOT NULL,
    phone_number VARCHAR NOT NULL,
    provider VARCHAR,
    is_active BOOLEAN,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    UNIQUE (phone_number)
);

CREATE TABLE IF NOT EXISTS dispositions (
    id VARCHAR NOT NULL,
    disposition_name VARCHAR NOT NULL,
    description TEXT,
    is_active VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    UNIQUE (disposition_name)
);

CREATE TABLE IF NOT EXISTS holidays (
    id VARCHAR NOT NULL,
    holiday_name VARCHAR NOT NULL,
    holiday_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    description TEXT,
    is_recurring VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS ivr_flows (
    id VARCHAR NOT NULL,
    flow_name VARCHAR NOT NULL,
    flow_config TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS lead_fields (
    id VARCHAR NOT NULL,
    field_name VARCHAR NOT NULL,
    field_type VARCHAR NOT NULL,
    is_required BOOLEAN,
    options TEXT,
    placeholder VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS payment_history (
    id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    amount INTEGER NOT NULL,
    payment_method VARCHAR,
    transaction_id VARCHAR,
    status VARCHAR,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS renewal_history (
    id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    plan_type VARCHAR NOT NULL,
    amount INTEGER NOT NULL,
    start_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    end_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    payment_method VARCHAR,
    transaction_id VARCHAR,
    status VARCHAR,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sms_templates (
    id VARCHAR NOT NULL,
    template_name VARCHAR NOT NULL,
    template_content TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    UNIQUE (template_name)
);

CREATE TABLE IF NOT EXISTS sound_library (
    id VARCHAR NOT NULL,
    sound_name VARCHAR NOT NULL,
    file_url VARCHAR NOT NULL,
    description TEXT,
    duration VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS sources (
    id VARCHAR NOT NULL,
    lead_type VARCHAR NOT NULL,
    source_name VARCHAR NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    UNIQUE (source_name)
);

CREATE TABLE IF NOT EXISTS statuses (
    id VARCHAR NOT NULL,
    status_name VARCHAR NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    UNIQUE (status_name)
);

CREATE TABLE IF NOT EXISTS system_logs (
    id VARCHAR NOT NULL,
    endpoint VARCHAR NOT NULL,
    method VARCHAR NOT NULL,
    user_id VARCHAR,
    ip_address VARCHAR,
    user_agent TEXT,
    status_code INTEGER NOT NULL,
    processing_time INTEGER,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS topup_history (
    id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    coin_type VARCHAR NOT NULL,
    amount INTEGER NOT NULL,
    payment_method VARCHAR,
    transaction_id VARCHAR,
    status VARCHAR,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    username VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    role userrole NOT NULL,
    phone VARCHAR,
    is_active BOOLEAN,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS attendance (
    id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    check_in_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    check_out_time TIMESTAMP WITHOUT TIME ZONE,
    total_break_duration INTEGER,
    status VARCHAR,
    notes TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS campaigns (
    id VARCHAR NOT NULL,
    campaign_name VARCHAR NOT NULL,
    campaign_type VARCHAR NOT NULL,
    call_pacing_ratio INTEGER,
    did_id VARCHAR,
    scheduled_at TIMESTAMP WITHOUT TIME ZONE,
    closure_at TIMESTAMP WITHOUT TIME ZONE,
    working_hours_start VARCHAR,
    working_hours_end VARCHAR,
    retry_attempts INTEGER,
    duration_between_retry INTEGER,
    assignment_type VARCHAR,
    schedule_days TEXT,
    save_to_contacts BOOLEAN,
    first_call_strategy VARCHAR,
    is_active BOOLEAN,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(did_id) REFERENCES did_numbers (id)
);

CREATE TABLE IF NOT EXISTS coin_wallets (
    id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    inbound_coins INTEGER,
    outbound_coins INTEGER,
    sms_coins INTEGER,
    email_coins INTEGER,
    fax_coins INTEGER,
    common_coins INTEGER,
    last_reset_date TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS leads (
    id VARCHAR NOT NULL,
    account VARCHAR,
    name VARCHAR NOT NULL,
    mobile_number VARCHAR NOT NULL,
    alternate_number VARCHAR,
    email VARCHAR,
    address TEXT,
    description TEXT,
    assigned_agent_id VARCHAR,
    source_id VARCHAR,
    status_id VARCHAR,
    category_id VARCHAR,
    follow_up_date TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    is_deleted BOOLEAN,
    deleted_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(assigned_agent_id) REFERENCES users (id),
    FOREIGN KEY(source_id) REFERENCES sources (id),
    FOREIGN KEY(status_id) REFERENCES statuses (id),
    FOREIGN KEY(category_id) REFERENCES categories (id)
);

CREATE TABLE IF NOT EXISTS notifications (
    id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR,
    is_read BOOLEAN,
    read_at TIMESTAMP WITHOUT TIME ZONE,
    action_url VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS reminders (
    id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT,
    reminder_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    is_completed BOOLEAN,
    completed_at TIMESTAMP WITHOUT TIME ZONE,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS breaks (
    id VARCHAR NOT NULL,
    attendance_id VARCHAR NOT NULL,
    break_reason_id VARCHAR NOT NULL,
    start_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    end_time TIMESTAMP WITHOUT TIME ZONE,
    duration INTEGER,
    notes TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(attendance_id) REFERENCES attendance (id),
    FOREIGN KEY(break_reason_id) REFERENCES break_reasons (id)
);

CREATE TABLE IF NOT EXISTS call_logs (
    id VARCHAR NOT NULL,
    agent_id VARCHAR NOT NULL,
    lead_id VARCHAR,
    phone_number VARCHAR NOT NULL,
    call_direction VARCHAR,
    call_status VARCHAR,
    duration INTEGER,
    recording_url VARCHAR,
    disposition VARCHAR,
    notes TEXT,
    started_at TIMESTAMP WITHOUT TIME ZONE,
    ended_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(agent_id) REFERENCES users (id),
    FOREIGN KEY(lead_id) REFERENCES leads (id)
);

CREATE TABLE IF NOT EXISTS campaign_bases (
    id VARCHAR NOT NULL,
    campaign_id VARCHAR NOT NULL,
    contact_name VARCHAR,
    phone_number VARCHAR NOT NULL,
    email VARCHAR,
    custom_data TEXT,
    call_status VARCHAR,
    call_attempts INTEGER,
    last_called_at TIMESTAMP WITHOUT TIME ZONE,
    is_active BOOLEAN,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(campaign_id) REFERENCES campaigns (id)
);

CREATE TABLE IF NOT EXISTS coin_transactions (
    id VARCHAR NOT NULL,
    wallet_id VARCHAR NOT NULL,
    transaction_type VARCHAR NOT NULL,
    coin_type VARCHAR NOT NULL,
    amount INTEGER NOT NULL,
    description TEXT,
    reference_id VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(wallet_id) REFERENCES coin_wallets (id)
);

CREATE TABLE IF NOT EXISTS lead_field_values (
    id VARCHAR NOT NULL,
    lead_id VARCHAR NOT NULL,
    field_id VARCHAR NOT NULL,
    value TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    updated_at TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (id),
    FOREIGN KEY(lead_id) REFERENCES leads (id),
    FOREIGN KEY(field_id) REFERENCES lead_fields (id)
);

-- ---------------------------------------------------------------------------
-- 3. Indexes
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS ix_agent_groups_id ON agent_groups (id);
CREATE INDEX IF NOT EXISTS ix_api_integrations_id ON api_integrations (id);
CREATE INDEX IF NOT EXISTS ix_blacklist_id ON blacklist (id);
CREATE INDEX IF NOT EXISTS ix_break_reasons_id ON break_reasons (id);
CREATE INDEX IF NOT EXISTS ix_categories_id ON categories (id);
CREATE INDEX IF NOT EXISTS ix_contacts_id ON contacts (id);
CREATE INDEX IF NOT EXISTS ix_did_numbers_id ON did_numbers (id);
CREATE INDEX IF NOT EXISTS ix_dispositions_id ON dispositions (id);
CREATE INDEX IF NOT EXISTS ix_holidays_id ON holidays (id);
CREATE INDEX IF NOT EXISTS ix_ivr_flows_id ON ivr_flows (id);
CREATE INDEX IF NOT EXISTS ix_lead_fields_id ON lead_fields (id);
CREATE INDEX IF NOT EXISTS ix_payment_history_id ON payment_history (id);
CREATE INDEX IF NOT EXISTS ix_renewal_history_id ON renewal_history (id);
CREATE INDEX IF NOT EXISTS ix_sms_templates_id ON sms_templates (id);
CREATE INDEX IF NOT EXISTS ix_sound_library_id ON sound_library (id);
CREATE INDEX IF NOT EXISTS ix_sources_id ON sources (id);
CREATE INDEX IF NOT EXISTS ix_statuses_id ON statuses (id);
CREATE INDEX IF NOT EXISTS ix_system_logs_id ON system_logs (id);
CREATE INDEX IF NOT EXISTS ix_topup_history_id ON topup_history (id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);
CREATE INDEX IF NOT EXISTS ix_users_id ON users (id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users (username);
CREATE INDEX IF NOT EXISTS ix_attendance_id ON attendance (id);
CREATE INDEX IF NOT EXISTS ix_campaigns_id ON campaigns (id);
CREATE INDEX IF NOT EXISTS ix_coin_wallets_id ON coin_wallets (id);
CREATE INDEX IF NOT EXISTS ix_leads_id ON leads (id);
CREATE INDEX IF NOT EXISTS ix_leads_mobile_number ON leads (mobile_number);
CREATE INDEX IF NOT EXISTS ix_notifications_id ON notifications (id);
CREATE INDEX IF NOT EXISTS ix_reminders_id ON reminders (id);
CREATE INDEX IF NOT EXISTS ix_breaks_id ON breaks (id);
CREATE INDEX IF NOT EXISTS ix_call_logs_id ON call_logs (id);
CREATE INDEX IF NOT EXISTS ix_campaign_bases_id ON campaign_bases (id);
CREATE INDEX IF NOT EXISTS ix_coin_transactions_id ON coin_transactions (id);
CREATE INDEX IF NOT EXISTS ix_lead_field_values_id ON lead_field_values (id);

-- ---------------------------------------------------------------------------
-- 4. Seed users
--    Passwords are bcrypt hashes (generated with the app's own hasher):
--      admin      / Admin@123
--      employee1  / Employee@123
--    ON CONFLICT (username) DO NOTHING keeps this idempotent and never
--    overwrites an existing user's password.
-- ---------------------------------------------------------------------------
INSERT INTO users (id, email, username, hashed_password, full_name, role, phone, is_active, created_at, updated_at)
VALUES
    (
        'USR20260915120000ADMIN1',
        'admin@daffytel.com',
        'admin',
        '$2b$12$UvRCzxXmdFlu8Dhxe7pPNOhVCO0zDsxkC2GU8cr1uCdWHoLdt7eQW',
        'Administrator',
        'ADMIN',
        NULL,
        TRUE,
        NOW(),
        NOW()
    ),
    (
        'USR20260915120000EMP001',
        'employee1@daffytel.com',
        'employee1',
        '$2b$12$5RXFhuAr0tamDfViKW2MqOp9igbaJBE4kYv1svkkdegPIJ2IjHM.m',
        'Employee One',
        'EMPLOYEE',
        NULL,
        TRUE,
        NOW(),
        NOW()
    )
ON CONFLICT (username) DO NOTHING;

-- ---------------------------------------------------------------------------
-- 5. Stamp Alembic so `alembic upgrade head` is a no-op afterwards.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

INSERT INTO alembic_version (version_num)
SELECT '7cdabde502d3'
WHERE NOT EXISTS (SELECT 1 FROM alembic_version);

COMMIT;

-- ---------------------------------------------------------------------------
-- 6. Verify
-- ---------------------------------------------------------------------------
-- SELECT username, role, is_active FROM users ORDER BY username;
-- SELECT count(*) AS table_count FROM information_schema.tables
--   WHERE table_schema = 'public';
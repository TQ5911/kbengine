CREATE TABLE IF NOT EXISTS alliance (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- alliance_name: was `name` (reserved keyword in MySQL 8+)
    alliance_name VARCHAR(21) NOT NULL,
    declaration VARCHAR(135) NOT NULL DEFAULT '',
    leader_guild_id BIGINT UNSIGNED NOT NULL,
    approve_type TINYINT NOT NULL DEFAULT 1,
    fund BIGINT NOT NULL DEFAULT 0,
    -- alliance_state: was `state` (STATE is also a MySQL 8+ reserved keyword)
    alliance_state TINYINT NOT NULL DEFAULT 1,
    created_at INT NOT NULL,
    updated_at INT NOT NULL,
    UNIQUE KEY uk_alliance_name (alliance_name),
    KEY idx_leader (leader_guild_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS alliance_member (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    alliance_id BIGINT UNSIGNED NOT NULL,
    guild_id BIGINT UNSIGNED NOT NULL,
    server_id INT UNSIGNED NOT NULL DEFAULT 0,
    guild_score BIGINT UNSIGNED NOT NULL DEFAULT 0,
    member_count INT UNSIGNED NOT NULL DEFAULT 0,
    -- === Guild leader personal info (帮会会长个人信息) ===
    leader_gb_id BIGINT UNSIGNED NOT NULL DEFAULT 0,
    leader_name VARCHAR(60) NOT NULL DEFAULT '',
    leader_level INT UNSIGNED NOT NULL DEFAULT 0,
    leader_profession INT NOT NULL DEFAULT 0,
    leader_gender TINYINT NOT NULL DEFAULT 0,
    -- member_role: was `role` (reserved keyword in MySQL 8+)
    member_role TINYINT NOT NULL DEFAULT 2,
    join_time INT NOT NULL,
    guild_icon INT UNSIGNED NOT NULL DEFAULT 0,
    guild_level INT UNSIGNED NOT NULL DEFAULT 0,
    -- === Guild-level attributes only(盟主数据已上提 alliance) ===
    guild_name VARCHAR(60) NOT NULL DEFAULT '',
    dsp_flag INT UNSIGNED NOT NULL DEFAULT 0,
    max_member_num INT UNSIGNED NOT NULL DEFAULT 0,
    UNIQUE KEY uk_guild (guild_id),
    KEY idx_alliance (alliance_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS alliance_apply (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    alliance_id BIGINT UNSIGNED NOT NULL,
    guild_id BIGINT UNSIGNED NOT NULL,
    guild_name VARCHAR(60) NOT NULL DEFAULT '',
    guild_score BIGINT UNSIGNED NOT NULL DEFAULT 0,
    server_id INT UNSIGNED NOT NULL DEFAULT 0,
    -- apply_state: was `status` (reserved keyword in MySQL 8+)
    apply_state TINYINT NOT NULL DEFAULT 0,
    created_at INT NOT NULL,
    -- ==== Guild-level cosmetic attributes (snapshot at apply time) ====
    guild_icon INT UNSIGNED NOT NULL DEFAULT 0,
    dsp_flag INT UNSIGNED NOT NULL DEFAULT 0,
    KEY idx_alliance (alliance_id),
    KEY idx_guild (guild_id),
    KEY idx_alliance_state (alliance_id, apply_state),
    KEY idx_guild_state (guild_id, apply_state)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS alliance_invite (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    alliance_id BIGINT UNSIGNED NOT NULL,
    alliance_name VARCHAR(21) NOT NULL DEFAULT '',
    guild_id BIGINT UNSIGNED NOT NULL,
    server_id INT UNSIGNED NOT NULL DEFAULT 0,
    -- invite_state: was `status` (reserved keyword in MySQL 8+)
    invite_state TINYINT NOT NULL DEFAULT 0,
    created_at INT NOT NULL,
    KEY idx_guild (guild_id),
    KEY idx_guild_state (guild_id, invite_state)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS alliance_enemy (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    attacker_type TINYINT NOT NULL,
    attacker_id BIGINT UNSIGNED NOT NULL,
    attacker_server_id INT UNSIGNED NOT NULL,
    target_type TINYINT NOT NULL,
    target_id BIGINT UNSIGNED NOT NULL,
    target_server_id INT UNSIGNED NOT NULL,
    end_time INT NOT NULL,
    created_at INT NOT NULL,
    KEY idx_attacker (attacker_type, attacker_id),
    KEY idx_target (target_type, target_id),
    UNIQUE KEY uk_relation (attacker_type, attacker_id, target_type, target_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS alliance_event (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    alliance_id BIGINT UNSIGNED NOT NULL,
    event_type INT NOT NULL,
    params_json VARCHAR(500) NOT NULL DEFAULT '',
    created_at INT NOT NULL,
    KEY idx_alliance_time (alliance_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS alliance_donate_log (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    alliance_id BIGINT UNSIGNED NOT NULL,
    guild_id BIGINT UNSIGNED NOT NULL,
    amount BIGINT NOT NULL DEFAULT 0,
    league_fund_get BIGINT NOT NULL DEFAULT 0,
    created_at INT NOT NULL,
    KEY idx_alliance (alliance_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS alliance_aid_log (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    alliance_id BIGINT UNSIGNED NOT NULL,
    from_guild_id BIGINT UNSIGNED NOT NULL,
    to_guild_id BIGINT UNSIGNED NOT NULL,
    amount BIGINT NOT NULL DEFAULT 0,
    created_at INT NOT NULL,
    KEY idx_alliance (alliance_id),
    KEY idx_from (from_guild_id),
    KEY idx_to (to_guild_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
